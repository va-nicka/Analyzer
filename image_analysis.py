import asyncio
from enum import Enum

from fastapi import UploadFile

from database import Image
from image_repository import save_image


class ImageAnalysisState(Enum):
    TO_ANALYZE = "to_analyze"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


async def analyze(image: Image):
    print("analyzing images")
    await asyncio.sleep(10)
    return image

async def analyze_inner():
    pass
