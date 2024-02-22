# -*- coding: utf-8 -*-
"""
Gather article details from the PubMed API
"""
import openai

class GenImager:
    """GenImager used to generate images from a given input prompt."""
    def __init__(self, openai_key: str, prompt: str, model: str) -> None:
        self._openaikey = openai_key
        self._prompt = prompt
        self._model_image = model


    def get_image(self) -> str:
        """Get image using OpenAI generative image models.
        
        :return: URL of the image generated.
        """
        try:
            openai.api_key =self._openaikey
            response = openai.images.generate(
                model=self._model_image,
                prompt= self._prompt,
                size="1024x1024",
                quality="standard",
                n=1,
                )
            image_url = response.data[0].url
            return image_url
        except:
            return ''