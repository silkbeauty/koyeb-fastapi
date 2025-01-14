from fastapi import APIRouter, HTTPException, Request
from app.services import s_files

router = APIRouter()
@router.get('/test')
async def root(): return {"xAIBooks": "New View Step by Step a, FastAPI!"}


@router.get('/filenames')
def list_files_endpoint(folder_name: str):
    try:
        files = s_files.get_filename_from_folder(folder_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Folder not found")
    return files


@router.get('/save_booknames_to_mongo')
async def save_names_to_mongo(request: Request, folder_name: str):
    try:
        files = s_files.get_filename_from_folder(folder_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Folder not found")
    
    documents = [{"book_name": filename} for filename in files]
    if documents:
        for doc in documents:
            await request.app.state.books_collection.update_one(
                {"book_name": doc["book_name"]}, {"$setOnInsert": doc}, upsert=True
            )


