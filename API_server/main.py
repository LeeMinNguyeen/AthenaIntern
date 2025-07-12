from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import fal_client
import matplotlib.pyplot as plt
import time

app = FastAPI()

# Add CORS middleware to allow public access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from dotenv import load_dotenv
import io
from fastapi.responses import StreamingResponse
from collections import defaultdict

load_dotenv()
os.environ["FAL_KEY"] = os.getenv("FAL_KEY") or ""

# Pydantic model for report chart request
class ReportChartRequest(BaseModel):
    type: List[str]
    status: List[str]

# Update the path to the folder containing images
ASSET_FOLDER = os.path.join(os.path.dirname(__file__), "images", "asset")
BACKGROUND_FOLDER = os.path.join(os.path.dirname(__file__), "images", "background")
CHART_FOLDER = os.path.join(os.path.dirname(__file__), "images", "chart")

@app.get("/images/asset/{image_name}")
def get_asset_image(image_name: str):
    """Serve an image from the 'asset' folder by its name."""
    image_path = os.path.join(ASSET_FOLDER, image_name)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found in 'asset' folder")
    return FileResponse(image_path)

@app.get("/images/background/{image_name}")
def get_background_image(image_name: str):
    """Serve an image from the 'background' folder by its name."""
    image_path = os.path.join(BACKGROUND_FOLDER, image_name)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found in 'background' folder")
    return FileResponse(image_path)

@app.get("/images")
def list_images():
    """List all image names in the 'asset' and 'background' folders."""
    if not os.path.exists(ASSET_FOLDER) or not os.path.exists(BACKGROUND_FOLDER):
        raise HTTPException(status_code=404, detail="One or both image folders not found")

    asset_images = [f"asset/{f}" for f in os.listdir(ASSET_FOLDER) if os.path.isfile(os.path.join(ASSET_FOLDER, f))]
    background_images = [f"background/{f}" for f in os.listdir(BACKGROUND_FOLDER) if os.path.isfile(os.path.join(BACKGROUND_FOLDER, f))]

    images = asset_images + background_images

    return {"images": images}

@app.get("/")
def root():
    return {"message": "Welcome to the Image Server! Use /images/{image_name} to fetch an image."}

@app.post("/generate/image")
def generate_image(prompt: str, output_format: str = "jpg"):
    """Generate an image based on the provided prompt."""
    if output_format == 'jpg':
        output_format = 'jpeg'
    handler = fal_client.submit(
        "fal-ai/flux/dev",
        arguments={
            "prompt": prompt,
            "output_format": output_format,
        },
    )
    result = handler.get()

    return result["images"][0]

@app.post("/generate/video")
def generate_video(prompt: str, image_url: str):
    result = fal_client.subscribe(
        "fal-ai/minimax/hailuo-02/standard/image-to-video",
        arguments={
            "prompt": prompt,
            "image_url": image_url
        },
    )

    return result["video"]

@app.post("/generate/audio")
def generate_audio(prompt: str):
    result = fal_client.subscribe(
        "cassetteai/sound-effects-generator",
        arguments={
            "prompt": prompt,
            "duration": 5
        },
    )

    return result["audio_file"]

@app.get("/chart/{chart_name}")
def get_chart_image(chart_name: str):
    chart_folder = os.path.join(os.path.dirname(__file__), "chart")
    chart_path = os.path.join(chart_folder, chart_name)
    if not os.path.exists(chart_path):
        raise HTTPException(status_code=404, detail="Chart image not found")
    return FileResponse(chart_path)

@app.post("/report/chart")
def report_chart(request: ReportChartRequest):
    # Handle default values
    type_list = request.type if request.type else []
    status_list = request.status if request.status else []

    # Calculate success rate for each type
    type_counts = defaultdict(int)
    success_counts = defaultdict(int)

    for t, s in zip(type_list, status_list):
        type_counts[t] += 1
        if s == "Success":
            success_counts[t] += 1

    types = list(type_counts.keys())
    success_rates = [
        (success_counts[t] / type_counts[t]) * 100 if type_counts[t] > 0 else 0
        for t in types
    ]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(types, success_rates, color="skyblue")
    ax.set_ylabel("Success Rate (%)")
    ax.set_xlabel("Content Type")
    ax.set_title("Success Rate by Content Type")
    ax.set_ylim(0, 100)

    for i, rate in enumerate(success_rates):
        ax.text(i, rate + 2, f"{rate:.1f}%", ha="center")

    # Save chart image in 'chart' folder
    os.makedirs(CHART_FOLDER, exist_ok=True)
    chart_filename = f"chart_{int(time.time())}_{os.getpid()}.png"
    chart_path = os.path.join(CHART_FOLDER, chart_filename)
    plt.savefig(chart_path, format="png")
    plt.close(fig)

    return FileResponse(chart_path)

    # Return link to the saved chart image
    chart_url = f"/chart/{chart_filename}"
    return {"chart_url": chart_url}