from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
import io

app = FastAPI()

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # Open the uploaded image file
    image = Image.open(file.file)
    
    # Process the image (if needed)
    # For now, we just return the uploaded image
    processed_image = image

    # Save the image to an in-memory buffer
    img_io = io.BytesIO()
    processed_image.save(img_io, 'JPEG')
    img_io.seek(0)

    # Return the image as a StreamingResponse
    return StreamingResponse(img_io, media_type="image/jpeg")

# To run the app, use:
# uvicorn filename:app --reload
