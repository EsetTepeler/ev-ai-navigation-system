import uvicorn
import sys
import os
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Add project root to path for data access
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
import logging
from dotenv import load_dotenv
from typing import Dict, Any, Optional, Union
from pydantic import BaseModel, ValidationError

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import services
from services.database_service import DatabaseService
from services.redis_service import RedisService
from services.ai_conversation_handler import AIConversationHandler
from services.charging_station_service import ChargingStationService

# Import routes - import only what we need to avoid dependency issues
try:
    from routes import vehicles

    VEHICLES_ROUTE_AVAILABLE = True
except Exception as e:
    logger.warning(f"Vehicles route not available: {e}")
    VEHICLES_ROUTE_AVAILABLE = False

try:
    from routes import charging

    CHARGING_ROUTE_AVAILABLE = True
except Exception as e:
    logger.warning(f"Charging route not available: {e}")
    CHARGING_ROUTE_AVAILABLE = False

# Disable navigation route due to dependency issues
NAVIGATION_ROUTE_AVAILABLE = False
logger.info("Navigation route disabled (using inline endpoints instead)")

# Import error handling
from src.exceptions.custom_exceptions import EVNavigationException
from src.middleware.error_handlers import (
    ev_navigation_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
    http_exception_handler,
)

# Qdrant service removed - no longer needed for this project

# Initialize services
database_service = DatabaseService()
redis_service = RedisService()
ai_service = AIConversationHandler()
charging_station_service = ChargingStationService()


# Pydantic models
class ChatMessage(BaseModel):
    message: str


class VehicleSearchQuery(BaseModel):
    query: str


class RouteRequest(BaseModel):
    start_location: str
    destination: str
    vehicle_model: str


class SimpleRouteRequest(BaseModel):
    start_lat: float
    start_lon: float
    end_lat: float
    end_lon: float
    vehicle_range_km: int
    battery_capacity_kwh: float
    current_battery_percent: float = 80.0
    min_charge_percent: float = 20.0
    preferred_charge_percent: float = 80.0


