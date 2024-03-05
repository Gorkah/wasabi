import exifread
import piexif
from piexif import ExifIFD, GPSIFD

def leer_metadata_imagen(ruta_imagen):
    with open(ruta_imagen, 'rb') as archivo_imagen:
        tags = exifread.process_file(archivo_imagen)

    # Imprimir todas las etiquetas (metadata) disponibles
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            print(f"{tag}: {tags[tag]}")

    # Obtener la ubicación GPS si está disponible
    if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
        latitud = tags['GPS GPSLatitude']
        longitud = tags['GPS GPSLongitude']
        print(f"Ubicación GPS: Latitud {latitud}, Longitud {longitud}")
    else:
        print("No se encontró información de ubicación GPS.")

def escribir_metadata_gps(ruta_imagen, latitud, longitud):
    # Leer la imagen y su metadata existente
    exif_dict = piexif.load(ruta_imagen)

    # Convertir la latitud y longitud a formato DMS (grados, minutos, segundos)
    latitud_ref = 'N' if latitud >= 0 else 'S'
    longitud_ref = 'E' if longitud >= 0 else 'W'
    latitud = abs(latitud)
    longitud = abs(longitud)
    latitud_dms = (int(latitud), 1), (int(latitud % 1 * 60), 1), (int(latitud % 1 * 60 % 1 * 60 * 100), 100)
    longitud_dms = (int(longitud), 1), (int(longitud % 1 * 60), 1), (int(longitud % 1 * 60 % 1 * 60 * 100), 100)

    # Crear la metadata GPS
    exif_dict['GPS'] = {
        GPSIFD.GPSLatitudeRef: latitud_ref,
        GPSIFD.GPSLatitude: latitud_dms,
        GPSIFD.GPSLongitudeRef: longitud_ref,
        GPSIFD.GPSLongitude: longitud_dms,
    }

    # Serializar y escribir la metadata en la imagen
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, ruta_imagen)

    print("Metadata GPS escrita exitosamente en la imagen.")

def main():
    while True:
        print("\nMENU:")
        print("1. Leer metadata de una imagen")
        print("2. Escribir metadata GPS en una imagen")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            # Solicitar la ruta de la imagen
            ruta_imagen = input("Por favor, introduce la ruta de la imagen: ")
            print("\nMetadata de la imagen:")
            leer_metadata_imagen(ruta_imagen)
        elif opcion == "2":
            # Solicitar la ruta de la imagen
            ruta_imagen = input("Por favor, introduce la ruta de la imagen: ")
            # Solicitar las coordenadas GPS
            latitud = float(input("Introduce la latitud (ej. 37.7749): "))
            longitud = float(input("Introduce la longitud (ej. -122.4194): "))
            escribir_metadata_gps(ruta_imagen, latitud, longitud)
        elif opcion == "3":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")

if __name__ == "__main__":
    main()
