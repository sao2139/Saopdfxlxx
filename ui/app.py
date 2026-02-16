import os
import threading
import pandas as pd
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from datetime import datetime

# Importamos la configuración y el motor lógico
from config.settings import APP_TITLE, APP_SIZE
from core.engine import PDFExtractor

# --- CONFIGURACIÓN DE COLORES CORPORATIVOS ---
COLOR_SIDEBAR_BG = "#2c3e50"       # Gris azulado oscuro (Profesional)
COLOR_MAIN_BG = "#ecf0f1"          # Gris muy claro (Limpio)
COLOR_TEXT_SIDEBAR = "#ffffff"     # Texto blanco
COLOR_TEXT_MAIN = "#2c3e50"        # Texto oscuro
COLOR_BTN_FOLDER = "#1abc9c"       # Turquesa (Acción secundaria)
COLOR_BTN_RUN_DISABLED = "#95a5a6" # Gris (Desactivado)
COLOR_BTN_RUN_ACTIVE = "#e74c3c"   # Rojo Intenso (Acción principal)
COLOR_PROGRESS = "#3498db"         # Azul corporativo
COLOR_CONSOLE_BG = "#ffffff"       # Fondo blanco para logs

class SaoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --- 1. CONFIGURACIÓN DE VENTANA ---
        self.title(APP_TITLE)
        self.geometry(APP_SIZE)
        self.resizable(False, False)
        ctk.set_appearance_mode("Light") # Base clara para aspecto de oficina
        
        # --- 2. CONFIGURACIÓN DEL ÍCONO (.ico) ---
        # Esto pone tu logo en la barra de tareas y esquina de la ventana
        icon_path = os.path.join("assets", "mi_logo.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception as e:
                print(f"Advertencia: No se pudo cargar el icono .ico: {e}")

        # --- 3. ESTADO INICIAL ---
        self.folder_path = ""
        self.extractor = PDFExtractor()
        self.is_running = False

        # --- 4. CONSTRUCCIÓN DE LA INTERFAZ ---
        self._setup_ui()

    def _setup_ui(self):
        """Diseña la interfaz gráfica pixel-perfect."""
        self.grid_columnconfigure(0, weight=0) # Sidebar fijo
        self.grid_columnconfigure(1, weight=1) # Área principal flexible
        self.grid_rowconfigure(0, weight=1)

        # === SIDEBAR (IZQUIERDA) ===
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=COLOR_SIDEBAR_BG)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1) # Empuja el footer hacia abajo

        # A. Carga Inteligente del Logo (Sin deformar)
        logo_path = os.path.join("assets", "logo.jpg")
        if os.path.exists(logo_path):
            try:
                pil_img = Image.open(logo_path)
                # Algoritmo de escalado proporcional (ancho fijo 180px)
                base_width = 180
                w_percent = (base_width / float(pil_img.size[0]))
                h_size = int((float(pil_img.size[1]) * float(w_percent)))
                
                img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(base_width, h_size))
                self.lbl_logo = ctk.CTkLabel(self.sidebar, text="", image=img)
                self.lbl_logo.grid(row=0, column=0, pady=(30, 15), padx=20)
            except Exception as e:
                self.log(f"Error cargando imagen: {e}")
        else:
            ctk.CTkLabel(self.sidebar, text="[LOGO FALTANTE]", text_color="white").grid(row=0, column=0, pady=30)

        # B. Título de la App
        ctk.CTkLabel(self.sidebar, text="SaoPdfxlxx", font=("Roboto", 22, "bold"), text_color=COLOR_TEXT_SIDEBAR).grid(row=1, column=0, pady=(0, 20))

        # C. Botones de Control
        self.btn_folder = ctk.CTkButton(self.sidebar, text="SELECCIONAR CARPETA", command=self.select_folder,
                                        fg_color=COLOR_BTN_FOLDER, hover_color="#16a085", 
                                        font=("Roboto", 13, "bold"), height=40, cursor="hand2")
        self.btn_folder.grid(row=2, column=0, pady=15, padx=20, sticky="ew")

        self.btn_run = ctk.CTkButton(self.sidebar, text="INICIAR PROCESO", command=self.start_processing_thread, 
                                     fg_color=COLOR_BTN_RUN_DISABLED, state="disabled",
                                     font=("Roboto", 13, "bold"), height=40)
        self.btn_run.grid(row=3, column=0, pady=15, padx=20, sticky="ew")

        # D. Footer (Versión)
        ctk.CTkLabel(self.sidebar, text="Enterprise v1.0.0\nPowered by Sao Systems", 
                     font=("Roboto", 10), text_color="#95a5a6").grid(row=5, column=0, pady=20)


        # === ÁREA PRINCIPAL (DERECHA) ===
        self.main_area = ctk.CTkFrame(self, corner_radius=0, fg_color=COLOR_MAIN_BG)
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(2, weight=1) # Consola flexible

        # E. Header Principal
        self.lbl_title_main = ctk.CTkLabel(self.main_area, text="Panel de Control de Extracción", 
                                           font=("Roboto", 24, "bold"), text_color=COLOR_TEXT_MAIN)
        self.lbl_title_main.grid(row=0, column=0, pady=(30, 10), padx=30, sticky="w")

        # F. Estado y Barra de Progreso
        self.lbl_status = ctk.CTkLabel(self.main_area, text="Estado: Esperando selección de archivos...", 
                                       font=("Roboto", 14), text_color="#7f8c8d")
        self.lbl_status.grid(row=1, column=0, pady=(0, 5), padx=30, sticky="w")

        self.progress = ctk.CTkProgressBar(self.main_area, progress_color=COLOR_PROGRESS, height=15)
        self.progress.grid(row=2, column=0, pady=(0, 20), padx=30, sticky="new")
        self.progress.set(0)

        # G. Consola de Logs (Estilo Terminal Limpia)
        self.console_frame = ctk.CTkFrame(self.main_area, fg_color=COLOR_CONSOLE_BG, corner_radius=8, border_width=1, border_color="#bdc3c7")
        self.console_frame.grid(row=3, column=0, pady=(0, 30), padx=30, sticky="nsew")
        
        self.console = ctk.CTkTextbox(self.console_frame, font=("Consolas", 12), fg_color="transparent", text_color="#2c3e50")
        self.console.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.log("Sistema SaoPdfxlxx inicializado correctamente.")
        self.log("Esperando instrucciones del usuario...")

    # --- LÓGICA DEL SISTEMA ---

    def log(self, msg):
        """Escribe mensajes en la consola con timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_msg = f"[{timestamp}] > {msg}\n"
        
        # Usamos 'after' para asegurar que la UI se actualice desde el hilo principal
        self.after(0, lambda: self._update_console(full_msg))

    def _update_console(self, msg):
        self.console.configure(state="normal")
        self.console.insert("end", msg)
        self.console.see("end")
        self.console.configure(state="disabled")

    def select_folder(self):
        """Abre el diálogo para seleccionar carpeta."""
        path = filedialog.askdirectory()
        if path:
            self.folder_path = path
            folder_name = os.path.basename(path)
            self.log(f"Carpeta seleccionada: {folder_name}")
            self.lbl_status.configure(text=f"Carpeta lista: {folder_name}")
            
            # Activar botón de ejecución
            self.btn_run.configure(state="normal", fg_color=COLOR_BTN_RUN_ACTIVE, hover_color="#c0392b", cursor="hand2")

    def start_processing_thread(self):
        """Inicia el proceso en un Hilo (Thread) separado."""
        if not self.is_running:
            self.is_running = True
            
            # Bloquear interfaz
            self.btn_folder.configure(state="disabled")
            self.btn_run.configure(state="disabled", text="PROCESANDO...")
            self.lbl_status.configure(text="Ejecutando extracción masiva...", text_color=COLOR_PROGRESS)
            
            # Lanzar hilo daemon (se cierra si cierras la app)
            t = threading.Thread(target=self.run_process)
            t.daemon = True
            t.start()

    def run_process(self):
        """Lógica pesada de extracción (Backend)."""
        self.log("--- INICIANDO MOTOR DE EXTRACCIÓN ---")
        
        try:
            files = [f for f in os.listdir(self.folder_path) if f.lower().endswith('.pdf')]
            total = len(files)
        except Exception as e:
            self.log(f"[ERROR CRÍTICO] No se puede leer la carpeta: {e}")
            self.reset_ui()
            return
        
        if total == 0:
            self.log("[ALERTA] No se encontraron archivos PDF.")
            self.reset_ui()
            return

        results = []
        errors = 0

        for i, file in enumerate(files):
            # Actualizar barra de progreso
            progress_val = (i + 1) / total
            self.after(0, lambda p=progress_val: self.progress.set(p))
            
            # Procesar archivo
            full_path = os.path.join(self.folder_path, file)
            data = self.extractor.process_file(full_path)
            
            if "Error" in data:
                self.log(f"[FALLO] {file}: {data['Error']}")
                errors += 1
            else:
                data['Archivo Origen'] = file
                results.append(data)
                self.log(f"[OK] {file}")

        # Guardar Excel
        self.save_excel(results, total, errors)
        self.reset_ui()

    def save_excel(self, data, total, errors):
        """Genera el archivo Excel final."""
        if not data:
            self.log("--- PROCESO FINALIZADO SIN DATOS ---")
            return
        
        output_path = os.path.join(self.folder_path, "Reporte_SaoPdfxlxx.xlsx")
        df = pd.DataFrame(data)
        
        # Ordenar columnas
        cols = ["Nombre", "Dirección", "Fecha", "Archivo Origen"]
        df = df[[c for c in cols if c in df.columns]]

        try:
            df.to_excel(output_path, index=False)
            self.log(f"--- REPORTE GUARDADO: {output_path} ---")
            
            # Mostrar mensaje de éxito en el hilo principal
            self.after(0, lambda: messagebox.showinfo(
                "Proceso Completado", 
                f"Archivos procesados: {total}\nExitosos: {total - errors}\nErrores: {errors}\n\nExcel generado correctamente."
            ))
        except Exception as e:
            self.log(f"[ERROR EXCEL] No se pudo guardar: {e}")
            self.after(0, lambda: messagebox.showerror("Error de Escritura", "Cierre el archivo Excel si lo tiene abierto e intente de nuevo."))

    def reset_ui(self):
        """Restaura la interfaz al terminar."""
        self.is_running = False
        # Usamos 'after' para modificar UI desde el hilo
        self.after(0, lambda: self._restore_buttons())

    def _restore_buttons(self):
        self.btn_folder.configure(state="normal")
        self.btn_run.configure(state="normal", text="INICIAR PROCESO", fg_color=COLOR_BTN_RUN_ACTIVE)
        self.lbl_status.configure(text="Estado: Proceso finalizado. Esperando...", text_color="#7f8c8d")
        self.progress.set(0)
        self.log("--- Fin del flujo de trabajo ---")