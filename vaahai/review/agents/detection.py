import json
from vaahai.config.manager import ConfigManager
from vaahai.llm_utils import get_llm_client

class LLMLanguageFrameworkCMSDetectionAgent:
    """
    Uses the default LLM provider to detect language, framework, and CMS from code.
    """
    def __init__(self):
        self.config = ConfigManager()
        self.llm_client = get_llm_client(self.config.get_default_llm_provider())

    def detect(self, code: str) -> dict:
        prompt = (
            "Analyze the following code and strictly answer in this JSON format:\n"
            "{\n  'language': <main programming language>,\n  'framework': <main framework or null>,\n  'cms': <main CMS or null>\n}\n"
            "If framework or CMS are not detected, use null.\n"
            "Code:\n" + code
        )
        response = self.llm_client.complete(prompt)
        # Try to extract JSON from the response
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            result = json.loads(response[json_start:json_end].replace("'", '"'))
            return {
                'language': result.get('language', 'Unknown'),
                'framework': result.get('framework'),
                'cms': result.get('cms'),
            }
        except Exception:
            return {'language': 'Unknown', 'framework': None, 'cms': None}
