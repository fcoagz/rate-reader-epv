from quart_schema.pydantic import File
from pydantic import BaseModel, Field

class ImageValidation(BaseModel):
    value: str | None = Field(None, description="Validates if the image is 'image-1' of 'image-2' that has at least the image to be loaded similar, otherwise it is None")

class ImageRequest(BaseModel):
    file: File = Field(..., description="The image file to be processed")
    type_img: str | None = Field(None, description="Optional type of the image")

class ImageResponse(BaseModel):
    content: list[dict] = Field([], description="The content of the image")

class ImageError(BaseModel):
    error: str = Field(..., description="The error message")

class ExceptionResponse(BaseModel):
    error: str = Field(..., description="The error message")