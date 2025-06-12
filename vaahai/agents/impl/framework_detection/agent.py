"""
Framework/CMS detection agent implementation.

This module provides a specialized agent that can identify popular web
frameworks, libraries, and content-management systems (CMS) used in a source
code repository. It relies on:

1. Dependency manifests (package.json, requirements.txt, composer.json, etc.)
2. Characteristic configuration files (angular.json, next.config.js, gatsby-config.js)
3. File / directory signatures (wp-config.php, wp-admin/, manage.py, artisan)
4. Keyword / import pattern matching inside source files

The implementation purposefully keeps the heuristic ruleset small and easy to
extend. It mirrors the design of the LanguageDetectionAgent so that additional
LLM-powered detection can be plugged-in later.
"""

from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from vaahai.agents.base.agent_base import AgentBase
from vaahai.agents.base.agent_registry import AgentRegistry
from vaahai.agents.utils.prompt_manager import PromptManager

logger = logging.getLogger(__name__)


@AgentRegistry.register("framework_detection")
class FrameworkDetectionAgent(AgentBase):
    """Detect web frameworks and CMS used in a project directory."""

    #: Confidence weights
    DEP_WEIGHT = 0.9
    FILE_WEIGHT = 0.8
    CODE_WEIGHT = 0.6

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prompt_manager = PromptManager(agent_type="framework_detection", agent_name=self.name)
        self.patterns = self._initialize_patterns()
        self.llm_client = self._initialize_llm_client()
        # Cache last analysed result keyed by absolute project path -> result
        self._cache: Dict[str, Dict[str, Any]] = {}

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------

    def run(self, project_path: str) -> Dict[str, Any]:
        """Analyse *project_path* and return detected frameworks / CMS.

        Args:
            project_path: Absolute or relative path to the root of a project
        Returns:
            Dict with the same structure as described in the system prompt.
        """
        project_path = os.path.abspath(project_path)
        if project_path in self._cache:
            return self._cache[project_path]

        if not os.path.isdir(project_path):
            raise ValueError(f"'{project_path}' is not a valid directory path")

        # 1. Gather project files list and limited code samples
        files: List[Path] = [Path(root) / f for root, _dirs, fnames in os.walk(project_path) for f in fnames]

        # 2. Apply detection strategies
        dep_candidates = self._detect_from_dependency_files(files)
        file_sig_candidates = self._detect_from_file_signatures(files)
        code_candidates = self._detect_from_code_patterns(files)

        # 3. Merge results (framework -> confidence)
        merged: Dict[str, float] = {}
        for name, conf in (*dep_candidates, *file_sig_candidates, *code_candidates):
            merged[name] = max(conf, merged.get(name, 0.0))

        # 4. Build ordered list of candidates
        ordered = sorted(merged.items(), key=lambda x: x[1], reverse=True)

        if not ordered:
            result = self._detect_with_llm(project_path)
            self._cache[project_path] = result
            return result

        primary_name, primary_conf = ordered[0]
        secondary = [{"name": n, "confidence": c, "type": self.patterns[n]["type"]} for n, c in ordered[1:]]

        cms_detection = next(((n, c) for n, c in ordered if self.patterns[n]["type"] == "cms"), (None, 0.0))
        cms_result = {"name": cms_detection[0] or "None", "confidence": cms_detection[1] if cms_detection[0] else 0.9}

        explanation = (
            f"Detected {primary_name} with confidence {primary_conf:.2f}. "
            f"Other matches: {', '.join(n for n, _ in ordered[1:]) or 'none'}."
        )

        result = {
            "primary_framework": {
                "name": primary_name,
                "type": self.patterns[primary_name]["type"],
                "confidence": primary_conf,
            },
            "secondary_frameworks": secondary,
            "cms": cms_result,
            "explanation": explanation,
        }
        self._cache[project_path] = result
        return result

    # ------------------------------------------------------------------
    # Initialisation helpers
    # ------------------------------------------------------------------

    def _initialize_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Return dictionary describing framework / CMS detection patterns."""
        return {
            # ---------- Front-end frameworks -------------------
            "react": {
                "type": "frontend",
                "dependency": ["react"],
                "file_signatures": [re.compile(r".*\\.(jsx|tsx)$")],
                "code_patterns": ["ReactDOM.render", "useState(", "useEffect("],
            },
            "angular": {
                "type": "frontend",
                "dependency": ["@angular/core"],
                "file_signatures": ["angular.json"],
                "code_patterns": ["platformBrowserDynamic", "@NgModule"],
            },
            "vue": {
                "type": "frontend",
                "dependency": ["vue"],
                "file_signatures": [re.compile(r".*\\.vue$")],
                "code_patterns": ["new Vue("],
            },
            # ---------- Back-end frameworks --------------------
            "express": {
                "type": "backend",
                "dependency": ["express"],
                "file_signatures": ["app.js", "server.js"],
                "code_patterns": ["app.get(", "router.get("],
            },
            "django": {
                "type": "backend",
                "dependency": ["django"],
                "file_signatures": ["manage.py", "settings.py"],
                "code_patterns": ["from django"],
            },
            "flask": {
                "type": "backend",
                "dependency": ["flask"],
                "file_signatures": ["app.py"],
                "code_patterns": ["from flask", "Flask(__name__)"],
            },
            "laravel": {
                "type": "backend",
                "dependency": ["laravel/framework"],
                "file_signatures": ["artisan", "config/app.php"],
                "code_patterns": ["Illuminate\\\\", "namespace App\\Protocols"],
            },
            "rails": {
                "type": "backend",
                "dependency": ["rails"],
                "file_signatures": ["config/application.rb"],
                "code_patterns": ["Rails.application"],
            },
            # ---------- CMS -----------------------------------
            "wordpress": {
                "type": "cms",
                "dependency": [],
                "file_signatures": ["wp-config.php", "wp-admin", "wp-includes"],
                "code_patterns": ["define('WP_DEBUG"],
            },
            "drupal": {
                "type": "cms",
                "dependency": [],
                "file_signatures": ["core/lib/Drupal.php", "modules/system"],
                "code_patterns": ["Drupal::"],
            },
            "joomla": {
                "type": "cms",
                "dependency": [],
                "file_signatures": ["configuration.php", "administrator/components"],
                "code_patterns": ["JFactory::"],
            },
        }

    def _initialize_llm_client(self):
        # Placeholder for future integration
        return None

    # ------------------------------------------------------------------
    # Detection helpers
    # ------------------------------------------------------------------

    def _detect_from_dependency_files(self, files: List[Path]) -> List[Tuple[str, float]]:
        """Return list of (framework_name, confidence) based on dependency manifests."""
        results: List[Tuple[str, float]] = []
        # package.json
        pkg_files = [f for f in files if f.name == "package.json"]
        for fpath in pkg_files:
            try:
                data = json.loads(fpath.read_text())
            except Exception:  # pragma: no cover – invalid JSON
                continue
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            for name, p in self.patterns.items():
                if any(dep in deps for dep in p.get("dependency", [])):
                    results.append((name, self.DEP_WEIGHT))
        # requirements.txt, pip
        req_files = [f for f in files if f.name == "requirements.txt"]
        if req_files:
            req_pkgs = set()
            for rf in req_files:
                req_pkgs.update({line.strip().lower().split("==")[0] for line in rf.read_text().splitlines() if line and not line.startswith("#")})
            for name, p in self.patterns.items():
                if any(dep in req_pkgs for dep in p.get("dependency", [])):
                    results.append((name, self.DEP_WEIGHT))
        # composer.json
        comp_files = [f for f in files if f.name == "composer.json"]
        for fpath in comp_files:
            try:
                data = json.loads(fpath.read_text())
            except Exception:  # pragma: no cover
                continue
            deps = {**data.get("require", {}), **data.get("require-dev", {})}
            for name, p in self.patterns.items():
                if any(dep in deps for dep in p.get("dependency", [])):
                    results.append((name, self.DEP_WEIGHT))
        return results

    def _detect_from_file_signatures(self, files: List[Path]) -> List[Tuple[str, float]]:
        """Return list of (framework_name, confidence) based on file / directory presence."""
        results: List[Tuple[str, float]] = []
        for name, p in self.patterns.items():
            for sig in p.get("file_signatures", []):
                if isinstance(sig, re.Pattern):
                    if any(sig.match(str(f)) for f in files):
                        results.append((name, self.FILE_WEIGHT))
                        break
                else:  # simple filename or directory substring
                    if any(sig in str(f) for f in files):
                        results.append((name, self.FILE_WEIGHT))
                        break
        return results

    def _detect_from_code_patterns(self, files: List[Path]) -> List[Tuple[str, float]]:
        """Return list of (framework_name, confidence) inspecting limited code lines."""
        results: List[Tuple[str, float]] = []
        # read small files only (\u003c 64k) to keep it lightweight
        small_files = [f for f in files if f.stat().st_size < 65536]
        for f in small_files:
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for name, p in self.patterns.items():
                if any(kw in text for kw in p.get("code_patterns", [])):
                    results.append((name, self.CODE_WEIGHT))
        return results

    # ------------------------------------------------------------------
    # LLM fallback
    # ------------------------------------------------------------------

    def _detect_with_llm(self, project_path: str) -> Dict[str, Any]:
        """Fallback method when heuristic detection fails."""
        return {
            "primary_framework": {"name": "Unknown", "type": "unknown", "confidence": 0.0},
            "secondary_frameworks": [],
            "cms": {"name": "None", "confidence": 0.9},
            "explanation": "LLM-based detection not yet implemented.",
        }
