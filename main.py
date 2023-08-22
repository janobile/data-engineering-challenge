import uvicorn
from app.config import app_config
from fastapi import FastAPI
from app.routes import router

# Create a FastAPI app instance using the App class
app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    # Run the FastAPI app using uvicorn
    uvicorn.run(app, host=app_config['host'], port=app_config['port'])

