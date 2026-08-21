from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.deps import check_user_authorization
from urllib.parse import quote

router = APIRouter()

@router.get("/generate")
async def generate_image(
    prompt: str = Query(..., description="Prompt to generate image from"),
    width: int = Query(800, description="Image width"),
    height: int = Query(800, description="Image height"),
    current_user: dict = Depends(check_user_authorization) # Require login
):
    """
    Generates an image URL from backend using Pollinations AI based on a text prompt.
    """
    try:
        encoded_prompt = quote(prompt)
        # Using Pollinations AI which provides free and fast AI image generation via URL
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
        return {"success": True, "image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
