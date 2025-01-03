from pydantic import BaseModel

class TransportTypeBase(BaseModel):
    name: str
    average_speed: float
    fuel_consumption: float
    vehicle_count: int

class TransportTypeCreate(TransportTypeBase):
    pass

class TransportTypeResponse(TransportTypeBase):
    id: int

    class Config:
        orm_mode = True

class RouteBase(BaseModel):
    route_number: str
    daily_passenger_count: int
    fare: float
    vehicles_on_route: int
    transport_type_id: int

class RouteCreate(RouteBase):
    pass

class RouteResponse(RouteBase):
    id: int

    class Config:
        orm_mode = True

class PathBase(BaseModel):
    start_point: str
    end_point: str
    stops_count: int
    distance: float
    route_id: int

class PathCreate(PathBase):
    pass

class PathResponse(PathBase):
    id: int

    class Config:
        orm_mode = True