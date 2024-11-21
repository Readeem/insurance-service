import uvicorn
from fastapi import FastAPI
from routes.insurance import router as insurance_router

app = FastAPI()
app.include_router(insurance_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