# Create FastAPI app
app = FastAPI(
    title="EV Navigation API",
    version="2.0",
    description="Electric Vehicle Navigation System with AI-powered route planning",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
# Production: Sadece belirli origin'lere izin ver
# Development: Frontend dev server için localhost:5173, 5174
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:5174,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:5174",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # React dev server + production domains
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

logger.info(f" CORS enabled for origins: {ALLOWED_ORIGINS}")

# ==================== Register Exception Handlers ====================

# Custom exception handler for all EV Navigation exceptions
app.add_exception_handler(EVNavigationException, ev_navigation_exception_handler)

# Validation error handlers (Pydantic)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)

# HTTP exception handler
app.add_exception_handler(HTTPException, http_exception_handler)

# Catch-all for unhandled exceptions
app.add_exception_handler(Exception, generic_exception_handler)

logger.info("Global exception handlers registered")

# ==================== Register API Routes ====================
if VEHICLES_ROUTE_AVAILABLE:
    app.include_router(vehicles.router, prefix="/api/vehicles", tags=["Vehicles"])
    logger.info(" Vehicles routes registered")

if CHARGING_ROUTE_AVAILABLE:
    app.include_router(
        charging.router, prefix="/api/charging", tags=["Charging Stations"]
    )
    logger.info(" Charging routes registered")

# Navigation route is disabled - using inline endpoints instead
# if NAVIGATION_ROUTE_AVAILABLE:
#     app.include_router(navigation.router, prefix="/api/navigation", tags=["Navigation"])
#     logger.info(" Navigation routes registered")

logger.info("API routes registration complete")


# Root endpoint
@app.get("/")
async def root():
    return {"name": " EV Navigation API", "version": "2.0", "status": "active"}


@app.get("/test-endpoint-12345")
async def test_endpoint():
    """Test endpoint to verify registration"""
    return {"message": "Test endpoint works!"}


# Database test endpoint
@app.get("/api/test-db")
async def test_database():
    """Test database connection with proper error handling"""
    try:
        return await database_service.test_connection()
    except Exception as e:
        from src.exceptions.custom_exceptions import DatabaseException

        raise DatabaseException(
            message="Failed to connect to database", details={"error": str(e)}
        )


@app.get("/api/redis-status")
async def get_redis_status():
    """Get Redis connection status with error handling"""
    try:
        return await redis_service.get_connection_status()
    except Exception as e:
        from src.exceptions.custom_exceptions import RedisException

        raise RedisException(
            message="Failed to get Redis status", details={"error": str(e)}
        )


@app.get("/api/vehicles-db")
async def get_vehicles_from_db():
    """Get all vehicles from database with Redis caching"""
    # Check cache first
    cached_vehicles = await redis_service.get_cached_vehicles()
    if cached_vehicles:
        return cached_vehicles

    # Get from database
    vehicles = await database_service.get_all_vehicles()

    # Cache result (await the async method)
    await redis_service.cache_vehicles(vehicles, expire_minutes=10)

    return vehicles


@app.get("/api/charging-stations")
async def get_charging_stations():
    return await database_service.get_charging_stations()


@app.post("/api/plan-route")
async def plan_route(request: RouteRequest):
    """Plan route with validation and error handling"""
    try:
        # Validate inputs
        if not request.start_location or len(request.start_location.strip()) == 0:
            from src.exceptions.custom_exceptions import ValidationException

            raise ValidationException(
                message="Start location cannot be empty", field="start_location"
            )

        if not request.destination or len(request.destination.strip()) == 0:
            from src.exceptions.custom_exceptions import ValidationException

            raise ValidationException(
                message="Destination cannot be empty", field="destination"
            )

        # Mock route planning (replace with actual implementation)
        return {
            "start": request.start_location,
            "destination": request.destination,
            "vehicle": request.vehicle_model,
            "status": "calculated",
            "distance_km": 25.5,
            "time_minutes": 35,
        }
    except ValidationException:
        raise  # Re-raise validation exceptions
    except Exception as e:
        from src.exceptions.custom_exceptions import RouteCalculationException

        raise RouteCalculationException(
            message="Failed to calculate route", details={"error": str(e)}
        )


@app.post("/api/navigation/simple-route")
async def calculate_simple_route(request: SimpleRouteRequest):
    """Calculate route with charging stops based on vehicle range"""
    try:
        import math
        import requests

        # Extract parameters
        start_lat = request.start_lat
        start_lon = request.start_lon
        end_lat = request.end_lat
        end_lon = request.end_lon
        vehicle_range_km = request.vehicle_range_km
        battery_capacity_kwh = request.battery_capacity_kwh
        current_battery_percent = request.current_battery_percent
        min_charge_percent = request.min_charge_percent

        # Haversine distance calculation
        def haversine_distance(lat1, lon1, lat2, lon2):
            R = 6371
            lat1_rad = math.radians(lat1)
            lat2_rad = math.radians(lat2)
            delta_lat = math.radians(lat2 - lat1)
            delta_lon = math.radians(lon2 - lon1)
            a = (
                math.sin(delta_lat / 2) ** 2
                + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
            )
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            return R * c

        total_distance = haversine_distance(start_lat, start_lon, end_lat, end_lon)
        usable_range_km = (
            vehicle_range_km * (current_battery_percent - min_charge_percent) / 100
        )

        logger.info(
            f"Route: {total_distance:.1f}km, Range: {vehicle_range_km}km, Usable: {usable_range_km:.1f}km"
        )

        # Get charging stations
        all_stations = charging_station_service.get_all_stations()

        # Find stations along route
        def is_station_near_route(station, corridor_width_km=100):
            try:
                station_lat = float(station.get("latitude", 0))
                station_lon = float(station.get("longitude", 0))
                dist_to_start = haversine_distance(
                    start_lat, start_lon, station_lat, station_lon
                )
                dist_to_end = haversine_distance(
                    station_lat, station_lon, end_lat, end_lon
                )
                deviation = abs((dist_to_start + dist_to_end) - total_distance)
                return deviation < corridor_width_km
            except:
                return False

        route_stations = []
        for station in all_stations:
            if is_station_near_route(station):
                station_lat = float(station.get("latitude", 0))
                station_lon = float(station.get("longitude", 0))
                dist_from_start = haversine_distance(
                    start_lat, start_lon, station_lat, station_lon
                )
                route_stations.append(
                    {"station": station, "distance_from_start": dist_from_start}
                )

        route_stations.sort(key=lambda x: x["distance_from_start"])

        # Calculate charging stops
        charging_stops = []
        if total_distance > usable_range_km:
            current_position = 0
            stop_count = 0
            max_stops = 5

            while (
                current_position + usable_range_km < total_distance
                and stop_count < max_stops
            ):
                target_distance = current_position + (usable_range_km * 0.85)
                best_station = None
                best_diff = float("inf")

                for station_data in route_stations:
                    dist = station_data["distance_from_start"]
                    if current_position < dist <= current_position + usable_range_km:
                        diff = abs(dist - target_distance)
                        if diff < best_diff:
                            best_diff = diff
                            best_station = station_data

                if best_station:
                    station = best_station["station"]
                    station_distance = best_station["distance_from_start"]
                    charging_stops.append(
                        {
                            "station_id": station.get("id"),
                            "name": station.get("name", "Şarj İstasyonu"),
                            "latitude": float(station.get("latitude", 0)),
                            "longitude": float(station.get("longitude", 0)),
                            "power_kw": station.get("power_kw", 50),
                            "distance_from_start_km": round(station_distance, 1),
                            "charging_time_minutes": int(
                                (battery_capacity_kwh * 0.7)
                                / (station.get("power_kw", 50) / 60)
                            ),
                        }
                    )
                    current_position = station_distance
                    stop_count += 1
                else:
                    break

        # OSRM routing
        route_coordinates = []
        try:
            waypoints = [(start_lon, start_lat)]
            for stop in charging_stops:
                waypoints.append((stop["longitude"], stop["latitude"]))
            waypoints.append((end_lon, end_lat))

            waypoints_str = ";".join([f"{lon},{lat}" for lon, lat in waypoints])
            osrm_url = (
                f"http://router.project-osrm.org/route/v1/driving/{waypoints_str}"
            )
            osrm_response = requests.get(
                osrm_url,
                params={"overview": "full", "geometries": "geojson"},
                timeout=15,
            )

            if osrm_response.status_code == 200:
                osrm_data = osrm_response.json()
                if osrm_data.get("routes"):
                    route = osrm_data["routes"][0]
                    geometry = route["geometry"]["coordinates"]
                    route_coordinates = [[coord[1], coord[0]] for coord in geometry]
                    total_distance = route["distance"] / 1000
        except Exception as e:
            logger.warning(f"OSRM failed: {e}")

        # Fallback to straight line
        if not route_coordinates:
            route_coordinates = [[start_lat, start_lon]]
            for stop in charging_stops:
                route_coordinates.append([stop["latitude"], stop["longitude"]])
            route_coordinates.append([end_lat, end_lon])

        # Calculate time and cost
        avg_speed_kmh = 80
        driving_time_minutes = int((total_distance / avg_speed_kmh) * 60)
        total_charging_time = sum(
            stop.get("charging_time_minutes", 30) for stop in charging_stops
        )
        total_time_minutes = driving_time_minutes + total_charging_time
        energy_needed_kwh = (total_distance / vehicle_range_km) * battery_capacity_kwh
        estimated_cost_tl = energy_needed_kwh * 0.40

        return {
            "success": True,
            "route_coordinates": route_coordinates,
            "charging_stops": charging_stops,
            "route_summary": {
                "total_distance_km": round(total_distance, 1),
                "driving_time_minutes": driving_time_minutes,
                "charging_time_minutes": total_charging_time,
                "total_time_minutes": total_time_minutes,
                "num_charging_stops": len(charging_stops),
                "estimated_cost_tl": round(estimated_cost_tl, 2),
                "energy_needed_kwh": round(energy_needed_kwh, 1),
            },
            "start_point": {"latitude": start_lat, "longitude": start_lon},
            "end_point": {"latitude": end_lat, "longitude": end_lon},
        }

    except Exception as e:
        logger.error(f"Route calculation error: {e}")
        from src.exceptions.custom_exceptions import RouteCalculationException

        raise RouteCalculationException(
            message="Rota hesaplanamadı", details={"error": str(e)}
        )


@app.post("/api/ai-chat")
async def ai_chat(chat_request: ChatMessage):
    """AI chat endpoint with error handling and context"""
    try:
        if not chat_request.message or len(chat_request.message.strip()) == 0:
            from src.exceptions.custom_exceptions import ValidationException

            raise ValidationException(
                message="Message cannot be empty", field="message"
            )

        # Fetch vehicle and charging station context for AI
        vehicles_response = await database_service.get_all_vehicles(limit=30)
        vehicles_list = (
            vehicles_response.get("vehicles", [])
            if isinstance(vehicles_response, dict)
            else []
        )

        # Get charging stations
        charging_stations = charging_station_service.get_all_stations()

        # Create context for AI
        context = {
            "vehicles": vehicles_list,
            "charging_stations": charging_stations,
            "total_vehicles": len(vehicles_list),
            "total_stations": len(charging_stations),
        }

        return await ai_service.chat_with_context(chat_request.message, context)
    except ValidationException:
        raise  # Re-raise validation exceptions
    except Exception as e:
        from src.exceptions.custom_exceptions import AIServiceException

        raise AIServiceException(message="AI service error", details={"error": str(e)})


@app.post("/api/smart-vehicle-search")
async def smart_vehicle_search(search_query: VehicleSearchQuery):
    vehicles_response = await database_service.get_all_vehicles(limit=20)
    # Extract vehicles list from response
    vehicles_list = (
        vehicles_response.get("vehicles", [])
        if isinstance(vehicles_response, dict)
        else []
    )
    return ai_service.smart_vehicle_search(search_query.query, vehicles_list)


if __name__ == "__main__":
    uvicorn.run("orchestrator:app", host="0.0.0.0", port=8000, reload=False)
