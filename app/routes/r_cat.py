from fastapi import APIRouter, HTTPException
router = APIRouter()

from app.services import s_files

@router.get('/clean_numbering_list_files')
def list_files_endpoint(folder_name: str):
    try:
        files = s_files.clean_files(folder_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Folder not found")
    return files


