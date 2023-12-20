import weaviate
from weaviate.embedded import EmbeddedOptions

client = weaviate.Client(embedded_options=EmbeddedOptions())

response = client.schema.get()

for resp_class in response["classes"]:
    print(f"deleting class: {resp_class['class']}")
    client.schema.delete_class(resp_class["class"])
