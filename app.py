# app.py
import sys
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from src.exception.exception import WordSearchException
from src.logging import logger
from src.pipeline.pipeline import Pipeline

app = FastAPI(
    title="Word Search Pipeline API",
    description="API to trigger data transformation and data detection pipeline",
    version="1.0.0"
)


@app.get("/")
def read_root():
    return {"message": "Word Search Pipeline API is running"}


@app.post("/run-pipeline")
def run_pipeline():
    try:
        logger.logger.info("=== API Trigger: Pipeline Started ===")
        pipeline = Pipeline()
        artifact = pipeline.run_pipeline()
        logger.logger.info("=== API Trigger: Pipeline Completed ===")

        return JSONResponse(content={
            "status": "success",
            "extracted_images_folder": artifact.image_file_path,
            "converted_documents_folder": artifact.converted_document_file_path,
            "detection_results_folder": artifact.detection_results_path
        })

    except WordSearchException as we:
        logger.logger.error(f"WordSearchException: {str(we)}")
        raise HTTPException(status_code=500, detail=str(we))

    except Exception as e:
        err_msg = "".join(traceback.format_exception(*sys.exc_info()))
        logger.logger.error(f"Unexpected error: {err_msg}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
