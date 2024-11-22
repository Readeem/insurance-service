import os

import uvicorn
from fastapi import FastAPI

from routes.insurance import router as insurance_router
from routes.tariffs import router as tariffs_router

app = FastAPI(
    title="Insurance Service",
    description="Test for SMIT",
    version="1.0.0",
)
app.include_router(insurance_router)
app.include_router(tariffs_router)

if __name__ == "__main__":
    os.system("alembic upgrade head")
    uvicorn.run(app, host="0.0.0.0", port=8000)
