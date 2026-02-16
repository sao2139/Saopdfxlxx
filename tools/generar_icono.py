import os
from PIL import Image

def convertir_jpg_a_ico_hd(input_path, output_path):
    """
    Convierte una imagen a .ico incluyendo múltiples tamaños
    para asegurar alta resolución en todas las vistas de Windows.
    """
    
    # 1. Verificar si existe la imagen original
    if not os.path.exists(input_path):
        print(f"[ERROR] No se encontró el archivo: {input_path}")
        return

    try:
        print(f"[INFO] Procesando imagen: {input_path}...")
        
        # 2. Abrir imagen original
        img = Image.open(input_path)
        
        # 3. Definir los tamaños estándar de iconos de Windows
        # El sistema operativo elegirá automáticamente el mejor para cada situación.
        icon_sizes = [
            (256, 256), # Icono Extra Grande (Vista Escritorio)
            (128, 128), # Grande
            (64, 64),   # Mediano
            (48, 48),   # Barra de tareas / Inicio
            (32, 32),   # Listas / Explorador
            (16, 16)    # Esquina de ventana / Detalles
        ]
        
        # 4. Guardar como ICO conteniendo TODOS los tamaños
        # Pillow hace el re-escalado (resampling) automáticamente con alta calidad (LANCZOS)
        img.save(
            output_path, 
            format='ICO', 
            sizes=icon_sizes
        )
        
        print(f"[ÉXITO] Icono generado en: {output_path}")
        print("[INFO] El archivo .ico contiene capas de: 256px, 128px, 64px, 48px, 32px y 16px.")

    except Exception as e:
        print(f"[FATAL] Error al convertir: {e}")

if __name__ == "__main__":
    # --- CONFIGURACIÓN ---
    # Ajusta estas rutas según tu estructura de carpetas
    
    # Ruta de entrada (Tu logo en JPG de alta calidad)
    INPUT_FILE = os.path.join("assets", "logo.jpg")
    
    # Ruta de salida (Donde guardaremos el icono)
    OUTPUT_FILE = os.path.join("assets", "mi_logo.ico")
    
    # Asegurar que la carpeta assets exista
    if not os.path.exists("assets"):
        os.makedirs("assets")
        
    # Ejecutar conversión
    convertir_jpg_a_ico_hd(INPUT_FILE, OUTPUT_FILE)