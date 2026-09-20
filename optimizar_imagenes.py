from pathlib import Path
from PIL import Image

BASE = Path(__file__).resolve().parent

CARPETAS = [
    BASE / "app" / "static" / "img",
    BASE / "app" / "static" / "img" / "civil",
]

CALIDAD = 82
MAX_LADO = 2400

EXTENSIONES = {".jpg", ".jpeg", ".png"}

for carpeta in CARPETAS:

    if not carpeta.exists():
        print(f"Carpeta no encontrada: {carpeta}")
        continue

    for archivo in carpeta.iterdir():

        if archivo.suffix.lower() not in EXTENSIONES:
            continue

        # No volver a procesar archivos WebP
        salida = archivo.with_suffix(".webp")

        try:
            with Image.open(archivo) as imagen:

                # Convertimos a RGB para evitar problemas con PNG
                imagen = imagen.convert("RGB")

                # Reducimos únicamente si supera el tamaño máximo
                imagen.thumbnail(
                    (MAX_LADO, MAX_LADO),
                    Image.Resampling.LANCZOS
                )

                imagen.save(
                    salida,
                    "WEBP",
                    quality=CALIDAD,
                    method=6
                )

            original_mb = archivo.stat().st_size / (1024 * 1024)
            nuevo_mb = salida.stat().st_size / (1024 * 1024)

            print(archivo.name)
            print(f"  Original: {original_mb:.2f} MB")
            print(f"  WebP:     {nuevo_mb:.2f} MB")
            print(f"  Guardado: {salida.name}")
            print()

        except Exception as error:
            print(f"ERROR en {archivo}: {error}")

print("Proceso terminado.")
print("Los archivos originales NO fueron eliminados.")