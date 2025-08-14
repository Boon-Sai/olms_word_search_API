import os
import sys
import json
from PIL import Image, ImageDraw
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from tqdm import tqdm

from src.exception.exception import WordSearchException
from src.logging import logger
from src.entity.config_entity import DataDetectionConfig, ConfigEntity
from src.entity.artifact_entity import DataDetectionArtifact


class DataDetection:
    def __init__(self):
        try:
            logger.logger.info("Initializing Data Detection component...")
            self.config = DataDetectionConfig(config=ConfigEntity())

            os.makedirs(self.config.annotated_images_folder, exist_ok=True)
            os.makedirs(self.config.output_json_folder, exist_ok=True)

            logger.logger.info(f"Annotated images folder: {self.config.annotated_images_folder}")
            logger.logger.info(f"Output folder: {self.config.output_json_folder}")

            # Initialize OCR model
            self.model = ocr_predictor(
                det_arch=self.config.data_detection_model,
                reco_arch=self.config.data_recognition_model,
                pretrained=self.config.pretrained,
                assume_straight_pages=self.config.assume_straight_text,
                export_as_straight_boxes=self.config.export_as_straingt_boxes
            )

        except Exception as e:
            raise WordSearchException(str(e), sys) from e

    def annotate_page(self, image_path, words, output_path):
        """Draw bounding boxes on the image for all detected words."""
        with Image.open(image_path) as img:
            draw = ImageDraw.Draw(img)
            img_width, img_height = img.size

            for word in words:
                bbox = word['bounding_box']
                x_min = bbox[0] * img_width
                y_min = bbox[1] * img_height
                x_max = bbox[2] * img_width
                y_max = bbox[3] * img_height
                draw.rectangle([(x_min, y_min), (x_max, y_max)], outline='red', width=2)

            img.save(output_path, "JPEG")

    def initiate_data_detection(self):
        """Run OCR on all images from data_transformation and save results."""
        try:
            results = []

            # Path to images from data_transformation
            images_root = os.path.join(
                self.config.artifact_folder_path, "data_transformation", "images" #need to add it in constants
            )

            if not os.path.exists(images_root):
                raise WordSearchException(
                    f"Images folder not found: {images_root}", sys
                )

            for doc_name in tqdm(os.listdir(images_root), desc="Processing documents"):
                doc_folder = os.path.join(images_root, doc_name)
                if not os.path.isdir(doc_folder):
                    continue

                logger.logger.info(f"Processing document: {doc_name}")

                annotated_doc_folder = os.path.join(
                    self.config.annotated_images_folder, doc_name
                )
                os.makedirs(annotated_doc_folder, exist_ok=True)

                for img_file in sorted(os.listdir(doc_folder)):
                    img_path = os.path.join(doc_folder, img_file)

                    # Load image into docTR
                    doc = DocumentFile.from_images(img_path)
                    ocr_result = self.model(doc)

                    page_words = []
                    for block in ocr_result.pages[0].blocks:
                        for line in block.lines:
                            for word in line.words:
                                word_data = {
                                    "document": doc_name,
                                    "page_image": img_file,
                                    "word": word.value,
                                    "bounding_box": [
                                        word.geometry[0][0],
                                        word.geometry[0][1],
                                        word.geometry[1][0],
                                        word.geometry[1][1]
                                    ],
                                    "confidence": word.confidence
                                }
                                page_words.append(word_data)
                                results.append(word_data)

                    # Save annotated image
                    annotated_img_path = os.path.join(annotated_doc_folder, img_file)
                    self.annotate_page(img_path, page_words, annotated_img_path)

            # Save all results to JSON
            json_path = os.path.join(self.config.output_json_folder, "final_output.json") # need to add it in constants
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            logger.logger.info(f"OCR results saved to {json_path}")

            return DataDetectionArtifact(
                annotated_image_file_path=self.config.annotated_images_folder,
                output_json_file_path=json_path
            )

        except Exception as e:
            raise WordSearchException(str(e), sys) from e
