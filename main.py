import io
import json
import logging
from pathlib import Path
import pandas as pd
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from src import DatasetInfo, DatasetStorage, HealthResponse, setup_logging

setup_logging(verbose=True)
logger = logging.getLogger(__name__)

app = FastAPI(title="Data Processing API", version="1.0.0")
storage = DatasetStorage()

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Return the application status and version."""
    response = HealthResponse(status="ok", version="1.0.0")
    return response

@app.post("/upload", response_model=DatasetInfo)
async def upload_dataset(file: UploadFile = File(...)):
    """Read and store a CSV upload."""
    filename = file.filename or ""
    extension = Path(filename).suffix.lower()
    if extension != ".csv":
        logger.warning(f"Unsupported file format: {extension}")
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: {extension}. Only CSV files are permitted"
        )
    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except pd.errors.EmptyDataError:
        logger.warning(f"Uploaded file is empty: {filename}")
        raise HTTPException(
            status_code=400,
            detail="The uploaded CSV is empty",
        )
    except pd.errors.ParserError:
        logger.warning(f"Could not parse CSV file: {filename}")
        raise HTTPException(
            status_code=400,
            detail="The uploaded file could not be read as a CSV",
        )
    except UnicodeDecodeError:
        logger.warning(f"Could not decode file")
        raise HTTPException(
            status_code=400,
            detail="The uploaded file has encoding that cannot be read"
        )

    dataset_id = storage.save(df, filename)
    metadata = storage.get_metadata(dataset_id)
    no_of_rows = metadata["rows"]
    logger.info(
        f"Uploaded dataset: id={dataset_id}, filename={filename}, rows={no_of_rows}"
    )
    response = DatasetInfo(
        id=metadata["id"],
        filename=metadata["filename"],
        rows=metadata["rows"],
        columns=metadata["columns"],
        column_names=metadata["column_names"],
    )
    return response

@app.get("/datasets/{dataset_id}")
def get_dataset(dataset_id: int, limit: int = Query(default=100, ge=1)):
    """Return up to limit rows from a stored dataset."""
    df = storage.get(dataset_id)
    if df is None:
        logger.warning(f"Dataset not found: {dataset_id}")
        raise HTTPException(
            status_code=404,
            detail=f"Dataset not found: {dataset_id}",
        )
    records = json.loads(df.head(limit).to_json(orient="records"))
    total_rows = len(df)
    returned_rows = len(records)
    logger.info(f"Retrieved dataset: id={dataset_id}, returned_rows={returned_rows}")
    response = {}
    response["id"] = dataset_id
    response["data"] = records
    response["total_rows"] = total_rows
    return response
