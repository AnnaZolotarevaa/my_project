from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Base, TransportType, Route, Path
from sqlalchemy import text
from pydantic import BaseModel

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/transport_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TransportTypeCreate(BaseModel):
    name: str
    average_speed: float
    fuel_consumption: float
    vehicle_count: int

class RouteCreate(BaseModel):
    route_number: str
    daily_passenger_count: int
    fare: float
    vehicles_on_route: int
    transport_type_id: int

class PathCreate(BaseModel):
    start_point: str
    end_point: str
    stops_count: int
    distance: float
    route_id: int

@app.post("/transport-types/")
def create_transport_type(transport_type: TransportTypeCreate, db: Session = Depends(get_db)):
    transport_type_db = TransportType(
        name=transport_type.name,
        average_speed=transport_type.average_speed,
        fuel_consumption=transport_type.fuel_consumption,
        vehicle_count=transport_type.vehicle_count
        
    )
    db.add(transport_type_db)
    db.commit()
    db.refresh(transport_type_db)
    return transport_type_db

@app.get("/transport-types/")
def get_transport_types(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(TransportType).offset(skip).limit(limit).all()

@app.put("/transport-types/{transport_type_id}/")
def update_transport_type(transport_type_id: int, transport_type: TransportTypeCreate, db: Session = Depends(get_db)):
    transport_type_db = db.query(TransportType).filter(TransportType.id == transport_type_id).first()
    if not transport_type_db:
        raise HTTPException(status_code=404, detail="Transport type not found")
    
    transport_type_db.name = transport_type.name
    transport_type_db.average_speed = transport_type.average_speed
    transport_type_db.fuel_consumption = transport_type.fuel_consumption
    transport_type_db.vehicle_count = transport_type.vehicle_count

    db.commit()
    db.refresh(transport_type_db)
    return {"message": "Transport type updated successfully", "data": transport_type_db}

@app.get("/transport-types/{transport_type_id}")
def get_transport_type_by_id(transport_type_id: int, db: Session = Depends(get_db)):
    transport_type = db.query(TransportType).filter(TransportType.id == transport_type_id).first()
    if not transport_type:
        raise HTTPException(status_code=404, detail="Transport type not found")
    return transport_type

@app.delete("/transport-types/{transport_type_id}")
def delete_transport_type(transport_type_id: int, db: Session = Depends(get_db)):
    transport_type = db.query(TransportType).filter(TransportType.id == transport_type_id).first()
    if not transport_type:
        raise HTTPException(status_code=404, detail="Transport type not found")
    db.delete(transport_type)
    db.commit()
    return {"message": "Transport type deleted successfully"}

@app.post("/routes/")
def create_route(route: RouteCreate, db: Session = Depends(get_db)):
    route_db = Route(
        route_number=route.route_number,
        daily_passenger_count=route.daily_passenger_count,
        fare=route.fare,
        vehicles_on_route=route.vehicles_on_route,
        transport_type_id=route.transport_type_id
    )
    db.add(route_db)
    db.commit()
    db.refresh(route_db)
    return route_db

@app.get("/routes/")
def get_routes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Route).offset(skip).limit(limit).all()


@app.put("/routes/{route_id}/")
def update_route(route_id: int, route: RouteCreate, db: Session = Depends(get_db)):
    route_db = db.query(Route).filter(Route.id == route_id).first()
    if not route_db:
        raise HTTPException(status_code=404, detail="Route not found")
    
    route_db.route_number = route.route_number
    route_db.daily_passenger_count = route.daily_passenger_count
    route_db.fare = route.fare
    route_db.vehicles_on_route = route.vehicles_on_route
    route_db.transport_type_id = route.transport_type_id

    db.commit()
    db.refresh(route_db)
    return {"message": "Route updated successfully", "data": route_db}


