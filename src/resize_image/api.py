import logging
import os

from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from resize_image.types import ExampleResponse
from resize_image.helpers import handle_file_upload
import io
import base64
# from fastapi.responses import StreamingResponse
from starlette.responses import StreamingResponse
from os import getcwd
from PIL import Image
from rembg import remove
BASEDIR = os.path.dirname(__file__)

if os.environ.get("K_SERVICE"):
    # Setup logging if we're in a cloud run environment
    from google.cloud.logging import Client as LoggingClient

    logging_client = LoggingClient()
    logging_client.setup_logging()

logger = logging.getLogger(__name__)

PATH_FILES = getcwd() + "/"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
@app.get("/example/{exampleValue}", response_model=ExampleResponse)
async def say_hello(exampleValue: str):
    logger.info(f"GET /example/{exampleValue}")
    return ExampleResponse(response_value=exampleValue.upper())

@app.get("/image/{rembg_id}")
async def rembgshow(rembg_id:str,
  response_description="Returns a thumbnail image from a larger image",
  response_class="StreamingResponse",
  responses= {200: {"description": "an image", "content": {"image/png": {}}}}):
    input = Image.open(PATH_FILES + rembg_id, mode="r")
    output = remove(input)
    imgio = io.BytesIO()
    output.save(imgio, 'PNG')
    imgio.seek(0)
    return StreamingResponse(content=imgio, media_type="image/png")
    
# RESIZE IMAGES FOR DIFFERENT DEVICES
def resize_image(filename: str):
    sizes = [{
        "width": 320,
        "height": 320
    }]
    for size in sizes:
            size_defined = size['width'], size['height']
            image = Image.open(PATH_FILES + filename, mode="r")
            image.thumbnail(size_defined)
            output = remove(image)
            imgio = io.BytesIO()
            output.save(imgio, 'JPEG')
            imgio.seek(0)
            return StreamingResponse(content=imgio, media_type="image/jpeg")
            # output.save(PATH_FILES + str(size['height']) + "_" + filename)

            print("success")


@app.post("/upload/file")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # SAVE FILE ORIGINAL
    with open(PATH_FILES + file.filename, "wb") as myfile:
            content = await file.read()
            myfile.write(content)
            myfile.close()
    # RESIZE IMAGES
    background_tasks.add_task(resize_image, filename=file.filename)
    return JSONResponse(content={"message": "success"})

"""
@app.post(
    "/image/remove_bg",
    tags=["upload and remove bg"],
    description="Upload, remove BG, return PNG",
    response_description="Returns a 320*320 image without background",
    response_class="StreamingResponse",
    responses= {200: {"description": "an image", "content": {"image/png": {}}}}
)
async def upload_remove_bg(
                         image: UploadFile = File(...)
                         ):
    img_dir = os.path.join(BASEDIR, 'statics/media/')                    
    image_, thumb_image = await handle_file_upload(image)
    input = Image.open(os.path.join(img_dir, thumb_image), mode="r")
    output = remove(input)
    imgio = io.BytesIO()
    output.save(imgio, 'PNG')
    imgio.seek(0)
    # print(base64.b64encode(imgio.read()).decode("utf-8"))
    # base64.b64encode(requests.get(url).content)
    # return StreamingResponse(content=imgio, media_type="image/png")
    payload = {
       "mime" : "image/png",
       "image": base64.b64encode(imgio.read()).decode("utf-8"),
       "success": True
    }
    return JSONResponse(content=payload)   

