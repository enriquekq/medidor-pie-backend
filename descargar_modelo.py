import os
import gdown

file_id = "1HQecdeSAXIjONkUMQAqPiTfUCoNY7uoA"
url = f"https://drive.google.com/uc?id={file_id}"
output_path = "best.pt"

if not os.path.exists(output_path):
    print("Descargando modelo best.pt desde Google Drive...")
    gdown.download(url, output_path, quiet=False)
else:
    print("Modelo best.pt ya existe.")
