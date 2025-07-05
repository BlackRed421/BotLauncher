import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
import os
import sys
import json
import subprocess
from threading import Thread
import requests
from PIL import Image, ImageTk
import io
import re
import datetime

# =============================================================================
# CONFIGURAÇÃO E TEMA
# =============================================================================
APP_NAME = "PoketLauncher"
APP_VERSION = "4.3"

THEME = {
    "color": {
        "background": "#111111",
        "frame_bg": "#1C1C1C",
        "card_bg": "#2A2A2A",
        "card_hover": "#333333",
        "button": "#3D3D3D",
        "button_hover": "#4A4A4A",
        "accent_primary": "#FFC700",
        "accent_primary_hover": "#FFD233",
        "accent_secondary": "#BDBDBD",
        "accent_secondary_hover": "#E0E0E0",
        "text": "#F5F5F5",
        "text_dark": "#9E9E9E",
        "error": "#E53935",
        "error_hover": "#C62828",
        "outline": "#555555"
    },
    "font": {
        "main": ("Roboto", 14),
        "title": ("Impact", 40, "bold"),
        "card_title": ("Roboto", 20, "bold"),
        "card_subtitle": ("Roboto", 13),
        "button": ("Roboto", 14, "bold"),
        "toast": ("Roboto", 12, "bold"),
        "code": ("Consolas", 14)
    }
}

# Lista de Pokémon para o dropdown (Nome e ID para a URL do GIF)
POKEMON_LIST = [
    {"id": 1, "name": "bulbasaur"}, {"id": 2, "name": "ivysaur"}, {"id": 3, "name": "venusaur"},
    {"id": 4, "name": "charmander"}, {"id": 5, "name": "charmeleon"}, {"id": 6, "name": "charizard"},
    {"id": 7, "name": "squirtle"}, {"id": 8, "name": "wartortle"}, {"id": 9, "name": "blastoise"},
    {"id": 10, "name": "caterpie"}, {"id": 11, "name": "metapod"}, {"id": 12, "name": "butterfree"},
    {"id": 13, "name": "weedle"}, {"id": 14, "name": "kakuna"}, {"id": 15, "name": "beedrill"},
    {"id": 16, "name": "pidgey"}, {"id": 17, "name": "pidgeotto"}, {"id": 18, "name": "pidgeot"},
    {"id": 19, "name": "rattata"}, {"id": 20, "name": "raticate"}, {"id": 21, "name": "spearow"},
    {"id": 22, "name": "fearow"}, {"id": 23, "name": "ekans"}, {"id": 24, "name": "arbok"},
    {"id": 25, "name": "pikachu"}, {"id": 26, "name": "raichu"}, {"id": 27, "name": "sandshrew"},
    {"id": 28, "name": "sandslash"}, {"id": 29, "name": "nidoran-f"}, {"id": 30, "name": "nidorina"},
    {"id": 31, "name": "nidoqueen"}, {"id": 32, "name": "nidoran-m"}, {"id": 33, "name": "nidorino"},
    {"id": 34, "name": "nidoking"}, {"id": 35, "name": "clefairy"}, {"id": 36, "name": "clefable"},
    {"id": 37, "name": "vulpix"}, {"id": 38, "name": "ninetales"}, {"id": 39, "name": "jigglypuff"},
    {"id": 40, "name": "wigglytuff"}, {"id": 41, "name": "zubat"}, {"id": 42, "name": "golbat"},
    {"id": 43, "name": "oddish"}, {"id": 44, "name": "gloom"}, {"id": 45, "name": "vileplume"},
    {"id": 46, "name": "paras"}, {"id": 47, "name": "parasect"}, {"id": 48, "name": "venonat"},
    {"id": 49, "name": "venomoth"}, {"id": 50, "name": "diglett"}, {"id": 51, "name": "dugtrio"},
    {"id": 52, "name": "meowth"}, {"id": 53, "name": "persian"}, {"id": 54, "name": "psyduck"},
    {"id": 55, "name": "golduck"}, {"id": 56, "name": "mankey"}, {"id": 57, "name": "primeape"},
    {"id": 58, "name": "growlithe"}, {"id": 59, "name": "arcanine"}, {"id": 60, "name": "poliwag"},
    {"id": 61, "name": "poliwhirl"}, {"id": 62, "name": "poliwrath"}, {"id": 63, "name": "abra"},
    {"id": 64, "name": "kadabra"}, {"id": 65, "name": "alakazam"}, {"id": 66, "name": "machop"},
    {"id": 67, "name": "machoke"}, {"id": 68, "name": "machamp"}, {"id": 69, "name": "bellsprout"},
    {"id": 70, "name": "weepinbell"}, {"id": 71, "name": "victreebel"}, {"id": 72, "name": "tentacool"},
    {"id": 73, "name": "tentacruel"}, {"id": 74, "name": "geodude"}, {"id": 75, "name": "graveler"},
    {"id": 76, "name": "golem"}, {"id": 77, "name": "ponyta"}, {"id": 78, "name": "rapidash"},
    {"id": 79, "name": "slowpoke"}, {"id": 80, "name": "slowbro"}, {"id": 81, "name": "magnemite"},
    {"id": 82, "name": "magneton"}, {"id": 83, "name": "farfetchd"}, {"id": 84, "name": "doduo"},
    {"id": 85, "name": "dodrio"}, {"id": 86, "name": "seel"}, {"id": 87, "name": "dewgong"},
    {"id": 88, "name": "grimer"}, {"id": 89, "name": "muk"}, {"id": 90, "name": "shellder"},
    {"id": 91, "name": "cloyster"}, {"id": 92, "name": "gastly"}, {"id": 93, "name": "haunter"},
    {"id": 94, "name": "gengar"}, {"id": 95, "name": "onix"}, {"id": 96, "name": "drowzee"},
    {"id": 97, "name": "hypno"}, {"id": 98, "name": "krabby"}, {"id": 99, "name": "kingler"},
    {"id": 100, "name": "voltorb"}, {"id": 101, "name": "electrode"}, {"id": 102, "name": "exeggcute"},
    {"id": 103, "name": "exeggutor"}, {"id": 104, "name": "cubone"}, {"id": 105, "name": "marowak"},
    {"id": 106, "name": "hitmonlee"}, {"id": 107, "name": "hitmonchan"}, {"id": 108, "name": "lickitung"},
    {"id": 109, "name": "koffing"}, {"id": 110, "name": "weezing"}, {"id": 111, "name": "rhyhorn"},
    {"id": 112, "name": "rhydon"}, {"id": 113, "name": "chansey"}, {"id": 114, "name": "tangela"},
    {"id": 115, "name": "kangaskhan"}, {"id": 116, "name": "horsea"}, {"id": 117, "name": "seadra"},
    {"id": 118, "name": "goldeen"}, {"id": 119, "name": "seaking"}, {"id": 120, "name": "staryu"},
    {"id": 121, "name": "starmie"}, {"id": 122, "name": "mr-mime"}, {"id": 123, "name": "scyther"},
    {"id": 124, "name": "jynx"}, {"id": 125, "name": "electabuzz"}, {"id": 126, "name": "magmar"},
    {"id": 127, "name": "pinsir"}, {"id": 128, "name": "tauros"}, {"id": 129, "name": "magikarp"},
    {"id": 130, "name": "gyarados"}, {"id": 131, "name": "lapras"}, {"id": 132, "name": "ditto"},
    {"id": 133, "name": "eevee"}, {"id": 134, "name": "vaporeon"}, {"id": 135, "name": "jolteon"},
    {"id": 136, "name": "flareon"}, {"id": 137, "name": "porygon"}, {"id": 138, "name": "omanyte"},
    {"id": 139, "name": "omastar"}, {"id": 140, "name": "kabuto"}, {"id": 141, "name": "kabutops"},
    {"id": 142, "name": "aerodactyl"}, {"id": 143, "name": "snorlax"}, {"id": 144, "name": "articuno"},
    {"id": 145, "name": "zapdos"}, {"id": 146, "name": "moltres"}, {"id": 147, "name": "dratini"},
    {"id": 148, "name": "dragonair"}, {"id": 149, "name": "dragonite"}, {"id": 150, "name": "mewtwo"},
    {"id": 151, "name": "mew"}
]
POKEMON_NAMES = [p['name'].capitalize() for p in POKEMON_LIST]

