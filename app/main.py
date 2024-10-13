import logging
from fastapi import FastAPI
from initialize_f1_data import initialize_f1_data
from routes import sample, race_routes, driver_routes, constructor_routes, circuit_routes
from utils.spark_utils import get_spark_session, stop_spark_session
from middleware.xss_protection import XSSProtectionMiddleware
from middleware.cors import add_cors_middleware
from middleware.auth import AuthMiddleware
from routes import auth_routes, admin_routes
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="F1 Race Data API",
    description="API for accessing F1 race data",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI 경로 (기본값)
    redoc_url="/redoc",  # ReDoc 경로 (기본값)
)


# CORS 미들웨어 추가
add_cors_middleware(app)

# XSS 보호 미들웨어 추가
app.add_middleware(XSSProtectionMiddleware)

# 인증 미들웨어 추가
app.add_middleware(AuthMiddleware)

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing Spark session...")
    get_spark_session()  # Initialize Spark session
    logger.info("Initializing F1 data...")
    initialize_f1_data()
    logger.info("F1 data initialization complete.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Stopping Spark session...")
    stop_spark_session()
    logger.info("Spark session stopped.")

# F1 라우트 포함
app.include_router(sample.router, prefix="/api/sample")
app.include_router(race_routes.router, prefix="/api/races")
app.include_router(driver_routes.router, prefix="/api/drivers")
app.include_router(constructor_routes.router, prefix="/api/constructors")
app.include_router(circuit_routes.router, prefix="/api/circuits")
app.include_router(auth_routes.router, prefix="/api/auth")
app.include_router(admin_routes.router, prefix="/api/admin")

@app.get("/")
async def root():
    return {"message": "F1 Race Data API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)