import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import exifread
import piexif
from piexif import ExifIFD, GPSIFD

def leer_metadata_imagen(ruta_imagen):
    with open(ruta_imagen, 'rb') as archivo_imagen:
        tags = exifread.process_file(archivo_imagen)

    metadata = ""
    # Agregar todas las etiquetas (metadata) disponibles a un string
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            metadata += f"{tag}: {tags[tag]}\n"

    # Obtener la ubicación GPS si está disponible
    if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
        latitud = tags['GPS GPSLatitude']
        longitud = tags['GPS GPSLongitude']
        metadata += f"Ubicación GPS: Latitud {latitud}, Longitud {longitud}"
    else:
        metadata += "No se encontró información de ubicación GPS."

    # Mostrar la metadata en una ventana emergente
    messagebox.showinfo("Metadata de la imagen", metadata)

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

    messagebox.showinfo("Éxito", "Metadata GPS escrita exitosamente en la imagen.")

def seleccionar_imagen():
    ruta_imagen = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=(("Archivos de imagen", "*.jpg;*.jpeg;*.png;*.bmp;*.gif"), ("Todos los archivos", "*.*")))
    if ruta_imagen:
        return ruta_imagen
    else:
        messagebox.showwarning("Advertencia", "No se seleccionó ninguna imagen.")
        return None

def leer_metadata():
    ruta_imagen = seleccionar_imagen()
    if ruta_imagen:
        leer_metadata_imagen(ruta_imagen)

def escribir_metadata():
    ruta_imagen = seleccionar_imagen()
    if ruta_imagen:
        latitud = float(entry_latitud.get())
        longitud = float(entry_longitud.get())
        escribir_metadata_gps(ruta_imagen, latitud, longitud)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Metadata de Imágenes")

# Etiqueta y campo de entrada para latitud
label_latitud = tk.Label(ventana, text="Latitud:")
label_latitud.grid(row=0, column=0, padx=10, pady=5)
entry_latitud = tk.Entry(ventana)
entry_latitud.grid(row=0, column=1, padx=10, pady=5)

# Etiqueta y campo de entrada para longitud
label_longitud = tk.Label(ventana, text="Longitud:")
label_longitud.grid(row=1, column=0, padx=10, pady=5)
entry_longitud = tk.Entry(ventana)
entry_longitud.grid(row=1, column=1, padx=10, pady=5)

# Botones para leer y escribir metadata
btn_leer_metadata = tk.Button(ventana, text="Leer Metadata", command=leer_metadata)
btn_leer_metadata.grid(row=2, column=0, padx=10, pady=5)
btn_escribir_metadata = tk.Button(ventana, text="Escribir Metadata GPS", command=escribir_metadata)
btn_escribir_metadata.grid(row=2, column=1, padx=10, pady=5)

ventana.mainloop()
