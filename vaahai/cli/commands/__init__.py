"""
Command initialization module.

This module initializes all CLI commands but avoids eager imports of ML-dependent modules.
"""

# Only import config directly - it has no ML dependencies
from . import config

# Other commands are imported dynamically when needed to avoid dependency issues
__all__ = ['config']
