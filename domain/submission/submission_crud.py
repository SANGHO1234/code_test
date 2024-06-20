from domain.submission.submission_schema import *
from models import SubmissionModel
from sqlalchemy.orm import Session
from datetime import datetime

def create_submission(db: Session, submission_create: SubmissionCreate):
    submission = SubmissionModel(
        username = submission_create.username,
        password = submission_create.password,
        status = 'SUBMITTED',
        created_at = datetime.now(),
        updated_at = datetime.now()
    )
    db.add(submission)
    db.commit()
    return submission


def get_submission(db: Session, submission_patch: SubmissionPatch):
    submission = db.query(SubmissionModel).get(submission_patch.id)
    return submission


def get_submitted_submission(db: Session):
    submission = db.query(SubmissionModel)   \
                    .filter(SubmissionModel.status == 'SUBMITTED')  \
                    .order_by(SubmissionModel.created_at).first()
    return submission


def get_submission_result(db: Session, submission_get: dict):
    submission = db.query(SubmissionModel)   \
                    .filter(SubmissionModel.username == submission_get['username'], 
                            SubmissionModel.password == submission_get['password'], 
                            SubmissionModel.id == submission_get['id']).one()
    return submission


def update_status(db: Session, submission: SubmissionModel):
    submission.updated_at = datetime.now()
    db.commit()



# def update_status(db: Session, status):
#     submitted_data = db.query(SubmissionModel)   \
#                     .filter(SubmissionModel.status=='SUBMITTED')  \
#                     .order_by(SubmissionModel.created_at.desc).first()
#     return submitted_data