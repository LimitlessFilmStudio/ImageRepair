from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
from pathlib import Path
from inference_gfpgan import restore_faces  # GFPGAN 提供的修复方法

app = FastAPI()

UPLOAD_FOLDER = "./uploads/"
RESULT_FOLDER = "./results/"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.post("/repair-photo/")
async def repair_photo(file: UploadFile = File(...)):
    # 保存上传文件
    file_path = Path(UPLOAD_FOLDER) / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 调用 GFPGAN 修复照片
    result_path = Path(RESULT_FOLDER) / f"restored_{file.filename}"
    restore_faces(input_path=str(file_path), output_path=str(result_path))

    # 返回修复后的照片
    return FileResponse(result_path)
