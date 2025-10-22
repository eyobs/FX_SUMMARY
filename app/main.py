"""
FX Summary Microservice
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import health, summary

app = FastAPI(
    title="FX Summary Microservice",
    description="Minimal FX summary service with Franksher API integration",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(summary.router, tags=["summary"])

@app.get("/")
async def root():
    return {
        "service": "FX Summary Microservice",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "summary": "/summary"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
