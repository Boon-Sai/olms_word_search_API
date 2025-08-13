from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import shutil
import os
import tempfile
from src.pipeline.pipeline import TrainPipeline
from src.exception.exception import WordSearchException
from src.logging import logger

app = FastAPI(title="Word Search Pipeline API")

import os
@app.post("/run-pipeline")
async def run_pipeline_api(folder_path: str = Form(...)):
    try:
        logger.logger.info(f"Received folder path: {folder_path}")
        if not os.path.exists(folder_path):
            return JSONResponse(status_code=400, content={"error": "Folder path does not exist"})
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        pipeline = TrainPipeline()
        transformation_artifact, detection_artifact = pipeline.run_pipeline(folder_path)
        response = {
            "message": "Pipeline executed successfully",
            "data_transformation": {
                "extracted_images_folder": transformation_artifact.image_file_path,
                "converted_documents_folder": transformation_artifact.converted_document_file_path
            },
            "data_detection": {
                "detection_results_file": detection_artifact.output_json_file_path
            }
        }
        return JSONResponse(status_code=200, content=response)
    except WordSearchException as e:
        logger.logger.error(f"Pipeline failed with error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})
    except Exception as e:
        logger.logger.error(f"Unexpected error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
