import os

# === PATHS ===
CURRENT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR_PATH, "../../"))

# Input data folder (used in Data Ingestion)
DATA_FOLDER_PATH = os.path.join(PROJECT_ROOT, "data")

# Main artifacts folder
ARTIFACTS_FOLDER_PATH = os.path.join(PROJECT_ROOT, "artifacts")

# Logs folder
LOG_DIR_PATH = os.path.join(PROJECT_ROOT, "logs")

# === SUPPORTED EXTENSIONS ===
SUPPORTED_DOC_EXTENSIONS = ["doc", "docx", "odt", "xls", "xlsx", "ppt", "pptx"]
SUPPORTED_IMG_EXTENSIONS = ["jpg", "jpeg", "png", "tiff"]

# === OCR MODELS ===
DETECTION_MODEL = "fast_base"
RECOGNITION_MODEL = "crnn_vgg16_bn"
PRETRAINED = True
ASSUME_STRAIGHT_TEXT = False
EXPORT_AS_STRAIGHT_BOXES = True