# =============================================================================
# CLASSES E FUNÇÕES UTILITÁRIAS
# =============================================================================
def get_persistent_data_dir():
    app_name = "KoreNexus"
    if sys.platform == "win32":
        base_dir = os.path.join(os.environ['APPDATA'], app_name)
    else:
        base_dir = os.path.join(os.path.expanduser('~'), f'.{app_name}')
    os.makedirs(base_dir, exist_ok=True)
    return base_dir

DATA_DIR = get_persistent_data_dir()
BOTS_FILE = os.path.join(DATA_DIR, 'bots.json')
CONFIG_FILE = os.path.join(DATA_DIR, 'config.json')

def initialize_files():
    if not os.path.exists(BOTS_FILE):
        with open(BOTS_FILE, 'w', encoding='utf-8') as f: json.dump([], f)
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({"client_bat_path": "", "xml_path": "", "openkore_path": ""}, f)

def load_data(file_path, is_json=True):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f) if is_json else f.read()
    except (FileNotFoundError, json.JSONDecodeError):
        if 'bots' in os.path.basename(file_path): return []
        if 'config' in os.path.basename(file_path): return {}
        return None

def save_data(file_path, data, is_json=True):
    with open(file_path, 'w', encoding='utf-8') as f:
        if is_json:
            json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            f.write(data)

