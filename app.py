from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import shutil
import os
import tempfile
from src.pipeline.pipeline import TrainPipeline
from src.exception.exception import WordSearchException
from src.logging import logger
from src.components.data_search import DataSearch
import json

app = FastAPI(
    title="Word Search Pipeline API",
    description="API for processing documents to extract text via OCR and searching for specific words in the extracted text.",
    version="1.0.0"
)

@app.post(
    "/run-pipeline",
    summary="Run Document Processing Pipeline",
    description="Processes documents in the specified folder path to convert them to images and perform OCR, generating a JSON file with all detected words."
)
async def run_pipeline_api(folder_path: str = Form(..., description="Path to the folder containing documents to process")):
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
                "annotated_images_folder": detection_artifact.annotated_image_file_path,
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

@app.post(
    "/search-word",
    summary="Search for a Word in OCR Results",
    description="Searches for a specific word in the OCR results JSON file (automatically sourced from artifacts/data_detection/annotated_images/output_json/final_output.json) and returns matching entries."
)
async def search_word_api(search_word: str = Form(..., description="The word to search for in the OCR results")):
    try:
        logger.logger.info(f"Received search word: {search_word}")
        if not search_word.strip():
            return JSONResponse(status_code=400, content={"error": "Search word cannot be empty"})

        searcher = DataSearch()
        search_artifact = searcher.initiate_data_search(search_word)

        with open(search_artifact.search_result_file_path, "r", encoding="utf-8") as f:
            search_results = json.load(f)

        response = {
            "message": "Search executed successfully",
            "data_search": {
                "results": search_results
            }
        }
        return JSONResponse(status_code=200, content=response)
    except WordSearchException as e:
        logger.logger.error(f"Search failed with error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})
    except Exception as e:
        logger.logger.error(f"Unexpected error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)