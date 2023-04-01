from fastapi import APIRouter, Depends

from app.services.station import StationService

router = APIRouter()


@router.get("/station/{station_name}")
def get_station_by_name(
    station_name: str, station_service: StationService = Depends(StationService)
):
    result = station_service.get_station_by_name(station_name=station_name)
    if result is None:
        return {"message": "Bus not found"}
    return result


@router.get("/station/buses/{station_name}")
def get_buses_by_station(
    station_name: str, station_service: StationService = Depends(StationService)
):
    result = station_service.get_buses_by_station(station_name=station_name)
    if result is None:
        return {"message": "Bus stop not found"}
    return result