import os
from http import HTTPStatus
from quart import Quart
from quart_schema import QuartSchema, DataSource, Info, validate_request, validate_response
from dotenv import load_dotenv

from models import ImageRequest, ImageResponse, ImageError
from services import get_image_content, OpenAIService
from config import BOXES_IMAGE_1, BOXES_IMAGE_2
from utils import Image

# Load environment variables
load_dotenv()

app = Quart(__name__)
QuartSchema(app, info=Info(title="Image Reader API from pyDolarVenezuela", version="1.0", description="API para leer imágenes y extraer información financiera de EnParaleloVzla"))

@app.post('/api/reader')
@validate_request(ImageRequest, source=DataSource.FORM_MULTIPART)
@validate_response(ImageResponse, HTTPStatus.OK)
@validate_response(ImageError, HTTPStatus.BAD_REQUEST)
async def reader_img(data: ImageRequest):
    try:
        if not data.type_img in ['image-1', 'image-2', 'null', None]:
            raise ValueError("Invalid type_img value")

        if not data.type_img or data.type_img not in ['image-1', 'image-2']:
            if not os.getenv('GEMINI_AI_TOKEN'):
                raise ValueError("GEMINI_AI_TOKEN is not defined")

            agent = OpenAIService()
            response = await agent.validate(data)

            if response.value in ['image-1', 'image-2']:
                image = Image.open(data.file)
                result = get_image_content(response.value, image, BOXES_IMAGE_1) if response.value == 'image-1' else get_image_content(response.value, image, BOXES_IMAGE_2)
        else:
            image = Image.open(data.file)
            result = get_image_content(data.type_img, image, BOXES_IMAGE_1) if data.type_img == 'image-1' else get_image_content(data.type_img, image, BOXES_IMAGE_2)

        return ImageResponse(content=result), HTTPStatus.OK
    except Exception as e:
        return ImageError(error=str(e)), HTTPStatus.BAD_REQUEST

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=14924)