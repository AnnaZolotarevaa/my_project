import requests
from faker import Faker
import random

API_URL_TRANSPORT_TYPE = "http://127.0.0.1:8000/transport-types/"  
API_URL_ROUTE = "http://127.0.0.1:8000/routes/"  
API_URL_PATH = "http://127.0.0.1:8000/paths/"  
NUM_RECORDS = 10
fake = Faker()

TRANSPORT_TYPES = [
    "bus", "trolleybus", "metro", "tram", "taxi", "train"]

def generate_random_transport_data():
    """Генерирует случайные данные для транспорта (TransportType)."""
    return {
        "name": random.choice(TRANSPORT_TYPES),  
        "average_speed": random.randint(20, 120),  
        "fuel_consumption": round(random.uniform(5.0, 20.0), 1),  
        "vehicle_count": random.randint(10, 500),   
    }

def generate_random_route_data(transport_type_id):
    """Генерирует случайные данные для маршрута (Route)."""
    return {
        "route_number": str(random.randint(1, 100)),  
        "daily_passenger_count": random.randint(50, 5000),  
        "fare": round(random.uniform(10, 50), 2),  
        "vehicles_on_route": random.randint(1, 50),  
        "transport_type_id": transport_type_id,
    }

def generate_random_path_data(route_id):
    """Генерирует случайные данные для пути (Path)."""
    return {
        "start_point": fake.city(),  
        "end_point": fake.city(),  
        "stops_count": random.randint(1, 20),  
        "distance": round(random.uniform(5.0, 200.0), 2),  
        "route_id": route_id  
    }

def populate_transport_database():
    """Заполняет базу данных случайными данными о транспорте через API."""
    for _ in range(NUM_RECORDS):
        transport_data = generate_random_transport_data()
        response = requests.post(API_URL_TRANSPORT_TYPE, json=transport_data)
        
        if response.status_code == 200:
            transport_type = response.json()  
            print(f"Тип транспорта '{transport_data['name']}' успешно добавлен.")
            route_data = generate_random_route_data(transport_type['id'])
            response = requests.post(API_URL_ROUTE, json=route_data)
            
            if response.status_code == 200:
                route = response.json()  
                print(f"Маршрут '{route_data['route_number']}' успешно добавлен.")
                path_data = generate_random_path_data(route['id']) 
                response = requests.post(API_URL_PATH, json=path_data)
                
                if response.status_code == 200:
                    print(f"Путь для маршрута '{route['route_number']}' успешно добавлен.")
                else:
                    print(f"Ошибка при добавлении пути: {response.text}")
            else:
                print(f"Ошибка при добавлении маршрута: {response.text}")
        else:
            print(f"Ошибка при добавлении типа транспорта: {response.text}")

if __name__ == "__main__":
    populate_transport_database()
