import shutil

from fastapi import APIRouter, Response, UploadFile

from app.tasks.tasks import process_pic

router = APIRouter(prefix="/images", tags=["Upload Images"])


@router.post("/hotels")
async def add_hotel_image(
    response: Response,
    file: UploadFile,
    name: int,
):
    im_path = f"app/static/images/{name}.webp"
    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(im_path)
    response.status_code = 201
