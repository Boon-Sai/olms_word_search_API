from dataclass import dataclass

@dataclass
class DataTransformationArtifact:
    image_file_path: str
    converted_document_file_path: str

@dataclass
class DataDetectionArtifact:
    annotated_image_file_path: str
    output_json_file_path: str