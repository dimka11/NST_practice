from fastapi import FastAPI, File, UploadFile, Form
from typing import Optional, List
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from nst import make_style_transfer


app = FastAPI(debug=True)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/checkfile")
def check_file():
    return {"status": "File not ready"}


@app.get("/downloadfile/")
def download_file():
    file_path = 'uploads/final_image.jpg'
    make_style_transfer('uploads/content.jpg', 'uploads/style.jpg', 0.75, 'uploads/final_image.jpg')
    return FileResponse(path=file_path, filename=file_path, media_type='image/jpg')


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/html/", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title></title>
        </head>
        <body>
        </body>
    </html>
    """


def save_file(filename, data):
    with open('uploads/'+filename, 'wb') as f:
        f.write(data)


@app.post("/upload_files")
async def upload(name: str = Form(...), files: List[UploadFile] = File(...)):
    print(name)
    for idx, file in enumerate(files):
        contents = await file.read()
        file_name = file.filename
        if idx == 0:
            save_file("content.jpg", contents)
        else:
            save_file("style.jpg", contents)

    return {"Uploaded Filenames": [file.filename for file in files]}

# @app.post("/upload")
# async def upload(file: UploadFile = File(...)):
#     print('request ')
#     contents = await file.read()
#     save_file(file.filename, contents)
#     return {"Filename": file.filename}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
