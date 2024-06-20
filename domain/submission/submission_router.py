from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from datetime import datetime
from models import SubmissionModel
from database import get_db
from sqlalchemy.orm import Session
from domain.submission import submission_schema
from domain.submission import submission_crud
from starlette import status
import ftplib
from pathlib import Path
import os

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="",
)


# @router.get("/hello")
# def hello():
#     return {"message": "안녕하세요 파이보"}

@router.get("/register")
def submission_form(request: Request):
    return templates.TemplateResponse("sign-in/index.html", {'request': request})
# return templates.TemplateResponse("register.html", {'request': request})


@router.get("/result")
def submission_form(request: Request):
    return templates.TemplateResponse("result.html", {'request': request})


@router.get("/submission", status_code = status.HTTP_200_OK, response_model = submission_schema.SubmissionGetResult)
def submission_get(
        _db: Session = Depends(get_db),
        username: str = None,
        password: str = None,
        id: int = None
    ):
    _submission_get = {
        'username': username,
        'password': password,
        'id': id
    }
    submission = submission_crud.get_submission_result(db = _db, submission_get = _submission_get)
    return submission
    

@router.post("/submission", status_code = status.HTTP_200_OK, response_model=submission_schema.SubmissionCreateResult)
def submission_create(
        _submission_create: submission_schema.SubmissionCreate,
        _db: Session = Depends(get_db)
    ):
    submission = submission_crud.create_submission(db = _db, submission_create = _submission_create)
    file = open(f'submission_codes/{submission.id}.py', mode = 'w')
    
    file.write(_submission_create.code)
    file.close()

    return submission


@router.patch("/submission", status_code = status.HTTP_200_OK, response_model = submission_schema.SubmissionPatchResult)
def submission_patch(
        _submission_patch: submission_schema.SubmissionPatch,
        _db: Session = Depends(get_db)
    ):
    submission = submission_crud.get_submission(db = _db, submission_patch = _submission_patch)
    submission.status = _submission_patch.status
    submission_crud.update_status(db = _db, submission = submission)

    return submission


@router.get("/new", status_code = status.HTTP_200_OK)
def fetch_new(request: Request, _db: Session = Depends(get_db)):

    submission = submission_crud.get_submitted_submission(db = _db)

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    CODE_PATH = os.path.join(BASE_DIR, f'submission_codes/{submission.id}.py')
    

    # ftp id.py 송신
    session = ftplib.FTP()
    session.connect('0.0.0.0', 21) # 두 번째 인자는 port number
    session.login("test", "test")   # FTP 서버에 접속
    
    uploadfile = open(CODE_PATH, mode='rb') #업로드할 파일 open
    session.encoding='utf-8'
    session.storlines(f'STOR {submission.id}.py', uploadfile) #파일 업로드
    
    uploadfile.close() # 파일 닫기
    
    session.quit() # 서버 나가기
    print('파일전송함')


    if submission:
        submission.status = 'PROCESSING'
        submission_crud.update_status(db = _db, submission = submission)
        return submission.id
    else: 
        raise HTTPException(status_code=500, detail="데이터가 존재하지 않습니다.")
    
# @router.post("/register", response_model = submission_schema.SubmissionCreate)
# def read_root(submission: SubmissionModel, db: Session = Depends(get_db)):
#     submission = SubmissionModel(
#         submission, 
#         created_at = datetime.now(), 
#         updated_at = datetime.now()
#     )
#     db.add(submission)
#     db.commit()
#     return {"submission": submission}

