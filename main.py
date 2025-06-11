from fastapi import FastAPI, HTTPException
from datetime import datetime
import os

app = FastAPI(
    title="Test FastAPI App",
    description="A minimal FastAPI app for VPS deployment testing",
    version="1.0.0"
)

# Test environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

@app.get("/")
async def root():
    return {
        "message": "Hello from FastAPI on VPS!",
        "timestamp": datetime.now().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "production")
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/info")
async def app_info():
    return {
        "app_name": "FastAPI Test App",
        "version": "1.0.0",
        "python_version": os.sys.version,
        "deployment_time": datetime.now().isoformat()
    }

@app.get("/env-test")
async def test_environment_variables():
    """Test endpoint to check if environment variables are properly set"""
    return {
        "database_url_set": DATABASE_URL is not None,
        "database_url_preview": DATABASE_URL[:20] + "..." if DATABASE_URL else None,
        "api_secret_key_set": API_SECRET_KEY is not None,
        "api_secret_key_length": len(API_SECRET_KEY) if API_SECRET_KEY else 0,
        "debug_mode": DEBUG_MODE,
        "all_env_vars_set": all([DATABASE_URL, API_SECRET_KEY]),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/secure-info")
async def get_secure_info():
    """Endpoint that requires API secret key to be set"""
    if not API_SECRET_KEY:
        raise HTTPException(
            status_code=500, 
            detail="API_SECRET_KEY environment variable not configured"
        )
    
    return {
        "message": "Secure endpoint accessed successfully!",
        "secret_key_configured": True,
        "debug_mode": DEBUG_MODE,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/database-status")
async def database_status():
    """Check database connection status (mock)"""
    if not DATABASE_URL:
        return {
            "status": "not_configured",
            "message": "DATABASE_URL environment variable not set",
            "connected": False
        }
    
    # In a real app, you'd test the actual connection here
    return {
        "status": "configured",
        "message": "Database URL is configured",
        "url_preview": DATABASE_URL[:30] + "..." if len(DATABASE_URL) > 30 else DATABASE_URL,
        "connected": True,  # Mock status
        "timestamp": datetime.now().isoformat()
    }

@app.get("/config-check")
async def configuration_check():
    """Complete configuration check"""
    config_status = {
        "environment": os.getenv("ENVIRONMENT", "production"),
        "debug_mode": DEBUG_MODE,
        "required_vars": {
            "DATABASE_URL": DATABASE_URL is not None,
            "API_SECRET_KEY": API_SECRET_KEY is not None,
        },
        "optional_vars": {
            "DEBUG_MODE": os.getenv("DEBUG_MODE") is not None,
        },
        "configuration_complete": all([DATABASE_URL, API_SECRET_KEY]),
        "timestamp": datetime.now().isoformat()
    }
    
    if not config_status["configuration_complete"]:
        missing_vars = [var for var, isset in config_status["required_vars"].items() if not isset]
        config_status["missing_variables"] = missing_vars
        config_status["setup_instructions"] = "Check GitHub Secrets configuration"
    
    return config_status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)