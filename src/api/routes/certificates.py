import os
import uuid
import aiofiles
import openpyxl
from datetime import datetime
from typing import Annotated
from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile

from src.schemas.certificate import SCertificateAdd
from src.services.certificate import CertificateService
from src.api.depends import certificate_service

router = APIRouter(
    prefix="/certificates",
    tags=["Certificates"],
)


@router.get("")
async def home():
    return ""


@router.get("/summary")
async def getSummary(
    certificate_service: Annotated[CertificateService, Depends(certificate_service)],
):
    return await certificate_service.getAll()


@router.post("/loadxlsx")
async def updateDatabaseByXlsx(
    uploaded_file: UploadFile,
    certificate_service: Annotated[CertificateService, Depends(certificate_service)],
):
    upload_folder_path = Path(__file__).resolve().parent.parent.parent.parent
    path_to_file = Path(
        upload_folder_path, "upload_files", f"{uuid.uuid4()}.{uploaded_file.filename.split('.')[-1]}"
    )
    with open(path_to_file, "wb") as f:
        f.write(uploaded_file.file.read())

    wb_obj = openpyxl.load_workbook(path_to_file)
    sheet_obj = wb_obj.active
    for i in range(2, sheet_obj.max_row):
        cert_center = sheet_obj.cell(row=i, column=1).value
        fio = sheet_obj.cell(row=i, column=2).value
        post = sheet_obj.cell(row=i, column=3).value
        organization = sheet_obj.cell(row=i, column=4).value
        expire_date = sheet_obj.cell(row=i, column=5).value
        if isinstance(expire_date, str):
            expire_date = datetime.strptime(expire_date, "%d.%m.%Y").date()
        status = sheet_obj.cell(row=i, column=6).value
        comment = sheet_obj.cell(row=i, column=7).value

        scsc = SCertificateAdd(
            cert_center=cert_center,
            fio=fio,
            post=post,
            organization=organization,
            expire_date=expire_date,
            status=status,
            comment=str(comment),
        )
        await certificate_service.create(scsc)
    os.remove(path_to_file)

    return {"status": "upload"}

