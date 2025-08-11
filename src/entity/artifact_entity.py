from dataclasses import dataclass

@dataclass
class DataTransformationArtifact:
    """
    Holds the output paths generated after data transformation.
    """
    image_file_path: str                    # Path to folder containing extracted images
    converted_document_file_path: str  

@dataclass
class DataDetectionArtifact:
    annotated_image_file_path: str
    output_json_file_path: str