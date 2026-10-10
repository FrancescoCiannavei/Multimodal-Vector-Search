from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/search")
def search(q: str):
    return {"query": q, "results": []}

@app.get("/")
def index():
    return FileResponse("public/html/index.html")

# Routes above take priority, so the static mount must come last
app.mount("/", StaticFiles(directory="public"), name="public")