@app.delete("/routes/{route_id}/")
def delete_route(route_id: int, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    db.delete(route)
    db.commit()
    
    return {"message": "Route deleted successfully"}

@app.post("/paths/")
def create_path(path: PathCreate, db: Session = Depends(get_db)):
    path_db = Path(
        start_point=path.start_point,
        end_point=path.end_point,
        stops_count=path.stops_count,
        distance=path.distance,
        route_id=path.route_id
    )
    db.add(path_db)
    db.commit()
    db.refresh(path_db)
    return path_db

@app.get("/paths/")
def get_paths(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Path).offset(skip).limit(limit).all()


@app.get("/routes/{route_id}")
def get_route_with_path(route_id: int, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return {
        "route": route,
        "path": route.path
    }

@app.put("/paths/{path_id}/")
def update_path(path_id: int, path: PathCreate, db: Session = Depends(get_db)):
    path_db = db.query(Path).filter(Path.id == path_id).first()
    if not path_db:
        raise HTTPException(status_code=404, detail="Path not found")
    
    path_db.start_point = path.start_point
    path_db.end_point = path.end_point
    path_db.stops_count = path.stops_count
    path_db.distance = path.distance
    path_db.route_id = path.route_id

    db.commit()
    db.refresh(path_db)
    return {"message": "Path updated successfully", "data": path_db}

@app.get("/paths/{path_id}")
def get_path_by_id(path_id: int, db: Session = Depends(get_db)):
    path = db.query(Path).filter(Path.id == path_id).first()
    if not path:
        raise HTTPException(status_code=404, detail="Path not found")
    return path

@app.delete("/paths/{path_id}")
def delete_path(path_id: int, db: Session = Depends(get_db)):
    path = db.query(Path).filter(Path.id == path_id).first()
    if not path:
        raise HTTPException(status_code=404, detail="Path not found")
    db.delete(path)
    db.commit()
    return {"message": "Path deleted successfully"}

@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).scalar()
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/transport-types/filtered/")
def get_filtered_transport_types(
    min_average_speed: float = None,
    max_fuel_consumption: float = None,
    db: Session = Depends(get_db)
):
    query = db.query(TransportType)
    
    if min_average_speed is not None:
        query = query.filter(TransportType.average_speed >= min_average_speed)
    
    if max_fuel_consumption is not None:
        query = query.filter(TransportType.fuel_consumption <= max_fuel_consumption)
    
    return query.all()

@app.get("/routes/with-transport-type/")
def get_routes_with_transport_type(db: Session = Depends(get_db)):
    query = db.query(Route, TransportType).join(TransportType, Route.transport_type_id == TransportType.id).all()
    return [{"route": route, "transport_type": transport_type} for route, transport_type in query]

@app.put("/routes/{route_id}/update/")
def update_route_passenger_count(route_id: int, new_passenger_count: int, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    if route.daily_passenger_count < new_passenger_count:
        route.daily_passenger_count = new_passenger_count
        db.commit()
        return {"message": "Route updated successfully"}
    else:
        raise HTTPException(status_code=400, detail="New passenger count is less than current count")

@app.get("/routes/group-by-transport-type/")
def group_routes_by_transport_type(db: Session = Depends(get_db)):
    query = db.query(
        TransportType.name, 
        func.avg(Route.fare).label("average_fare")
    ).join(TransportType, Route.transport_type_id == TransportType.id) \
     .group_by(TransportType.name).all()
    
    return [{"transport_type": name, "average_fare": average_fare} for name, average_fare in query]

@app.get("/routes/sorted/")
def get_sorted_routes(
    sort_by: str = "daily_passenger_count",  
    order: str = "asc", 
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    
    valid_fields = {
        "daily_passenger_count": Route.daily_passenger_count,
        "fare": Route.fare
    }
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    
    column = valid_fields[sort_by]
    query = db.query(Route).order_by(column.desc() if order == "desc" else column.asc())
    return query.offset(skip).limit(limit).all()



