from fastapi import APIRouter, status

router = APIRouter()


@router.get("/health", status_code=status.HTTP_204_NO_CONTENT)
async def health_check():
    return None
