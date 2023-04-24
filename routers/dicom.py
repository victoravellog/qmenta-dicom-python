import base64
import matplotlib.pyplot as plt
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from pydicom import dcmread

app = APIRouter()


async def check_file_type(file):
    if file.content_type != "application/dicom" and file.content_type != "application/octet-stream":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="File not valid")

    return file


async def analize_file_input(in_file: UploadFile):
    file_location = f"files/{in_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(in_file.file.read())
    ds = dcmread(file_location)

    return ds


@app.post("/data/patient_name")
async def analize_name(file: UploadFile | None = None):
    await check_file_type(file)
    ds = await analize_file_input(file)

    return {"patientName": str(ds.PatientName)}


@app.post("/data/slice_image")
async def analize_image(file: UploadFile | None = None):
    await check_file_type(file)
    ds = await analize_file_input(file)

    pixel_array = ds.pixel_array
    plt.imshow(pixel_array, cmap=plt.cm.bone)
    filename, ext = file.filename.split(".")
    plt.savefig(f"static/{filename}.png")
    encoded_file = base64.b64encode(
        open(f"static/{filename}.png", "rb").read())
    return {"image": encoded_file}
