import os
import threading
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from openpyxl import Workbook
from openpyxl.styles import Font

from config.settings import APP_TITLE, APP_SIZE
from core.engine import PDFExtractor

COLOR_SIDEBAR = "#2c3e50"
COLOR_FONDO = "#ecf0f1"
COLOR_TEXTO = "#2c3e50"
COLOR_BTN_VERDE = "#1abc9c"
COLOR_BTN_ROJO = "#e74c3c"
COLOR_PROGRESO = "#3498db"

class SaoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title(APP_TITLE)
        self.geometry(APP_SIZE)
        self.resizable(False, False)
        ctk.set_appearance_mode("Light")
        
        try:
            ruta_icono = os.path.join("assets", "mi_logo.ico")
            self.iconbitmap(ruta_icono)
        except:
            pass

        self.ruta_carpeta = ""
        self.motor = PDFExtractor()
        self.procesando = False

        self._construir_interfaz()

    def _construir_interfaz(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=COLOR_SIDEBAR)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        try:
            ruta_logo = os.path.join("assets", "logo.jpg")
            img_original = Image.open(ruta_logo)
            ancho_base = 180
            porcentaje = (ancho_base / float(img_original.size[0]))
            alto_final = int((float(img_original.size[1]) * float(porcentaje)))
            imagen_ctk = ctk.CTkImage(light_image=img_original, size=(ancho_base, alto_final))
            lbl_logo = ctk.CTkLabel(self.sidebar, text="", image=imagen_ctk)
            lbl_logo.grid(row=0, column=0, pady=30, padx=20)
        except:
            ctk.CTkLabel(self.sidebar, text="SAO SYSTEMS", text_color="white").grid(row=0, column=0, pady=30)

        ctk.CTkLabel(self.sidebar, text="SaoPdfxlxx", font=("Arial", 20, "bold"), text_color="white").grid(row=1, column=0)

        self.btn_carpeta = ctk.CTkButton(self.sidebar, text="SELECCIONAR CARPETA", 
                                         command=self.seleccionar_carpeta,
                                         fg_color=COLOR_BTN_VERDE, hover_color="#16a085",
                                         height=40, font=("Arial", 12, "bold"))
        self.btn_carpeta.grid(row=2, column=0, pady=20, padx=20, sticky="ew")

        self.btn_iniciar = ctk.CTkButton(self.sidebar, text="INICIAR PROCESO", 
                                         command=self.iniciar_hilo_proceso,
                                         fg_color="#95a5a6", state="disabled",
                                         height=40, font=("Arial", 12, "bold"))
        self.btn_iniciar.grid(row=3, column=0, pady=0, padx=20, sticky="ew")

        ctk.CTkLabel(self.sidebar, text="Enterprise v1.0 Lite\nSao Systems", text_color="gray").grid(row=5, column=0, pady=20)
        self.sidebar.grid_rowconfigure(4, weight=1)

        # --- MAIN PANEL ---
        self.panel_main = ctk.CTkFrame(self, fg_color=COLOR_FONDO, corner_radius=0)
        self.panel_main.grid(row=0, column=1, sticky="nsew")
        self.panel_main.grid_columnconfigure(0, weight=1)
        self.panel_main.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(self.panel_main, text="Panel de Control", font=("Arial", 24, "bold"), text_color=COLOR_TEXTO).grid(row=0, column=0, pady=(30,10), padx=30, sticky="w")
        
        self.lbl_estado = ctk.CTkLabel(self.panel_main, text="Estado: Esperando carpeta...", font=("Arial", 14), text_color="gray")
        self.lbl_estado.grid(row=1, column=0, pady=0, padx=30, sticky="w")

        self.barra = ctk.CTkProgressBar(self.panel_main, progress_color=COLOR_PROGRESO, height=15)
        self.barra.grid(row=2, column=0, pady=20, padx=30, sticky="ew")
        self.barra.set(0)

        self.consola = ctk.CTkTextbox(self.panel_main, font=("Consolas", 12), text_color="black", fg_color="white")
        self.consola.grid(row=3, column=0, pady=(0,30), padx=30, sticky="nsew")
        self.log("Sistema SaoPdfxlxx Lite inicializado.")

    def log(self, mensaje):
        hora = datetime.now().strftime("%H:%M:%S")
        texto = f"[{hora}] > {mensaje}\n"
        self.after(0, lambda: self._escribir_consola(texto))

    def _escribir_consola(self, texto):
        self.consola.configure(state="normal")
        self.consola.insert("end", texto)
        self.consola.see("end")
        self.consola.configure(state="disabled")

    def seleccionar_carpeta(self):
        ruta = filedialog.askdirectory()
        if ruta:
            self.ruta_carpeta = ruta
            nombre = os.path.basename(ruta)
            self.log(f"Carpeta seleccionada: {nombre}")
            self.lbl_estado.configure(text=f"Lista para procesar: {nombre}")
            self.btn_iniciar.configure(state="normal", fg_color=COLOR_BTN_ROJO)

    def iniciar_hilo_proceso(self):
        if not self.procesando:
            self.procesando = True
            self.btn_carpeta.configure(state="disabled")
            self.btn_iniciar.configure(state="disabled", text="TRABAJANDO...")
            hilo = threading.Thread(target=self.proceso_pesado)
            hilo.daemon = True
            hilo.start()

    def proceso_pesado(self):
        self.log("--- INICIANDO EXTRACCIÓN ---")
        archivos = [f for f in os.listdir(self.ruta_carpeta) if f.lower().endswith('.pdf')]
        total = len(archivos)
        
        if total == 0:
            self.log("No encontré archivos PDF.")
            self.restaurar_botones()
            return

        datos_extraidos = []
        errores = 0

        for i, archivo in enumerate(archivos):
            progreso = (i + 1) / total
            self.after(0, lambda p=progreso: self.barra.set(p))
            
            ruta_completa = os.path.join(self.ruta_carpeta, archivo)
            info = self.motor.process_file(ruta_completa)
            
            if "Error" in info:
                self.log(f"[X] Error en {archivo}")
                errores += 1
            else:
                info['Archivo'] = archivo
                datos_extraidos.append(info)
                self.log(f"[OK] {archivo}")

        self.guardar_excel(datos_extraidos, total, errores)
        self.restaurar_botones()

    def guardar_excel(self, datos, total, errores):
        if not datos:
            return
            
        ruta_excel = os.path.join(self.ruta_carpeta, "Reporte_Final.xlsx")
        
        try:
            wb = Workbook()
            hoja = wb.active
            hoja.title = "Datos"
            
            headers = ["Nombre", "Dirección", "Fecha", "Archivo"]
            hoja.append(headers)
            
            for celda in hoja[1]:
                celda.font = Font(bold=True)
                
            for fila in datos:
                valores = [
                    fila.get("Nombre", ""),
                    fila.get("Dirección", ""),
                    fila.get("Fecha", ""),
                    fila.get("Archivo", "")
                ]
                hoja.append(valores)

            for columna in hoja.columns:
                max_longitud = 0
                letra_columna = columna[0].column_letter
                for celda in columna:
                    try:
                        if len(str(celda.value)) > max_longitud:
                            max_longitud = len(str(celda.value))
                    except:
                        pass
                hoja.column_dimensions[letra_columna].width = (max_longitud + 2)

            wb.save(ruta_excel)
            self.log("--- EXCEL GUARDADO CORRECTAMENTE ---")
            self.after(0, lambda: messagebox.showinfo("Éxito", f"Procesados: {total}\nErrores: {errores}"))
            
        except Exception as e:
            self.log(f"Error guardando Excel: {e}")
            self.after(0, lambda: messagebox.showerror("Error", "Cierra el Excel antes de continuar."))

    def restaurar_botones(self):
        self.procesando = False
        self.after(0, lambda: self._activar_ui())

    def _activar_ui(self):
        self.btn_carpeta.configure(state="normal")
        self.btn_iniciar.configure(state="normal", text="INICIAR PROCESO", fg_color=COLOR_BTN_ROJO)
        self.barra.set(0)
        self.lbl_estado.configure(text="Proceso finalizado.")