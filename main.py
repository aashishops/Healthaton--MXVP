from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, ImageOps
import numpy as np
import os
from keras.models import load_model
import logging

app = FastAPI()
logging.basicConfig(level=logging.ERROR)

app.mount("/static", StaticFiles(directory="static"), name="static")
# Define the paths to the HTML files
index_html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
upload_html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")  # Same HTML file as / test section

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
with open("labels.txt", "r") as f:
    class_names = f.readlines()

# Serve the index HTML file at the root URL
@app.get("/", response_class=HTMLResponse)
async def serve_index_html():
    return HTMLResponse(open(index_html_path).read())

@app.post("/test")
async def upload_image(file: UploadFile = File(...)):
    # Open the uploaded image file
    image = Image.open(file.file).convert("RGB")

    # Resize the image to 224x224 (as required by your model)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # Convert the image to a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Create the array of the right shape to feed into the Keras model
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    # Predict the class of the image
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]

    # Prepare the result message
    result = f"{class_name}"
    print(result)

    # Return the result as a JSON response
    return {"result": result}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)