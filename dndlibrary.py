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
from abstractextractor import AbstractExtractor

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
        self.vectorstore_id = "dndlibrary"

        # setup logging
        logging.basicConfig(
            format="%(asctime)s - %(message)s")
        self.class_logger = logging.getLogger(__name__)

    def re_instantiate_weaviate(self) -> weaviate.Client:
        try:
            token = self.refresh_token()

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

            abstract_extractor = AbstractExtractor()
            abstract_extractor.consume_elements(elements)

            data_object = {"source": path.name, "abstract": abstract_extractor.abstract()}

            data_objects.append(data_object)

        # load into weaviate
        self.weaviate_client.batch.configure(batch_size=100)  # Configure batch
        with self.weaviate_client.batch as batch:
            for data_object in data_objects:
                batch.add_data_object(data_object, "Document")
    
    def run(self):
        # check if collection is already created
        # if not create collection and load PDFS
        collection_found = False
        try:
            collection_check = self.weaviate_client.collections.get(self.vectorstore_id)
            self.class_logger.info(f"{self.vectorstore_id} exists. Skip loading.")
            collection_found = True
        except Exception as err:
            self.class_logger.error(f"Run failed, no collection found: {err}")
            collection_found = False
            pass

        if not collection_found:
            self.class_logger.info("Loading DND library...")
            self.load_library()


