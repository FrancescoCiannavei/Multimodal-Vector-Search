import logging

from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from seed import seed

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/search")
def search(q: str):
    return {"query": q, "results": []}

@app.get("/api/seed")
def run_seed():
    try:
        seed()
    except Exception as e:
        logger.exception("Seeding failed")
        return JSONResponse(
            status_code=500,
            content={"message": f"Seeding failed: {e}", "success": False},
        )
    return {"message": "Seeded", "success": True}

@app.get("/")
def index():
    return FileResponse("public/html/index.html")

# Routes above take priority, so the static mount must come last
app.mount("/", StaticFiles(directory="public"), name="public")
