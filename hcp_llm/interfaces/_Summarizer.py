# -*- coding: utf-8 -*-
"""
Gather article details from the PubMed API
"""
import openai


class SummarizerAI:
    def __init__(self, openai_key: str, prompt: str, model: str, temperature: float) -> None:
        self._openaikey = openai_key
        self._prompt = prompt
        self._model = model
        self._temperature = temperature


    def get_response(self) -> str:
        openai.api_key =self._openaikey
        messages = [{"role": "user", "content": self._prompt}]
        response = openai.chat.completions.create(
                            model=self._model,
                            messages=messages,
                            temperature=0.2,
                        )
        response = response.choices[0].message.content.strip()
        return response