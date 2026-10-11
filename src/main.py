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
    return {
        "query": q,
        "results": [
            {
				"id": 1,
				"file": "data/text/chess.txt",
    			"modality": "text",
			},
            {
				"id": 3,
				"file": "data/audio/coffee/coffee-grinder.mp3",
    			"modality": "audio",
			},
		]
	}

@app.get("/")
def index():
    return FileResponse("public/html/index.html")

# Routes above take priority, so the static mount must come last
app.mount("/", StaticFiles(directory="public"), name="public")
