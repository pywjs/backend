# apps/uploads/endpoints.py

from fastapi import APIRouter, UploadFile, File, HTTPException

from apps.uploads.storages import get_storage

router = APIRouter()


@router.post("/upload/")
async def upload(file: UploadFile = File(...)):
    storage = get_storage()
    file_name = file.filename
    try:
        # Generate a unique file name
        await storage.upload_file(file, file_name)
        url = storage.get_url(file_name)
        return {"filename": file_name, "url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
