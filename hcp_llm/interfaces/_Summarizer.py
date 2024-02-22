# -*- coding: utf-8 -*-
"""
Gather article details from the PubMed API
"""
import openai


class SummarizerAI:
    """SummarizerAI class used to process a specific prompt through OpenAI model."""
    def __init__(self, openai_key: str, prompt: str, model: str, temperature: float) -> None:
        self._openaikey = openai_key
        self._prompt = prompt
        self._model = model
        self._temperature = temperature


    def get_response(self) -> str:
        """Get response from a given prompt.
        
        :return: Processed response through model.
        """
        openai.api_key =self._openaikey
        messages = [{"role": "user", "content": self._prompt}]
        response = openai.chat.completions.create(
                            model=self._model,
                            messages=messages,
                            temperature=self._temperature,
                        )
        response = response.choices[0].message.content.strip()
        return response