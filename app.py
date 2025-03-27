from fastapi import FastAPI, File, UploadFile
import tensorflow as tf
import numpy as np
import pickle
from PIL import Image
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# ✅ Mount static files correctly (Serve HTML, CSS, and JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load trained model
model = tf.keras.models.load_model("skin_disease_model_v2.h5")

# Load class names
with open("class_names.pkl", "rb") as file:
    class_names = pickle.load(file)

# Function to preprocess image
def preprocess_image(image):
    img = image.resize((128, 128))  # Resize to match model input size
    img = np.array(img) / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# ✅ Home Route (Serves index.html from /static)
@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(open("static/index.html").read())

# ✅ Prediction Route (Allows POST requests)
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("RGB")  # Open uploaded image
    processed_img = preprocess_image(image)  # Preprocess image

    predictions = model.predict(processed_img)
    predicted_class = class_names[np.argmax(predictions)]
    confidence = np.max(predictions)

    return {"predicted_class": predicted_class, "confidence": float(confidence)}


#http://127.0.0.1:8000/static/index.html