from fastapi import UploadFile
from fastapi.responses import FileResponse

IMAGES_DIR = "images/"


async def save_image(file: UploadFile) -> str:
    path = f"{IMAGES_DIR}{file.filename}"
    contents = await file.read()

    with open(path, "wb") as f:
        f.write(contents)

    return path


def load_image(path: str) -> FileResponse:
    return FileResponse(path)
