import customtkinter as ctk
import json
import subprocess
import sys
import os

# SI HICISTE INGENIERIA INVERSA A ESTE PROGRAMA PARA VER EL CODIGO
# DE UNA VEZ TE AVISO QUE NO INTENTES CAMBIAR NADA PQ HAY COSAS QUE NI YO
# SE COMO ES QUE FUNCIONAN AUN ESTANDO MAL XD

# AQUI SOLO ENCONTRARAS LA LOGICA DE LA UI MAS NO OTRA COSA
# LA LOGICA DEL BOT ESTA EN: bot.py

# --- CONFIGURACIÓN DE TEMA ---
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

CONFIG_FILE = 'settings.json'

# Colores de la UI
COLOR_SIDEBAR = "#2b2d3e"
COLOR_SIDEBAR_HOVER = "#3a3d52"
COLOR_ACCENT = "#1f8ef1"
COLOR_BG_CONTENT = "#f4f6f9"
COLOR_TEXT_DARK = "#333333"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("L4D2 AI - Config")
        self.geometry("600x500")
        self.resizable(False, False)

        # Layout Principal: 2 Columnas (Sidebar | Contenido)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.config = self.load_config()
        self.entries = {} # Aquí se guardan todos los inputs de todas las pestañas

        # 1. CREAR SIDEBAR
        self.setup_sidebar()

        # 2. CREAR LAS 3 PANTALLAS (FRAMES)
        # Se crean todas al inicio pero solo se muestra una a la vez
        self.frame_standard = ctk.CTkScrollableFrame(self, fg_color=COLOR_BG_CONTENT, corner_radius=0)
        self.frame_aimbot = ctk.CTkScrollableFrame(self, fg_color=COLOR_BG_CONTENT, corner_radius=0)
        self.frame_visuals = ctk.CTkScrollableFrame(self, fg_color=COLOR_BG_CONTENT, corner_radius=0)

        self.setup_standard_content()
        self.setup_aimbot_content()
        self.setup_visuals_content()

        # 3. INICIAR EN LA PRIMERA PESTAÑA
        self.select_frame("Standard")

    def setup_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=COLOR_SIDEBAR)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        # Logo
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="AI Aimbot", 
                                     font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Botones de Navegación
        self.btn_standard = self.create_nav_btn("Standard", "Standard", 1)
        self.btn_aimbot = self.create_nav_btn("Aimbot Settings", "Aimbot", 2)
        self.btn_visuals = self.create_nav_btn("Visuals & Perf", "Visuals", 3)

        # Botón Guardar (Fijo abajo)
        self.btn_save = ctk.CTkButton(self.sidebar_frame, text="GUARDAR E INICIAR", 
                                      fg_color=COLOR_ACCENT, hover_color="#166db8",
                                      height=40, font=ctk.CTkFont(weight="bold"),
                                      command=self.save_and_run)
        self.btn_save.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

    def create_nav_btn(self, text, value, row):
        btn = ctk.CTkButton(self.sidebar_frame, text=text, fg_color="transparent", 
                            text_color="gray", hover_color=COLOR_SIDEBAR_HOVER, 
                            anchor="w", font=ctk.CTkFont(weight="bold"),
                            command=lambda: self.select_frame(value))
        btn.grid(row=row, column=0, sticky="ew", padx=10, pady=5)
        return btn

    # --- LÓGICA DE NAVEGACIÓN ---
    def select_frame(self, name):
        # 1. Resetear color botones
        self.btn_standard.configure(fg_color="transparent", text_color="gray")
        self.btn_aimbot.configure(fg_color="transparent", text_color="gray")
        self.btn_visuals.configure(fg_color="transparent", text_color="gray")

        # 2. Ocultar todos los frames
        self.frame_standard.grid_forget()
        self.frame_aimbot.grid_forget()
        self.frame_visuals.grid_forget()

        # 3. Mostrar el seleccionado y pintar botón
        if name == "Standard":
            self.frame_standard.grid(row=0, column=1, sticky="nsew")
            self.btn_standard.configure(fg_color="#3e4157", text_color="white")
        elif name == "Aimbot":
            self.frame_aimbot.grid(row=0, column=1, sticky="nsew")
            self.btn_aimbot.configure(fg_color="#3e4157", text_color="white")
        elif name == "Visuals":
            self.frame_visuals.grid(row=0, column=1, sticky="nsew")
            self.btn_visuals.configure(fg_color="#3e4157", text_color="white")

    # ==========================================
    # CONTENIDO PESTAÑA 1: STANDARD
    # ==========================================
    def setup_standard_content(self):
        self.create_section_title(self.frame_standard, "Configuración General")
        
        self.create_input_field(self.frame_standard, "Tecla Activación (ON/OFF)", "tecla_activacion")
        self.create_input_field(self.frame_standard, "Tecla Disparo (Aim)", "tecla_disparo")
        self.create_input_field(self.frame_standard, "Tecla Salir (Cerrar)", "tecla_salir")

        self.create_section_title(self.frame_standard, "Mecánicas de Defensa")
        self.create_input_field(self.frame_standard, "Umbral Deadstop (0.1 - 1.0)", "umbral_empujar")

    # ==========================================
    # CONTENIDO PESTAÑA 2: AIMBOT
    # ==========================================
    def setup_aimbot_content(self):
        self.create_section_title(self.frame_aimbot, "Sensibilidad de Rastreo")
        self.create_input_field(self.frame_aimbot, "Divisor X (Horizontal)", "divisor_x")
        self.create_input_field(self.frame_aimbot, "Divisor Y (Vertical)", "divisor_y")
        
        self.create_section_title(self.frame_aimbot, "Ajustes de Puntería")
        self.create_input_field(self.frame_aimbot, "Offset Cabeza (píxeles)", "offset_cabeza")
        self.create_input_field(self.frame_aimbot, "Memoria (Frames de predicción)", "paciencia_memoria")
        
        self.create_section_title(self.frame_aimbot, "Inteligencia Artificial")
        self.create_input_field(self.frame_aimbot, "Confianza Mínima (0.1 - 1.0)", "confidencia")

    # ==========================================
    # CONTENIDO PESTAÑA 3: VISUALS
    # ==========================================
    def setup_visuals_content(self):
        self.create_section_title(self.frame_visuals, "Rendimiento y Pantalla")

        # Switch Ventana
        self.create_switch_field(self.frame_visuals, "Mostrar Ventana de Depuración", "mostrar_ventana")

        # Slider Resolución
        self.create_section_title(self.frame_visuals, "Resolución de Visión (IA)")
        
        res_container = ctk.CTkFrame(self.frame_visuals, fg_color="white", corner_radius=6)
        res_container.pack(fill="x", padx=20, pady=5)

        self.lbl_res_val = ctk.CTkLabel(res_container, text="Estado: ...", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_res_val.pack(anchor="w", padx=15, pady=(10, 5))

        current_res = self.config.get("tamano_captura", 416)
        self.slider_res = ctk.CTkSlider(res_container, from_=320, to=640, number_of_steps=10, command=self.update_res_ui)
        self.slider_res.set(current_res)
        self.slider_res.pack(fill="x", padx=15, pady=(0, 15))
        
        self.update_res_ui(current_res) # Init color

    # --- HELPERS UI ---
    def create_section_title(self, parent, text):
        lbl = ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=16, weight="bold"), 
                           text_color=COLOR_ACCENT, anchor="w")
        lbl.pack(fill="x", padx=20, pady=(20, 10))

    def create_input_field(self, parent, label, key):
        frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=6)
        frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(frame, text=label.upper(), font=ctk.CTkFont(size=11, weight="bold"), 
                     text_color="gray").pack(anchor="w", padx=15, pady=(10, 0))

        entry = ctk.CTkEntry(frame, border_width=0, fg_color="#f0f2f5", text_color="black", height=35)
        entry.insert(0, str(self.config.get(key, "")))
        entry.pack(fill="x", padx=15, pady=(5, 15))
        self.entries[key] = entry

    def create_switch_field(self, parent, label, key):
        frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=6)
        frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(frame, text=label.upper(), font=ctk.CTkFont(size=11, weight="bold"), 
                     text_color="gray").pack(side="left", padx=15, pady=15)
        
        var = ctk.BooleanVar(value=self.config.get(key, True))
        ctk.CTkSwitch(frame, text="", variable=var, progress_color=COLOR_ACCENT).pack(side="right", padx=15)
        self.entries[key] = var

    def update_res_ui(self, val):
        val = int(val)
        if val <= 416:
            txt, col = f"{val} px - EXCELENTE", "#2CC985"
        elif val <= 512:
            txt, col = f"{val} px - EQUILIBRADO", "#f39c12"
        else:
            txt, col = f"{val} px - PELIGRO (LAG)", "#e74c3c"
        
        self.lbl_res_val.configure(text=txt, text_color=col)
        self.slider_res.configure(progress_color=col, button_color=col)
        self.config["tamano_captura"] = val # Update temp config

    # --- CARGA Y GUARDADO ---
    def load_config(self):
        default = {
            "tecla_activacion": "t", "tecla_disparo": "z", "tecla_salir": "q",
            "divisor_x": 10.0, "divisor_y": 9.0, "offset_cabeza": -5,
            "paciencia_memoria": 15, "umbral_empujar": 0.20, "confidencia": 0.25,
            "mostrar_ventana": True, "tamano_captura": 416
        }
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f: return {**default, **json.load(f)}
            except: pass
        return default

    def save_and_run(self):
        try:
            new_config = self.config.copy()
            # 1. Recoger inputs de texto/switches
            for key, widget in self.entries.items():
                if isinstance(widget, ctk.CTkEntry):
                    val = widget.get()
                    try: 
                        if "." in val: val = float(val)
                        else: val = int(val)
                    except: pass
                    new_config[key] = val
                elif isinstance(widget, ctk.BooleanVar):
                    new_config[key] = widget.get()
            
            # 2. Recoger slider resolucion
            new_config["tamano_captura"] = int(self.slider_res.get())

            with open(CONFIG_FILE, 'w') as f: json.dump(new_config, f, indent=4)
            
            self.iconify()
            subprocess.Popen([sys.executable, 'bot.py'])
        except Exception as e: print(e)

if __name__ == "__main__":
    app = App()
    app.mainloop()