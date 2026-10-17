import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
app = FastAPI(title="Taxes Fáciles USA", version="2025.1.0")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", include_in_schema=False)
async def home():
    page = STATIC_DIR / "index.html"
    if not page.is_file():
        return JSONResponse({"error": "No se encontró static/index.html"}, status_code=500)
    return FileResponse(page)

@app.get("/health")
async def health():
    return {"status": "ok", "app": "Taxes Fáciles USA", "tax_year": 2025,
            "tax_data_storage": "none", "calculation_location": "browser"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
