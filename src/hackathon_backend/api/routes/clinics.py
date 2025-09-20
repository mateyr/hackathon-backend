from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from hackathon_backend.core.db import engine
from hackathon_backend.models.clinic import Clinic
from hackathon_backend.models.user import User
from hackathon_backend.schemas.api_response import ApiResponse
from hackathon_backend.schemas.clinic import ClinicGet, ClinicsResponse


router = APIRouter(prefix="/clinics", tags=["clinics"])


def get_session():
    with Session(engine) as session:
        yield session


@router.get("/", response_model=ApiResponse[ClinicsResponse])
def read_clinics(
    session: Session = Depends(get_session),
) -> ApiResponse[ClinicsResponse]:

    statement = select(Clinic)
    clinics = session.exec(statement).all()
    clinics_data = [ClinicGet.model_validate(u) for u in clinics]

    return ApiResponse(
        success=True,
        data=ClinicsResponse(clinics=clinics_data),
        message="Clinics fetched successfully",
    )
