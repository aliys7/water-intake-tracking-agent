from dotenv import load_dotenv
from scripts.openrouter_client import get_openrouter_response

load_dotenv()

class WaterIntakeAgent:
    def analyze_intake(self, total_ml):
        prompt = f"""
        You are a hydration specialist. The user has consumed {total_ml} ml today.
        Provide a concise hydration status and personalized advice.
        """
        return get_openrouter_response(prompt)