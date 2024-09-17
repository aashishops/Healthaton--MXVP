from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from PIL import Image, ImageOps
import numpy as np
import io
import os
from keras.models import load_model

app = FastAPI()

# Define the path to the HTML file
html_file_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# Serve the HTML file at the root URL
@app.get("/", response_class=HTMLResponse)
async def serve_html():
    return FileResponse(html_file_path)

@app.post("/upload")
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
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Prepare the result message
    result = f"Class: {class_name[2:].strip()}, Confidence Score: {confidence_score:.2f}"

    # Optionally, you can return the result as part of the response
    return {"result": result}
