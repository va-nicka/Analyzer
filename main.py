from fastapi import FastAPI, UploadFile, HTTPException
from fastapi_utils.tasks import repeat_every

from database import init_database, insert_image, fetch_image, fetch_images_by_state, update_analysis_state
from image_analysis import ImageAnalysisState, analyze
from image_repository import save_image, load_image

database = "data.db"
init_database(database)

app = FastAPI()


@app.post("/images")
async def upload_image(file: UploadFile, marker_id: str, marker_lane: int, number_of_lanes: int):
    path = await save_image(file)
    image_id = insert_image(database, path, ImageAnalysisState.TO_ANALYZE, marker_id, marker_lane, number_of_lanes)
    return {"id": f"{image_id}"}


@app.get("/images/{image_id}/status")
async def get_analysis_status(image_id: str):
    image = fetch_image(database, image_id)
    return {"status": f"{image.state}"}


@app.get("/images/{image_id}")
async def get_image(image_id: str):
    image = fetch_image(database, image_id)

    if image is None:
        raise HTTPException(status_code=404, detail="Item not found")

    file = load_image(image.path)

    if image is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return file


@app.on_event("startup")
@repeat_every(seconds=10)
async def analyze_images() -> None:
    images = fetch_images_by_state(database, ImageAnalysisState.TO_ANALYZE)

    for image in images:
        update_analysis_state(database, image.image_id, ImageAnalysisState.IN_PROGRESS)

    for image in images:
        await analyze(image)
        update_analysis_state(database, image.image_id, ImageAnalysisState.FINISHED)
