import logging
import os

import base64

from fastapi import FastAPI, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from resize_image.types import ExampleResponse
from resize_image.helpers import handle_file_upload, remove_background


from os import getcwd


templates = Jinja2Templates(directory="templates")

BASEDIR = os.path.dirname(__file__)

if os.environ.get("K_SERVICE"):
    # Setup logging if we're in a cloud run environment
    from google.cloud.logging import Client as LoggingClient

    logging_client = LoggingClient()
    logging_client.setup_logging()

logger = logging.getLogger(__name__)

PATH_FILES = getcwd() + "/"

description = """
Image Remove Background API
## Users
You will be able to:
* **Upload an image and get back a 320 X 320 image without the background** 
"""

app = FastAPI(
    title="RemoveBackground",
    description=description,
    version="0.0.1",
    contact={
        "name": "Daniel VALIDE",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/image/remove_bg",
        tags=["Upload Resize Remove Background"],
        description="Upload Resize Remove Background return PNG",
        response_description="Returns a base64 image data",
        response_class=ORJSONResponse,
        responses={200: {"description": "an base 64 encoded image", "content": {"application/json": {}}}}
)
async def upload_remove_bg(
    image: UploadFile | None = None
):
    if not image:
        payload = {
            "mime": "image/png",
            "image": "",
            "success": False
        }
    else:
        img_dir, thumb_image = await handle_file_upload(image)
        base64_image = await remove_background(img_dir, thumb_image)

        payload = {
            "mime": "image/png",
            "image": base64.b64encode(base64_image.read()).decode("utf-8"),
            "success": True
        }
    return ORJSONResponse(content=payload)

# STEP 1 - HOMEPAGE DISPLAY ALL DATA FUNCTION - WORKING
@app.get("/", response_class=HTMLResponse)
def read_notes(request: Request, skip: int = 0, limit: int = 100):
    notes = []
    return templates.TemplateResponse("index.html", {
        "request": request,
        "notes": notes,
    })
    