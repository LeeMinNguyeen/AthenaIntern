# AthenaIntern API Server

This project is a FastAPI-based server for serving and generating images, videos, and audio assets, as well as generating report charts. It is designed to support automation and prompt engineering tasks, providing endpoints for asset management and AI-powered content generation.

## Features
- **Image Serving**: Fetch images from `images/asset` and `images/background` folders via API endpoints.
- **Image Listing**: List all available images in the asset and background folders.
- **AI Image Generation**: Generate images using prompts via the `/generate/image` endpoint.
- **AI Video Generation**: Generate videos from images and prompts via the `/generate/video` endpoint.
- **AI Audio Generation**: Generate audio files from prompts via the `/generate/audio` endpoint.
- **Report Chart Generation**: Generate and serve success rate charts by content type via the `/report/chart` endpoint.
- **CORS Support**: Configured for public API access.

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies (FastAPI, fal_client, matplotlib, python-dotenv, etc.)

## Setup
1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set environment variables**:
   - Create a `.env` file in the root directory.
   - Add your FAL API key:
     ```
     FAL_KEY=your_fal_api_key_here
     ```
4. **Run the server**:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints
### Image Endpoints
- `GET /images/asset/{image_name}`: Fetch asset image by name.
- `GET /images/background/{image_name}`: Fetch background image by name.
- `GET /images`: List all images in asset and background folders.

### Content Generation Endpoints
- `POST /generate/image`: Generate image from prompt.
- `POST /generate/video`: Generate video from image and prompt.
- `POST /generate/audio`: Generate audio from prompt.

### Chart Endpoints
- `POST /report/chart`: Generate and serve a success rate chart by content type.
- `GET /chart/{chart_name}`: Fetch generated chart image by name.

### Root Endpoint
- `GET /`: Welcome message and usage info.

## Folder Structure
- `main.py`: FastAPI server implementation.
- `images/asset/`: Asset images.
- `images/background/`: Background images.
- `images/chart/`: Generated chart images.
- `requirements.txt`: Python dependencies.
- `.env`: Environment variables (not committed).

## Notes
- Ensure your FAL API key is valid for AI-powered endpoints.
- All image, video, and audio generation uses the `fal_client` API.
- Charts are generated using matplotlib and saved in the `images/chart` folder.