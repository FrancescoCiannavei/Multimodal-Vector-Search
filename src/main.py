import logging

from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from seed import seed
from retrive import retrive

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/api/health")
def health():
    return {"status": "ok"}

#! Warning, for production enviroments you might want to protect this route.
@app.get("/api/seed")
def run_seed():
    try:
        count = seed()
    except Exception as e:
        logger.exception("Seeding failed")
        return JSONResponse(
            status_code=500,
            content={"message": f"Seeding failed: {e}", "success": False},
        )
    return {"message": f"Seeded {count} files", "success": True}

@app.get("/api/retrive")
def run_retrive(q):
    results = retrive(q, 10)
    print(results)
    return {
        "query": q,
        "results": results
	}

@app.get("/")
def index():
    return FileResponse("public/html/index.html")

# Routes above take priority, so the static mount must come last
app.mount("/", StaticFiles(directory="public", follow_symlink=True), name="public")