class AnimatedImageLabel(ctk.CTkLabel):
    def __init__(self, master, size, **kwargs):
        super().__init__(master, **kwargs)
        self.size = size
        self.frames = []
        self.frame_index = 0
        self.delay = 100
        self.is_animating = False
        self.after_id = None
        self.configure(text="")

    def load_gif_from_data(self, gif_data):
        try:
            gif_image = Image.open(io.BytesIO(gif_data))
            self.frames = []
            for i in range(gif_image.n_frames):
                gif_image.seek(i)
                frame = gif_image.copy().convert("RGBA")
                frame.thumbnail(self.size, Image.Resampling.LANCZOS)
                self.frames.append(ImageTk.PhotoImage(frame))
            
            self.delay = gif_image.info.get('duration', 100)
            self.frame_index = 0
            
            if len(self.frames) > 1:
                self.is_animating = True
                self.animate()
            else:
                self.is_animating = False
                self.configure(image=self.frames[0])
        except Exception:
            self.configure(text="?", image=None)

    def animate(self):
        if not self.is_animating or not self.frames:
            return
        self.configure(image=self.frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.after_id = self.after(self.delay, self.animate)

    def stop_animation(self):
        self.is_animating = False
        if self.after_id:
            self.after_cancel(self.after_id)

class ThemedToplevel(ctk.CTkToplevel):
    def __init__(self, master, title, geometry):
        super().__init__(master)
        self.title(title)
        self.geometry(geometry)
        self.transient(master)
        self.grab_set()
        self.configure(fg_color=THEME["color"]["background"])
        self.after(20, self._center_window)

    def _center_window(self):
        try:
            self.update_idletasks()
            master = self.master
            x = master.winfo_x() + (master.winfo_width() - self.winfo_width()) // 2
            y = master.winfo_y() + (master.winfo_height() - self.winfo_height()) // 2
            self.geometry(f"+{x}+{y}")
        except Exception:
            pass

class SettingsWindow(ThemedToplevel):
    def __init__(self, master):
        super().__init__(master, "Configurações", "700x300")
        self.master_app = master
        config = self.master_app.config

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(pady=20, padx=20, fill="x", expand=True)
        ctk.CTkLabel(main_frame, text="CONFIGURAÇÕES DE CAMINHOS", font=("Roboto", 18, "bold"), text_color=THEME["color"]["accent_primary"]).pack(anchor="w", pady=(0, 20))

        path_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        path_frame.pack(fill="x", expand=True)
        path_frame.grid_columnconfigure(1, weight=1)

        def create_path_row(row, text, var, cmd):
            ctk.CTkLabel(path_frame, text=text, text_color=THEME["color"]["text"], font=THEME["font"]["main"]).grid(row=row, column=0, padx=(0, 10), pady=10, sticky="w")
            ctk.CTkEntry(path_frame, textvariable=var, fg_color=THEME["color"]["card_bg"], border_width=0, corner_radius=8).grid(row=row, column=1, padx=(0, 10), sticky="ew")
            ctk.CTkButton(path_frame, text="Procurar...", width=100, command=cmd, fg_color=THEME["color"]["button"], hover_color=THEME["color"]["button_hover"], corner_radius=8).grid(row=row, column=2, sticky="e")

        self.client_bat_path_var = ctk.StringVar(value=config.get("client_bat_path", ""))
        self.xml_path_var = ctk.StringVar(value=config.get("xml_path", ""))
        self.kore_path_var = ctk.StringVar(value=config.get("openkore_path", ""))
        create_path_row(0, "Cliente (.bat):", self.client_bat_path_var, self.browse_client_bat_file)
        create_path_row(1, "Clientes (XML):", self.xml_path_var, self.browse_xml_file)
        create_path_row(2, "Pasta OpenKore:", self.kore_path_var, self.browse_kore_folder)
        ctk.CTkButton(self, text="Salvar e Fechar", command=self.save_and_close, fg_color=THEME["color"]["accent_primary"], hover_color=THEME["color"]["accent_primary_hover"], text_color="#000000", corner_radius=8, height=35, font=THEME["font"]["button"]).pack(pady=20, padx=20)

    def browse_client_bat_file(self):
        path = filedialog.askopenfilename(title="Selecione o arquivo .bat do Cliente", filetypes=[("Batch files", "*.bat"), ("All files", "*.*")])
        if path: self.client_bat_path_var.set(path)
    def browse_xml_file(self):
        path = filedialog.askopenfilename(title="Selecione o Arquivo XML", filetypes=[("XML files", "*.xml"), ("All files", "*.*")])
        if path: self.xml_path_var.set(path)
    def browse_kore_folder(self):
        path = filedialog.askdirectory(title="Selecione a Pasta Principal do OpenKore")
        if path: self.kore_path_var.set(path)
    def save_and_close(self):
        new_config = {"client_bat_path": self.client_bat_path_var.get(), "xml_path": self.xml_path_var.get(), "openkore_path": self.kore_path_var.get()}
        save_data(CONFIG_FILE, new_config)
        self.master_app.load_config()
        self.master_app.show_toast("Configurações salvas!")
        self.master_app.load_macros_from_disk()
        self.destroy()

class AddBotWindow(ThemedToplevel):
    def __init__(self, master):
        super().__init__(master, "Adicionar Novo Bot", "450x450")
        self.master_app = master
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        ctk.CTkLabel(frame, text="ADICIONAR NOVO BOT", font=("Roboto", 18, "bold"), text_color=THEME["color"]["accent_primary"]).pack(anchor="w", pady=(0, 20))

        ctk.CTkLabel(frame, text="Apelido (Identificação):", text_color=THEME["color"]["text"], font=THEME["font"]["main"]).pack(anchor="w", padx=5)
        self.nickname_entry = ctk.CTkEntry(frame, width=400, fg_color=THEME["color"]["card_bg"], border_width=0, corner_radius=8)
        self.nickname_entry.pack(fill="x", pady=(2, 15))

        ctk.CTkLabel(frame, text="Nome do Personagem (para config):", text_color=THEME["color"]["text"], font=THEME["font"]["main"]).pack(anchor="w", padx=5)
        self.char_name_entry = ctk.CTkEntry(frame, width=400, fg_color=THEME["color"]["card_bg"], border_width=0, corner_radius=8)
        self.char_name_entry.pack(fill="x", pady=(2, 15))

        ctk.CTkLabel(frame, text="Pokémon:", text_color=THEME["color"]["text"], font=THEME["font"]["main"]).pack(anchor="w", padx=5)
        self.pokemon_combo = ctk.CTkComboBox(frame, values=POKEMON_NAMES, width=400, fg_color=THEME["color"]["card_bg"], border_width=0, corner_radius=8, dropdown_fg_color=THEME["color"]["card_bg"], button_color=THEME["color"]["button"], button_hover_color=THEME["color"]["button_hover"])
        self.pokemon_combo.pack(fill="x", pady=(2, 15))
        self.pokemon_combo.set("Selecione um Pokémon")

        ctk.CTkLabel(frame, text="Executável do Kore:", text_color=THEME["color"]["text"], font=THEME["font"]["main"]).pack(anchor="w", padx=5)
        self.executable_menu = ctk.CTkOptionMenu(frame, values=["wxstart.exe", "start.exe"], corner_radius=8, fg_color=THEME["color"]["card_bg"], button_color=THEME["color"]["button"], button_hover_color=THEME["color"]["button_hover"], dropdown_fg_color=THEME["color"]["card_bg"])
        self.executable_menu.pack(fill="x", pady=(2, 20))
        
        ctk.CTkButton(self, text="Adicionar Bot", command=self.add_bot, fg_color=THEME["color"]["accent_primary"], hover_color=THEME["color"]["accent_primary_hover"], text_color="#000000", corner_radius=8, height=35, font=THEME["font"]["button"]).pack(pady=(0, 20))

    def add_bot(self):
        nickname = self.nickname_entry.get()
        char_name = self.char_name_entry.get()
        pokemon_name_cap = self.pokemon_combo.get()

        if not all([nickname, char_name]) or pokemon_name_cap == "Selecione um Pokémon":
            return self.master_app.show_toast("Erro: Preencha todos os campos!", error=True)
        
        pokemon_name_lower = pokemon_name_cap.lower()
        pokemon_id = POKEMON_NAMES.index(pokemon_name_cap) + 1

        new_bot_data = {
            "nickname": nickname, 
            "characterName": char_name, 
            "pokemon_name": pokemon_name_lower,
            "pokemon_id": pokemon_id,
            "executable": self.executable_menu.get()
        }
        bots = load_data(BOTS_FILE)
        bots.append(new_bot_data)
        save_data(BOTS_FILE, bots)
        self.master_app.refresh_bot_grid()
        self.master_app.show_toast(f"Bot '{nickname}' adicionado!")
        self.destroy()

# =============================================================================
# CLASSE PRINCIPAL DA APLICAÇÃO
# =============================================================================
class KoreNexusApp(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=THEME["color"]["background"])
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        self.config = {}
        self.current_macro_path = None
        self.macro_widgets = {}
        self.settings_win = None
        self.add_bot_win = None
        self.toast_label = None
        self.toast_after_id = None
        
        initialize_files()
        self.load_config()
        self.build_ui()
        self.load_macros_from_disk()
        self.check_for_legacy_macros_import()
        
    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Header ---
        header_frame = ctk.CTkFrame(self, fg_color=THEME["color"]["background"], height=70)
        header_frame.grid(row=0, column=0, padx=30, pady=(10, 0), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header_frame, text=APP_NAME.upper(), font=THEME["font"]["title"], text_color=THEME["color"]["text"]).pack(side="left", padx=(10, 0), pady=10)
        
        # --- Main Content Frame with Tabs ---
        main_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_content_frame.grid(row=1, column=0, padx=30, pady=20, sticky="nsew")
        main_content_frame.grid_rowconfigure(0, weight=1)
        main_content_frame.grid_columnconfigure(0, weight=1)
        
        self.tab_view = ctk.CTkTabview(main_content_frame,
                                       fg_color=THEME["color"]["frame_bg"],
                                       segmented_button_fg_color=THEME["color"]["frame_bg"],
                                       segmented_button_selected_color=THEME["color"]["card_bg"],
                                       segmented_button_selected_hover_color=THEME["color"]["card_hover"],
                                       segmented_button_unselected_color=THEME["color"]["frame_bg"],
                                       segmented_button_unselected_hover_color=THEME["color"]["button"],
                                       text_color=THEME["color"]["text"],
                                       corner_radius=12,
                                       border_color=THEME["color"]["outline"],
                                       border_width=2)
        self.tab_view.grid(row=0, column=0, sticky="nsew")
        self.tab_view.add("Bot Launcher")
        self.tab_view.add("Macro Manager")
        self.tab_view._segmented_button.configure(font=ctk.CTkFont(size=14, weight="bold"))

        self.setup_launcher_ui(self.tab_view.tab("Bot Launcher"))
        self.setup_macros_ui(self.tab_view.tab("Macro Manager"))
        
    def load_config(self):
        self.config = load_data(CONFIG_FILE)

    # =========================================================================
    # SEÇÃO: BOT LAUNCHER
    # =========================================================================
    def setup_launcher_ui(self, tab):
        tab.configure(fg_color="transparent")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        toolbar = ctk.CTkFrame(tab, fg_color="transparent")
        toolbar.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        
        ctk.CTkButton(toolbar, text="Adicionar Bot", command=self.open_add_bot_window, fg_color=THEME["color"]["accent_primary"], text_color="#000000", hover_color=THEME["color"]["accent_primary_hover"], font=THEME["font"]["button"]).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Lançar Cliente", command=self.launch_client, fg_color=THEME["color"]["button"], hover_color=THEME["color"]["button_hover"], font=THEME["font"]["main"]).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Abrir XML", command=self.launch_xml, fg_color=THEME["color"]["button"], hover_color=THEME["color"]["button_hover"], font=THEME["font"]["main"]).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Configurações", command=self.open_settings_window, fg_color=THEME["color"]["button"], hover_color=THEME["color"]["button_hover"]).pack(side="right", padx=5)

        self.bot_scroll_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        self.bot_scroll_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.bot_scroll_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.refresh_bot_grid()

    def refresh_bot_grid(self):
        for widget in self.bot_scroll_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame): # Assuming cards are in frames
                for sub_widget in widget.winfo_children():
                     if isinstance(sub_widget, AnimatedImageLabel):
                        sub_widget.stop_animation()
            widget.destroy()
        bots = load_data(BOTS_FILE)
        if not bots:
            ctk.CTkLabel(self.bot_scroll_frame, text="Nenhum bot encontrado.\nClique em 'Adicionar Bot' para começar.", font=THEME["font"]["main"], text_color=THEME["color"]["text_dark"]).pack(pady=50)
        else:
            for i, bot_data in enumerate(bots):
                self.create_bot_card(bot_data, *divmod(i, 4))

    def create_bot_card(self, bot_data, row, col):
        card_glow = ctk.CTkFrame(self.bot_scroll_frame, fg_color="transparent", border_color=THEME["color"]["card_bg"], border_width=2, corner_radius=16)
        card_glow.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

        card = ctk.CTkFrame(card_glow, fg_color=THEME["color"]["card_bg"], corner_radius=12)
        card.pack(fill="both", expand=True, padx=2, pady=2)

        def on_enter(e): card_glow.configure(border_color=THEME["color"]["accent_primary"])
        def on_leave(e): card_glow.configure(border_color=THEME["color"]["card_bg"])

        card_glow.bind("<Enter>", on_enter)
        card_glow.bind("<Leave>", on_leave)

        image_label = AnimatedImageLabel(card, size=(120, 120), fg_color="transparent")
        image_label.pack(pady=(20, 15), padx=15)
        
        pokemon_id = bot_data.get("pokemon_id")
        if not pokemon_id:
            pokemon_name = bot_data.get("pokemon", "pikachu").lower()
            try:
                pokemon_id = [p for p in POKEMON_LIST if p['name'] == pokemon_name][0]['id']
            except IndexError:
                pokemon_id = 25 # Default to Pikachu

        Thread(target=self.load_pokemon_image, args=(pokemon_id, image_label), daemon=True).start()

        ctk.CTkLabel(card, text=bot_data.get('nickname', 'Sem nome'), font=THEME["font"]["card_title"], text_color=THEME["color"]["text"]).pack(pady=(0, 2), padx=15)
        ctk.CTkLabel(card, text=bot_data.get('characterName', ''), font=THEME["font"]["card_subtitle"], text_color=THEME["color"]["text_dark"]).pack(pady=(0, 20), padx=15)

        ctk.CTkButton(card, text="Iniciar", height=40, font=THEME["font"]["button"], command=lambda b=bot_data: self.launch_bot(b), fg_color=THEME["color"]["accent_primary"], hover_color=THEME["color"]["accent_primary_hover"], text_color="#000000").pack(pady=(0, 8), padx=15, fill="x")
        ctk.CTkButton(card, text="Config", height=35, command=lambda b=bot_data: self.open_bot_config(b), fg_color="transparent", border_color=THEME["color"]["outline"], hover_color=THEME["color"]["button_hover"], border_width=2).pack(pady=(0, 8), padx=15, fill="x")
        ctk.CTkButton(card, text="Excluir", height=35, command=lambda b=bot_data: self.delete_bot(b), fg_color="transparent", text_color=THEME["color"]["text_dark"], hover_color=THEME["color"]["error_hover"]).pack(pady=(0, 20), padx=15, fill="x")

    def load_pokemon_image(self, pokemon_id, image_label):
        try:
            url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/{pokemon_id}.gif"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            gif_data = response.content
            self.after(0, image_label.load_gif_from_data, gif_data)
        except Exception:
            self.after(0, lambda: image_label.configure(text="X", font=THEME["font"]["title"]))

    def delete_bot(self, bot_to_delete):
        if not messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o bot '{bot_to_delete.get('nickname')}'?"):
            return
        bots = [b for b in load_data(BOTS_FILE) if b.get('nickname') != bot_to_delete.get('nickname')]
        save_data(BOTS_FILE, bots)
        self.refresh_bot_grid()
        self.show_toast(f"Bot '{bot_to_delete.get('nickname')}' deletado.")

    def launch_client(self):
        client_bat_path = self.config.get("client_bat_path")
        if not client_bat_path or not os.path.isfile(client_bat_path):
            self.show_toast("Erro: Arquivo .bat do cliente não configurado.", error=True)
            return self.open_settings_window()
        try:
            Thread(target=lambda: subprocess.Popen([client_bat_path], cwd=os.path.dirname(client_bat_path), creationflags=subprocess.CREATE_NO_WINDOW), daemon=True).start()
            self.show_toast("Iniciando cliente...")
        except Exception as e: self.show_toast(f"Erro ao iniciar o cliente: {e}", error=True)

    def launch_xml(self):
        path = self.config.get("xml_path")
        if not path or not os.path.exists(path):
            self.show_toast("Erro: Caminho do arquivo XML não configurado.", error=True)
            return self.open_settings_window()
        self.open_file_with_default_app(path)

    def launch_bot(self, bot_data):
        kore_path = self.config.get("openkore_path")
        if not kore_path or not os.path.isdir(kore_path):
            self.show_toast("Erro: Pasta do OpenKore não configurada.", error=True)
            return self.open_settings_window()
        
        char_name, executable = bot_data['characterName'], bot_data['executable']
        config_file = f"config_{char_name}.txt"
        config_path = os.path.join(kore_path, 'control', config_file)
        executable_path = os.path.join(kore_path, executable)

        if not os.path.exists(config_path): return self.show_toast(f"Config não encontrado: {config_file}", error=True)
        if not os.path.exists(executable_path): return self.show_toast(f"Executável '{executable}' não encontrado.", error=True)
        
        try:
            config_arg = f"--config={os.path.join('control', config_file)}"
            Thread(target=lambda: subprocess.Popen([executable_path, config_arg], cwd=kore_path, creationflags=subprocess.CREATE_NO_WINDOW), daemon=True).start()
            self.show_toast(f"Iniciando bot '{bot_data.get('nickname', char_name)}'...")
        except Exception as e: self.show_toast(f"Erro ao iniciar o bot: {e}", error=True)

    def open_bot_config(self, bot_data):
        kore_path = self.config.get("openkore_path")
        if not kore_path or not os.path.isdir(kore_path):
            self.show_toast("Erro: Pasta do OpenKore não configurada.", error=True)
            return self.open_settings_window()
        
        config_file_path = os.path.join(kore_path, 'control', f"config_{bot_data['characterName']}.txt")
        if not os.path.exists(config_file_path):
            return self.show_toast(f"Arquivo de config não encontrado.", error=True)
        self.open_file_with_default_app(config_file_path)

    # =========================================================================
    # SEÇÃO: MACRO MANAGER
    # =========================================================================
    def get_macro_paths(self):
        kore_path = self.config.get("openkore_path")
        if not kore_path or not os.path.isdir(kore_path):
            return None, None, None, None, None

        macros_dir = os.path.join(kore_path, "KoreNexus_Macros")
        automacros_subdir = os.path.join(macros_dir, "automacros")
        macros_subdir = os.path.join(macros_dir, "macros")
        backups_subdir = os.path.join(macros_dir, "backups")
        main_macro_file = os.path.join(kore_path, "macros.txt")
        
        for path in [macros_dir, automacros_subdir, macros_subdir, backups_subdir]:
            os.makedirs(path, exist_ok=True)
            
        return automacros_subdir, macros_subdir, backups_subdir, main_macro_file, macros_dir

    def setup_macros_ui(self, tab):
        tab.configure(fg_color="transparent")
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(1, weight=1)

        toolbar = ctk.CTkFrame(tab, fg_color="transparent")
        toolbar.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky="ew")
        
        ctk.CTkButton(toolbar, text="Compilar", font=THEME["font"]["button"], fg_color=THEME["color"]["accent_primary"], text_color="#000000", hover_color=THEME["color"]["accent_primary_hover"], command=self.compile_main_macro_file).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Abrir Original", command=self.open_original_macro_file, fg_color=THEME["color"]["button"], hover_color=THEME["color"]["button_hover"]).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Importar de macros.txt", command=self.import_from_main_file, fg_color=THEME["color"]["button"], hover_color=THEME["color"]["button_hover"]).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Adicionar Novo Macro", command=self.add_new_macro_dialog, fg_color=THEME["color"]["button"], hover_color=THEME["color"]["button_hover"]).pack(side="right", padx=5)

        main_frame = ctk.CTkFrame(tab, fg_color="transparent")
        main_frame.grid(row=1, column=0, columnspan=2, padx=15, pady=15, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1, minsize=300)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_rowconfigure(0, weight=1)

        # --- Painel Esquerdo (Listas) ---
        list_panel = ctk.CTkFrame(main_frame, fg_color="transparent")
        list_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        list_panel.grid_rowconfigure(1, weight=1)
        list_panel.grid_rowconfigure(3, weight=1)
        list_panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(list_panel, text="AUTOMACROS", font=ctk.CTkFont(size=16, weight="bold"), text_color=THEME["color"]["text"]).grid(row=0, column=0, padx=5, pady=(0,5), sticky="w")
        self.automacros_frame = ctk.CTkScrollableFrame(list_panel, fg_color=THEME["color"]["card_bg"], corner_radius=8)
        self.automacros_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        ctk.CTkLabel(list_panel, text="MACROS", font=ctk.CTkFont(size=16, weight="bold"), text_color=THEME["color"]["text"]).grid(row=2, column=0, padx=5, pady=(10,5), sticky="w")
        self.macros_frame = ctk.CTkScrollableFrame(list_panel, fg_color=THEME["color"]["card_bg"], corner_radius=8)
        self.macros_frame.grid(row=3, column=0, sticky="nsew", padx=0, pady=0)

        # --- Painel Direito (Editor) ---
        editor_panel = ctk.CTkFrame(main_frame, fg_color="transparent")
        editor_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        editor_panel.grid_rowconfigure(1, weight=1)
        editor_panel.grid_columnconfigure(0, weight=1)

        editor_header_frame = ctk.CTkFrame(editor_panel, fg_color="transparent")
        editor_header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        self.editing_label = ctk.CTkLabel(editor_header_frame, text="Selecione um macro para editar...", text_color=THEME["color"]["text_dark"], anchor="w")
        self.editing_label.pack(side="left")

        self.save_button = ctk.CTkButton(editor_header_frame, text="Salvar Alterações", state="disabled", command=self.save_current_macro, fg_color=THEME["color"]["button"], hover_color=THEME["color"]["button_hover"])
        self.save_button.pack(side="right")

        self.editor_textbox = ctk.CTkTextbox(editor_panel, font=THEME["font"]["code"], wrap="none", fg_color=THEME["color"]["card_bg"], text_color=THEME["color"]["text"], border_width=0, corner_radius=8)
        self.editor_textbox.grid(row=1, column=0, sticky="nsew")
        self.editor_textbox.configure(state="disabled")
        self.editor_textbox.bind("<KeyRelease>", self.on_editor_change)

    def load_macros_from_disk(self):
        for widget in self.automacros_frame.winfo_children(): widget.destroy()
        for widget in self.macros_frame.winfo_children(): widget.destroy()
        self.macro_widgets.clear()

        automacros_dir, macros_dir, _, _, _ = self.get_macro_paths()
        if not automacros_dir:
            ctk.CTkLabel(self.automacros_frame, text="Defina a pasta do OpenKore nas Configurações.", text_color=THEME["color"]["text_dark"], wraplength=250).pack(pady=20, padx=10)
            ctk.CTkLabel(self.macros_frame, text="Defina a pasta do OpenKore nas Configurações.", text_color=THEME["color"]["text_dark"], wraplength=250).pack(pady=20, padx=10)
            return

        for filename in sorted(os.listdir(automacros_dir)):
            if filename.endswith(".txt"):
                self.create_macro_widget(filename, automacros_dir, self.automacros_frame, "automacro")
        
        for filename in sorted(os.listdir(macros_dir)):
            if filename.endswith(".txt"):
                self.create_macro_widget(filename, macros_dir, self.macros_frame, "macro")

    def create_macro_widget(self, filename, dir_path, parent_frame, m_type):
        macro_name = os.path.splitext(filename)[0]
        full_path = os.path.join(dir_path, filename)

        card = ctk.CTkFrame(parent_frame, fg_color="transparent")
        card.pack(fill="x", padx=5, pady=4)
        card.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(card, text=macro_name, anchor="w", font=THEME["font"]["main"])
        label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        label.bind("<Button-1>", lambda e, p=full_path, n=macro_name: self.load_macro_to_editor(p, n))

        switch_var = ctk.StringVar(value="on")
        switch = ctk.CTkSwitch(card, text="", variable=switch_var, onvalue="on", offvalue="off", width=0, progress_color=THEME["color"]["accent_primary"])
        switch.grid(row=0, column=1, padx=10, pady=5)

        remove_button = ctk.CTkButton(card, text="✕", width=20, height=20, fg_color="transparent", text_color=THEME["color"]["error"], hover=False, command=lambda p=full_path, n=macro_name: self.delete_macro(p, n))
        remove_button.grid(row=0, column=2, padx=(0, 10), pady=5)
        
        self.macro_widgets[full_path] = {"switch": switch, "type": m_type}

    def load_macro_to_editor(self, path, name):
        try:
            content = load_data(path, is_json=False)
            self.editor_textbox.configure(state="normal")
            self.editor_textbox.delete("1.0", "end")
            self.editor_textbox.insert("1.0", content)
            self.current_macro_path = path
            self.editing_label.configure(text=f"Editando: {name}")
            self.save_button.configure(state="disabled")
            self.show_toast(f"Visualizando '{name}'.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível ler o arquivo do macro:\n{e}")
            self.show_toast(f"Falha ao carregar '{name}'.", error=True)

    def on_editor_change(self, event=None):
        if self.current_macro_path:
            self.save_button.configure(state="normal")

    def save_current_macro(self):
        if not self.current_macro_path: return
        try:
            content = self.editor_textbox.get("1.0", "end-1c")
            save_data(self.current_macro_path, content, is_json=False)
            self.save_button.configure(state="disabled")
            macro_name = os.path.splitext(os.path.basename(self.current_macro_path))[0]
            self.show_toast(f"Macro '{macro_name}' salvo com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o arquivo do macro:\n{e}")
            self.show_toast("Falha ao salvar o macro.", error=True)

    def add_new_macro_dialog(self):
        dialog = ctk.CTkInputDialog(text="Digite o nome do novo macro:", title="Criar Novo Macro")
        macro_name = dialog.get_input()
        if not macro_name: return

        macro_name = re.sub(r'[\\/*?:"<>|]', "", macro_name)
        if not macro_name:
            messagebox.showerror("Nome Inválido", "O nome do macro contém apenas caracteres inválidos.")
            return

        type_dialog = ThemedToplevel(self, "Tipo de Macro", "300x150")
        ctk.CTkLabel(type_dialog, text=f"Qual o tipo do macro '{macro_name}'?").pack(pady=10)
        result = {"type": None}
        def set_type(m_type):
            result["type"] = m_type
            type_dialog.destroy()
        ctk.CTkButton(type_dialog, text="Automacro", command=lambda: set_type("automacro")).pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(type_dialog, text="Macro", command=lambda: set_type("macro")).pack(pady=5, padx=20, fill="x")
        self.wait_window(type_dialog)
        macro_type = result["type"]
        if not macro_type: return

        automacros_dir, macros_dir, _, _, _ = self.get_macro_paths()
        if not automacros_dir:
            self.show_toast("Configure o caminho do OpenKore primeiro.", error=True)
            return

        folder = automacros_dir if macro_type == "automacro" else macros_dir
        new_path = os.path.join(folder, f"{macro_name}.txt")

        if os.path.exists(new_path):
            messagebox.showwarning("Existente", "Um macro com este nome já existe.")
            return

        header = f"{macro_type} {macro_name} {{\n\t# Adicione seu código aqui\n}}\n"
        save_data(new_path, header, is_json=False)
        
        self.load_macros_from_disk()
        self.load_macro_to_editor(new_path, macro_name)
        self.show_toast(f"Novo {macro_type} '{macro_name}' criado.")

    def delete_macro(self, path, name):
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o macro '{name}'?"):
            try:
                os.remove(path)
                if path == self.current_macro_path:
                    self.editor_textbox.configure(state="normal")
                    self.editor_textbox.delete("1.0", "end")
                    self.editor_textbox.configure(state="disabled")
                    self.editing_label.configure(text="Selecione um macro para editar...")
                    self.current_macro_path = None
                    self.save_button.configure(state="disabled")
                self.load_macros_from_disk()
                self.show_toast(f"Macro '{name}' excluído com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível excluir o macro:\n{e}")
                self.show_toast(f"Falha ao excluir '{name}'.", error=True)

    def compile_main_macro_file(self):
        _, _, backups_dir, main_macro_file, _ = self.get_macro_paths()
        if not main_macro_file:
            self.show_toast("Configure o caminho do OpenKore primeiro.", error=True)
            return

        if os.path.exists(main_macro_file):
            if not messagebox.askyesno("Confirmar Compilação", "Isso irá sobrescrever o seu `macros.txt` principal. Um backup será criado.\n\nDeseja continuar?"):
                return
            try:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                backup_file = os.path.join(backups_dir, f"macros.txt.{timestamp}.bak")
                with open(main_macro_file, 'r', encoding='utf-8') as src, open(backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
                self.show_toast("Backup do macros.txt criado.")
            except Exception as e:
                messagebox.showerror("Falha no Backup", f"Não foi possível criar o backup.\nOperação cancelada.\n\nErro: {e}")
                return

        try:
            final_content = ""
            active_count = 0
            sorted_widgets = sorted(self.macro_widgets.items(), key=lambda item: os.path.basename(item[0]))

            for path, data in sorted_widgets:
                if data["switch"].get() == "on":
                    content = load_data(path, is_json=False)
                    if content:
                        final_content += content + "\n\n"
                        active_count += 1
            
            save_data(main_macro_file, final_content.strip(), is_json=False)
            messagebox.showinfo("Compilação Concluída", f"`macros.txt` atualizado com sucesso!\n\n{active_count} macros ativos foram compilados.")
            self.show_toast(f"{active_count} macros compilados.")
        except Exception as e:
            messagebox.showerror("Erro na Compilação", f"Ocorreu um erro ao escrever o `macros.txt`:\n{e}")
            self.show_toast("Falha na compilação.", error=True)

    def open_original_macro_file(self):
        _, _, _, main_macro_file, _ = self.get_macro_paths()
        if not main_macro_file or not os.path.exists(main_macro_file):
            self.show_toast("Arquivo `macros.txt` não encontrado.", error=True)
            return
        self.open_file_with_default_app(main_macro_file)

    def import_from_main_file(self):
        automacros_dir, macros_dir, _, main_macro_file, _ = self.get_macro_paths()
        if not main_macro_file:
            self.show_toast("Configure o caminho do OpenKore primeiro.", error=True)
            return

        if not os.path.exists(main_macro_file):
            self.show_toast("Arquivo `macros.txt` não encontrado para importação.", error=True)
            return
        
        if not messagebox.askyesno("Confirmar Importação", "Isso irá ler seu `macros.txt` e criar arquivos individuais para cada macro encontrado. Macros existentes com o mesmo nome serão sobrescritos.\n\nDeseja continuar?"):
            return

        try:
            content = load_data(main_macro_file, is_json=False)
            pattern = re.compile(r'(automacro|macro)\s+([\w\d_-]+)\s*\{((?:[^{}]|\{(?3)\})*)\}', re.DOTALL)
            matches = pattern.finditer(content)
            imported_count = 0
            for match in matches:
                m_type, m_name, m_body = match.groups()
                full_macro_text = f"{m_type} {m_name} {{{m_body}}}"
                folder = automacros_dir if m_type == "automacro" else macros_dir
                file_path = os.path.join(folder, f"{m_name}.txt")
                save_data(file_path, full_macro_text.strip(), is_json=False)
                imported_count += 1
            
            if imported_count > 0:
                self.load_macros_from_disk()
                messagebox.showinfo("Importação Concluída", f"{imported_count} macros foram importados com sucesso!")
            else:
                messagebox.showwarning("Nenhum Macro Encontrado", "Não foi possível encontrar macros formatados corretamente para importar.")
        except Exception as e:
            messagebox.showerror("Erro na Importação", f"Ocorreu um erro ao importar:\n{e}")

    def check_for_legacy_macros_import(self):
        automacros_dir, macros_dir, _, main_macro_file, macros_dir_root = self.get_macro_paths()
        if not main_macro_file: return
        
        if not automacros_dir or not os.path.exists(automacros_dir): return
        if not macros_dir or not os.path.exists(macros_dir): return

        is_macros_dir_empty = not any(os.scandir(automacros_dir)) and not any(os.scandir(macros_dir))

        if os.path.exists(main_macro_file) and is_macros_dir_empty:
             if messagebox.askyesno("Importador de Macros", "Detectamos um `macros.txt` existente e suas pastas de gerenciamento estão vazias.\n\nDeseja importar e dividir os macros existentes em arquivos individuais?"):
                self.import_from_main_file()

    # =========================================================================
    # SEÇÃO: UTILITÁRIOS E JANELAS
    # =========================================================================
    def open_file_with_default_app(self, file_path):
        try:
            if sys.platform == "win32":
                os.startfile(file_path)
            elif sys.platform == "darwin":
                subprocess.call(["open", file_path])
            else:
                subprocess.call(["xdg-open", file_path])
        except Exception as e:
            self.show_toast(f"Não foi possível abrir o arquivo: {e}", error=True)

    def open_settings_window(self):
        if self.settings_win is None or not self.settings_win.winfo_exists():
            self.settings_win = SettingsWindow(self)
        self.settings_win.focus()

    def open_add_bot_window(self):
        if self.add_bot_win is None or not self.add_bot_win.winfo_exists():
            self.add_bot_win = AddBotWindow(self)
        self.add_bot_win.focus()

    def show_toast(self, message, error=False):
        if self.toast_after_id:
            self.after_cancel(self.toast_after_id)
        if self.toast_label:
            self.toast_label.destroy()

        fg_color = THEME["color"]["error"] if error else THEME["color"]["button"]
        
        self.toast_label = ctk.CTkLabel(self, text=message, corner_radius=8, font=THEME["font"]["toast"], text_color=THEME["color"]["text"], fg_color=fg_color)
        self.toast_label.place(relx=0.5, y=10, anchor="n")
        self.toast_label.lift()
        self.toast_after_id = self.toast_label.after(3000, self.hide_toast)

    def hide_toast(self):
        if self.toast_label:
            self.toast_label.destroy()
            self.toast_label = None
        self.toast_after_id = None

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    app = KoreNexusApp()
    app.mainloop()
