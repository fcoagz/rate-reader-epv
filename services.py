import os
import re
from PIL import Image
from pydantic_ai import Agent, BinaryContent
from pydantic_ai.models.gemini import GeminiModel
import pytesseract

from models import ImageValidation, ImageRequest
from config import SYSTEM_PROMPT, EXPECTED_PLATFORMS, EXPECTED_CURRENCIES
from utils import validate_image_content

class OpenAIService(Agent):
    def __init__(self, **kwargs):
        super().__init__(
            model=GeminiModel('gemini-2.0-flash', api_key=os.getenv('GEMINI_AI_TOKEN')),
            result_type=ImageValidation,
            system_prompt=SYSTEM_PROMPT,
            **kwargs
        )

    async def validate(self, data: ImageRequest = None) -> ImageValidation:
        try:
            response = await self.run([
                'What is the type of the image?',
                BinaryContent(
                    data.file.read(),
                    media_type='image/png')
            ])

            return response.data
        except Exception as e:
            raise ValueError(f"Failed to create prompt result: {e}")

def get_image_content(type: str, image: Image.Image, boxes: list[tuple[int, int, int, int]]) -> list[dict]:
    content = []
    for i, box in enumerate(boxes):
        cropped_image = image.crop(box)
        cropped_image = cropped_image.convert('L')  # Convert to grayscale255, '1')  # Convert to black and white
        text = pytesseract.image_to_string(cropped_image, lang='eng', config='--psm 6 --oem 3')

        if type == 'image-1':
            match = re.search(r'\b\d{1,3}(?:\.\d{3})*(?:,\d{2})\b', text)
            if i == 0 and match:
                content.append({
                    'platform': '@EnParaleloVzla3',
                    'rates': float(match.group().replace(',', '.'))
                })
            else:
                rate = validate_image_content(text, EXPECTED_PLATFORMS)
                if rate:
                    content.append(rate)
        elif type == 'image-2':
            match = re.search(r'\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?', text)
            if match:
                rate_str = match.group().replace('.', '').replace(',', '.')
                try:
                    rate = float(rate_str)
                    for currency in EXPECTED_CURRENCIES:
                        if currency not in [item['platform'] for item in content]:
                            content.append({
                                'platform': currency,
                                'rate': rate
                            })
                            break
                except ValueError:
                    pass

    return content