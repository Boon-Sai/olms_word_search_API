import os
import sys
import json
from PIL import Image, ImageDraw
from fuzzywuzzy import fuzz
from src.exception.exception import WordSearchException
from src.logging import logger
from src.entity.config_entity import DataSearchConfig, ConfigEntity
from src.entity.artifact_entity import DataSearchArtifact


class DataSearch:
    def __init__(self):
        try:
            logger.logger.info("Initializing Data Search component...")
            self.config = DataSearchConfig(config=ConfigEntity())

            os.makedirs(self.config.data_search_folder_path, exist_ok=True)

            logger.logger.info(f"Search output folder: {self.config.data_search_folder_path}")

        except Exception as e:
            raise WordSearchException(str(e), sys) from e

    def annotate_page(self, image_path, words, output_path):
        """Draw bounding boxes on the image for matched words only."""
        try:
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
                    # Optionally, add text label for matched word
                    draw.text((x_min, y_min - 10), word['word'], fill='red')

                img.save(output_path, "JPEG")
                logger.logger.info(f"Annotated image saved to {output_path}")

        except Exception as e:
            raise WordSearchException(f"Failed to annotate image: {str(e)}", sys) from e

    def initiate_data_search(self, search_query: str, fuzzy_threshold: int = 80, partial_match: bool = True):
        """Search for words in the OCR results JSON with dynamic matching options."""
        try:
            input_json_path = self.config.input_json_path
            if not os.path.exists(input_json_path):
                raise WordSearchException(
                    f"OCR results JSON not found: {input_json_path}", sys
                )

            with open(input_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Split search query into individual terms
            search_terms = search_query.strip().split()
            results = []
            annotated_images = {}

            for entry in data:
                entry_word = entry["word"].lower()
                document = entry["document"]
                if not document.endswith(".pdf"):
                    document += ".pdf"
                page_str = entry["page_image"].split("_")[1].split(".")[0]
                page = int(page_str)

                # Check each search term
                for term in search_terms:
                    term_lower = term.lower()
                    match = False

                    # Exact or partial match
                    if partial_match and term_lower in entry_word:
                        match = True
                    # Fuzzy match
                    elif fuzz.ratio(term_lower, entry_word) >= fuzzy_threshold:
                        match = True

                    if match:
                        result = {
                            "document": document,
                            "page": page,
                            "word": entry["word"],
                            "bounding_box": entry["bounding_box"],
                            "confidence": entry["confidence"],
                            "matched_term": term  # Track which term matched
                        }
                        results.append(result)

                        # Track images for annotation
                        image_key = (document, page)
                        if image_key not in annotated_images:
                            annotated_images[image_key] = []
                        annotated_images[image_key].append(result)

            # Generate annotated images for matched words
            images_root = os.path.join(
                self.config.artifact_folder_path, "data_transformation", "images"
            )
            for (document, page), matched_words in annotated_images.items():
                doc_folder = os.path.join(images_root, document.replace(".pdf", ""))
                img_file = f"img_{page}.jpg"
                img_path = os.path.join(doc_folder, img_file)
                if not os.path.exists(img_path):
                    logger.logger.warning(f"Image not found: {img_path}")
                    continue

                annotated_doc_folder = os.path.join(
                    self.config.data_search_folder_path, "annotated_images", document.replace(".pdf", "")
                )
                os.makedirs(annotated_doc_folder, exist_ok=True)
                annotated_img_path = os.path.join(annotated_doc_folder, img_file)
                self.annotate_page(img_path, matched_words, annotated_img_path)

            # Save search results to JSON
            search_query_safe = search_query.replace(" ", "_")
            output_json_path = os.path.join(
                self.config.data_search_folder_path, f"search_{search_query_safe}.json"
            )
            with open(output_json_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            logger.logger.info(f"Search results saved to {output_json_path}")

            return DataSearchArtifact(
                search_result_file_path=output_json_path
            )

        except Exception as e:
            raise WordSearchException(str(e), sys) from e