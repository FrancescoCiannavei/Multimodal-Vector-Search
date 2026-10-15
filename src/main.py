import json
import logging
from typing import Annotated

from fastapi import FastAPI, Query, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from seed import seed
from retrive import retrive

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/api/health")
def health():
    return {"status": "ok"}

#! Warning, for production enviroments you might want to protect this route.
# Using the files query param you can easly seed new content without truncating the table and seeding one more time
# Example: /api/seed?files=data/text/coffee.txt&files=data/text/chess.txt
@app.get("/api/seed")
def run_seed(files: Annotated[list[str] | None, Query()] = None):
    def events():
        try:
            for event in seed(files):
                yield json.dumps(event) + "\n"
        except Exception as e:
            logger.exception("Seeding failed")
            yield json.dumps({"event": "error", "message": f"Seeding failed: {e}", "success": False}) + "\n"

    return StreamingResponse(
        events(),
        media_type="text/plain",
        headers={"X-Content-Type-Options": "nosniff"},
    )

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
    return FileResponse("public/html/query.html")

@app.get("/seed")
def seed_page():
    return FileResponse("public/html/seed.html")

# Routes above take priority, so the static mount must come last
app.mount("/", StaticFiles(directory="public", follow_symlink=True), name="public")
