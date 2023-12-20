"""
Wrapper for stability.ai API
"""
import base64
import os
import requests


class StabilityAPI:
    def __init__(self, engine_id: str = "stable-diffusion-xl-1024-v1-0"):
        self.engine_id = engine_id
        self.api_host = os.getenv("STABILITY_API_HOST", "https://api.stability.ai")
        self.api_key = os.getenv("STABILITY_API_KEY")

    def generate_image(self, prompt: str) -> dict:
        if self.api_key is None:
            raise Exception("Missing Stability API key.")

        response = requests.post(
            f"{self.api_host}/v1/generation/{self.engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            json={
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 30,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            },
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        return response.json()
