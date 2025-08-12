import os
import sys
import glob
import shutil
import subprocess
from PIL import Image
from pdf2image import convert_from_path

from src.exception.exception import WordSearchException
from src.logging import logger
from src.entity.config_entity import DataTransformationConfig, ConfigEntity
from src.entity.artifact_entity import DataTransformationArtifact



class DataTransformation:
    def __init__(self):
        try:
            logger.logger.info("Initializing Data Transformation component...")
            self.config = DataTransformationConfig(config=ConfigEntity())

            logger.logger.info(f"Documents folder: {self.config.documents_folder}")
            logger.logger.info(f"Images folder: {self.config.images_folder}")

        except Exception as e:
            raise WordSearchException(str(e), sys) from e

    def preprocess_files(self):
        """Convert supported documents/images to PDFs."""
        try:
            logger.logger.info("Starting file preprocessing...")

            pdf_paths = []
            supported_extensions = (
                self.config.supported_doc_extenctions
                + self.config.supported_img_extenctions
                + ["pdf"]
            )

            for ext in supported_extensions:
                files = glob.glob(os.path.join(self.config.data_folder_path, f"*.{ext}"))

                if not files:
                    continue

                logger.logger.info(f"Found {len(files)} .{ext} files to process.")

                for file_path in files:
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    pdf_path = os.path.join(self.config.documents_folder, f"{base_name}.pdf")

                    try:
                        if ext in self.config.supported_doc_extenctions:
                            logger.logger.info(f"Converting {file_path} to PDF via LibreOffice...")
                            subprocess.run(
                                [
                                    "soffice", "--headless", "--convert-to", "pdf",
                                    file_path, "--outdir", self.config.documents_folder
                                ],
                                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                            )

                        elif ext in self.config.supported_img_extenctions:
                            logger.logger.info(f"Converting image {file_path} to PDF...")
                            img = Image.open(file_path)
                            rgb_img = img.convert("RGB")
                            rgb_img.save(pdf_path)

                        elif ext == "pdf":
                            logger.logger.info(f"Copying existing PDF {file_path}...")
                            shutil.copy(file_path, pdf_path)

                        else:
                            logger.logger.warning(f"Unsupported file skipped: {file_path}")
                            continue

                        pdf_paths.append(pdf_path)
                        logger.logger.info(f"Processed: {file_path}")

                    except subprocess.CalledProcessError as e:
                        logger.logger.error(
                            f"LibreOffice failed for {file_path}: {e.stderr.decode()}"
                        )
                    except Exception as e:
                        raise WordSearchException(str(e), sys) from e

            logger.logger.info("File preprocessing completed.")
            return pdf_paths

        except Exception as e:
            raise WordSearchException(str(e), sys) from e

    def extract_images_from_pdfs(self, pdf_paths):
        """Extract images from PDFs page by page."""
        try:
            logger.logger.info("Starting image extraction from PDFs...")

            image_file_paths = []

            for pdf_path in pdf_paths:
                base_name = os.path.splitext(os.path.basename(pdf_path))[0]
                doc_image_folder = os.path.join(self.config.images_folder, base_name)
                os.makedirs(doc_image_folder, exist_ok=True)

                logger.logger.info(f"Extracting from {pdf_path} to {doc_image_folder}")

                try:
                    pages = convert_from_path(pdf_path)
                    for idx, page in enumerate(pages, start=1):
                        image_filename = f"img_{idx}.jpg"
                        image_path = os.path.join(doc_image_folder, image_filename)
                        page.save(image_path, "JPEG")
                        image_file_paths.append(image_path)

                    logger.logger.info(f"Extracted {len(pages)} images from {pdf_path}.")

                except Exception as e:
                    raise WordSearchException(str(e), sys) from e

            logger.logger.info("Image extraction completed.")
            return image_file_paths

        except Exception as e:
            raise WordSearchException(str(e), sys) from e

    def initiate_data_transformation(self):
        """Run full pipeline: convert to PDFs, then extract images."""
        try:
            logger.logger.info("Starting full data transformation pipeline...")

            pdf_paths = self.preprocess_files()
            image_paths = self.extract_images_from_pdfs(pdf_paths)

            logger.logger.info("Data transformation completed successfully.")

            return DataTransformationArtifact(
                image_file_path=self.config.images_folder,
                converted_document_file_path=self.config.documents_folder
            )

        except Exception as e:
            raise WordSearchException(str(e), sys) from e
