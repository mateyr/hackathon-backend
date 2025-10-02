from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from hackathon_backend.core.db import engine
from hackathon_backend.models.appointment import Appointment
from hackathon_backend.models.doctor import Doctor
from hackathon_backend.models.health_center import HealthCenter
from hackathon_backend.models.patient import Patient
from hackathon_backend.schemas.api_response import ApiResponse
from hackathon_backend.schemas.appoinment import AppointmentCreate, AppointmentGet, AppointmentsResponse, AppointmentUpdate


router = APIRouter(prefix="/appointments", tags=["appointments"])


def get_session():
    with Session(engine) as session:
        yield session


@router.get("/{patiend_id}", response_model=ApiResponse[AppointmentsResponse])
def read_appointments(
    patiend_id: int,
    session: Session = Depends(get_session),
) -> ApiResponse[AppointmentsResponse]:
    
    patient = session.get(Patient, patiend_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    elif patient.is_deleted:
        raise HTTPException(status_code=404, detail="Patient has been deleted")

    statement = select(Appointment).where(Appointment.patient_id == patiend_id)
    appointment = session.exec(statement).all()
    appointments_data = [AppointmentGet.model_validate(u) for u in appointment]

    return ApiResponse(
        success=True,
        data=AppointmentsResponse(appointment=appointments_data),
        message="Appoinments fetched successfully",
    )


@router.post("/", response_model=ApiResponse[AppointmentsResponse])
def create_appointment(
    appointment_in: AppointmentCreate,
    session: Session = Depends(get_session),
) -> ApiResponse[AppointmentsResponse]:
    
    try:

        patient = session.get(Patient, appointment_in.patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        doctor = session.get(Doctor, appointment_in.doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        
        clinic = session.get(HealthCenter, appointment_in.health_center_id)
        if not clinic:
            raise HTTPException(status_code=404, detail="Clinic not found")
        
        appointment = Appointment.model_validate(appointment_in)

        session.add(appointment)
        session.commit()
        session.refresh(appointment)    

        appointment_data = [AppointmentGet.model_validate(appointment)]

        return ApiResponse(
            success=True,
            data=AppointmentsResponse(appointment=appointment_data),
            message="Appoinments fetched successfully",
        )
    
    except HTTPException:
        raise

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.patch("/{appointment_id}", response_model=ApiResponse[AppointmentsResponse])
def update_appointment(
    appointment_id: int,
    appointment_in: AppointmentUpdate,
    session: Session = Depends(get_session),
) -> ApiResponse[AppointmentsResponse]:
    
    try:

        appointment = session.get(Appointment, appointment_id)
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")

        updated_data = appointment_in.model_dump(exclude_unset=True)  
        appointment = Appointment.model_validate(appointment, update=updated_data)

        session.add(appointment)
        session.commit()
        session.refresh(appointment)

        appointment_data = [AppointmentGet.model_validate(appointment)]

        return ApiResponse(
            success=True,
            data=AppointmentsResponse(appointments=appointment_data),
            message="Appointment updated successfully",
        )
    
    except HTTPException:
        raise

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.patch("/{appointment_id}", response_model=AppointmentsResponse[AppointmentGet])
def delete_appointment(
    appointment_id: int,
    session: Session = Depends(get_session),
) -> ApiResponse[AppointmentGet]:

    try:

        appointment = session.get(Appointment, appointment_id)

        if not appointment or appointment.is_deleted:
            raise HTTPException(status_code=404, detail="Appointment not found or already deleted")

        appointment.soft_delete()

        session.add(appointment)
        session.commit()
        session.refresh(appointment)

        appointment_data = [AppointmentGet.model_validate(appointment)]

        return ApiResponse(
            success=True,
            data=AppointmentsResponse(appointment=appointment_data),
            message="Appointment deleted successfully",
        )

    except HTTPException:
        raise

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
