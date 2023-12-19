"""
DNDLibrary class
Manages the DND books including the base guides of DM, Monster and Player
"""
from pathlib import Path
import weaviate
from weaviate.embedded import EmbeddedOptions
import os
import subprocess
import logging
from unstructured.partition.pdf import partition_pdf

# for google vertex ai token refreshing
def refresh_token() -> str:
    result = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error refreshing token: {result.stderr}")
        return None
    return result.stdout.strip()

class DNDLibrary:
    def __init__(self):
        self.pdf_location = "data/"
        self.pdf_path = Path(self.pdf_location)
        self.weaviate_client = None
        self.vectorstore_class = "dndlibrary"

        # setup logging
        logging.basicConfig(
            format="%(asctime)s - %(message)s")
        self.class_logger = logging.getLogger(__name__)

    def re_instantiate_weaviate(self):
        try:
            token = refresh_token()

            if token:
                self.weaviate_client = weaviate.Client(
                    additional_headers={
                        "X-Palm-Api-Key": token
                    },
                    embedded_options=EmbeddedOptions(
                        additional_env_vars={
                            "ENABLE_MODULES": "text2vec-palm"
                        }
                    )
                )
            else:
                raise ValueError
        except Exception:
            raise

    def load_library(self):
        # Load the dnd library in the data folder
        data_objects = []

        for path in self.pdf_path.iterdir():
            if path.suffix != ".pdf":
                continue

            self.class_logger.info(f"Processing {path.name}...")

            elements = partition_pdf(filename=path)

            for i in range(len(elements)):
                data_object = {
                    "source": path.name, 
                    "content": elements[i].text
                }
                
                data_objects.append(data_object)

            self.class_logger.info(f"Added {len(data_objects)} data objects from {path.name}")

            # load into weaviate
            self.class_logger.info(f"Loading {path.name} into Weaviate")
            self.weaviate_client.batch.configure(batch_size=100)  # Configure batch
            with self.weaviate_client.batch as batch:
                for data_object in data_objects:
                    batch.add_data_object(
                        data_object,
                        self.vectorstore_class
                    )
    
    def run(self):
        # connect to weaviate embedded
        self.re_instantiate_weaviate()

        # check if collection is already created
        # if not create collection and load PDFS
        collection_found = self.weaviate_client.schema.exists(self.vectorstore_class)
        if collection_found:
            self.class_logger.info(f"{self.vectorstore_class} exists. Skip loading.")
        else:
            self.class_logger.info("Loading DND library...")
            self.load_library()


