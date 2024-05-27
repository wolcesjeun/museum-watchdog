from pathlib import Path
import hashlib
import google.generativeai as genai


class ObjectExtractor:
    def __init__(self):
        genai.configure(api_key="AIzaSyDrScl5UUguG17Q6Igmba21m-tx4nmEWI4")
        self.model_name = "gemini-1.5-pro-latest"
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        self.model = genai.GenerativeModel(model_name=self.model_name,
                                           generation_config=self.generation_config,
                                           safety_settings=self.safety_settings)
        self.uploaded_files = []

    def upload_if_needed(self, pathname: str) -> list[str]:
        path = Path(pathname)
        hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
        try:
            existing_file = genai.get_file(name=hash_id)
            return [existing_file]
        except:
            pass
        self.uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
        return [self.uploaded_files[-1]]

    def object_extractor_from_image(self, image_path: str) -> str:
        prompt_parts = [
            """
            You are a museum security camera. In the visual, identify the number of historical artifacts you see and list them. I need you to provide a JSON output where you first state the total number of artifacts. Then, create a nested JSON or a list for the artifacts, and for each artifact, include small JSON data containing the artifact name, artifact type, and artifact category.
            Example JSON output:
                {
                "total_artifacts": 3,
                "artifacts": [
                    {
                        "artifact_name": "Ancient Vase",
                        "artifact_type": "Ceramics",
                        "artifact_category": "Ancient Artifacts"
                    },
                    {
                        "artifact_name": "Medieval Sword",
                        "artifact_type": "Weaponry",
                        "artifact_category": "Medieval Artifacts"
                    },
                    {
                        "artifact_name": "Renaissance Painting",
                        "artifact_type": "Painting",
                        "artifact_category": "Renaissance Art"
                    }
                ]
                }"""
            # "Extract the objects in the provided image and output them in a list in alphabetical order",
            # *** promt düzenlenecek ve json cıktısı adam edilecek.****
            # "Sen bir müze güvenlik kamerası bekçi köpeğisin senin işin gördüğün görselde bir müze eseri aramak ve bu eseri oldukça detaylandırıp çıktı vermek",
            "Image: ",
            *self.upload_if_needed(image_path),
            "List of Objects: ",
        ]
        response = self.model.generate_content(prompt_parts)
        generated_text = response.text
        for uploaded_file in self.uploaded_files:
            genai.delete_file(name=uploaded_file.name)
        return generated_text


if __name__ == "__main__":
    generative_model = ObjectExtractor()
    element_path = "element_screenshots/pexelsvideo01-20240504_034257.png"
    generated_output = generative_model.object_extractor_from_image(element_path)
    print(generated_output)
