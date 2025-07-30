from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException, Path, Depends, status
from fastapi.security import APIKeyHeader

from .auth.auth import get_key_user
from ..repository.electricity_reading_repository import ElectricityReadingRepository
from ..service.electricity_reading_service import ElectricityReadingService
from .models import OPENAPI_EXAMPLES, ElectricReading, Readings


api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)


async def get_api_key(api_key: str = Depends(api_key_header)):
    user = get_key_user(api_key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key"
        )
    return api_key


repository = ElectricityReadingRepository()
service = ElectricityReadingService(repository)

router = APIRouter(prefix="/readings", tags=["Readings"])


@router.post(
    "/store",
    dependencies=[Depends(get_api_key)],
    response_model=ElectricReading,
    description="Store Readings",
)
def store(data: ElectricReading):
    service.store_reading(data.model_dump(mode="json"))
    return data


@router.get(
    "/read/{smart_meter_id}",
    response_model=List[Readings],
    description="Get Stored Readings",
)
def read(smart_meter_id: str = Path(openapi_examples=OPENAPI_EXAMPLES)):
    readings = service.retrieve_readings_for(smart_meter_id)
    if len(readings) < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No readings found")
    else:
        return [r.to_json() for r in readings]
