import time
import logging
import warnings
warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)


class GeminiClient:
    def __init__(self, api_key: str = None):
        from django.conf import settings
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model = None
        self.available = False
        self._configure()

    def _configure(self):
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-3.6-flash')
            self.available = True
        except Exception as e:
            logger.error(f"Gemini configuration failed: {e}")
            self.available = False

    def generate_response(self, prompt: str) -> dict:
        start_time = time.time()

        if not self.available or not self.api_key:
            return self._mock_response(prompt, start_time)

        try:
            import google.generativeai as genai
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=1024,
                    temperature=0.3,
                )
            )
            end_time = time.time()
            text = response.text if response.text else "No response generated."

            return {
                'success': True,
                'response': text.strip(),
                'response_time': round(end_time - start_time, 3),
                'token_count': len(text.split()),
                'error': None,
            }

        except Exception as e:
            end_time = time.time()
            logger.error(f"Gemini API error: {e}")
            return {
                'success': False,
                'response': f"API Error: {str(e)}",
                'response_time': round(end_time - start_time, 3),
                'token_count': 0,
                'error': str(e),
            }

    def _mock_response(self, prompt: str, start_time: float) -> dict:
        time.sleep(0.3)
        end_time = time.time()
        demo_text = "Demo mode — set GEMINI_API_KEY in settings.py for real responses."
        return {
            'success': True,
            'response': demo_text,
            'response_time': round(end_time - start_time, 3),
            'token_count': len(demo_text.split()),
            'error': None,
        }