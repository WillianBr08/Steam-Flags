#!/usr/bin/env python3
"""
Steam Flags - Configure Steam launch options for Linux gaming
GTK4 + libadwaita version
"""
import sys
import os
import locale

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, Gdk

APP_ID = "com.github.steam_flags"
APP_VERSION = "0.3.0"

STRINGS = {
    "pt_BR": {
        "app_title": "Steam Flags",
        "welcome_title": "Steam Flags",
        "welcome_desc": "Gere comandos de inicialização do Gamescope para o Steam",
        "welcome_start": "Começar",
        "lang_label": "Idioma:",
        "lang_system": "Sistema",
        "lang_pt": "Português",
        "lang_en": "English",
        "enable_gamescope": "Habilitar Gamescope",
        "game_res": "Resolução do Jogo",
        "out_res": "Resolução de Saída",
        "refresh_rate": "Taxa de Atualização",
        "scaling": "Escalonamento",
        "scaling_mode": "Modo (-S):",
        "scaling_default": "Padrão",
        "scaling_stretch": "Esticar",
        "scaling_integer": "Inteiro",
        "upscaling": "Upscaling (-F):",
        "upscaling_none": "Nenhum",
        "upscaling_fsr": "FSR",
        "upscaling_nis": "NIS",
        "fsr_sharpness": "Nitidez FSR:",
        "display_mode": "Modo de Exibição",
        "display_window": "Janela (Padrão)",
        "display_fullscreen": "Tela Cheia (-f)",
        "display_borderless": "Sem Bordas (-b)",
        "other_settings": "Outras Configurações",
        "grab_cursor": "Capturar cursor (--force-grab-cursor / -g)",
        "env_vars": "Variáveis de Ambiente",
        "clear_preload": "Limpar LD_PRELOAD",
        "amd_antilag": "AMD Anti-Lag",
        "vkbasalt": "vkBasalt",
        "feral_gamemode": "Feral Gamemode (gamemoderun)",
        "proton_settings": "Configurações do Proton",
        "dll_overrides": "WINEDLLOVERRIDES (separado por vírgula):",
        "dll_placeholder": "dxgi,dinput8",
        "generated_cmd": "Comando Gerado:",
        "cmd_placeholder": "O comando aparecerá aqui conforme você altera as opções...",
        "copy_clipboard": "Copiar para Área de Transferência",
        "width": "Largura (-w):",
        "height": "Altura (-h):",
        "width_out": "Largura (-W):",
        "height_out": "Altura (-H):",
        "frequency": "Frequência (-r):",
        "cachyos_game_performance": "Game Performance (CachyOS)",
        "cachyos_antilag_warning": "Aviso: ananicy-cpp deve estar desativado",
        "settings": "Configurações",
        "settings_language": "Idioma",
        "settings_theme": "Tema",
        "theme_light": "Claro",
        "theme_dark": "Escuro",
        "theme_system": "Sistema",
        "theme_palestra": "Palmeiras",
        "copy_feedback": "✓ Copiado!",
    },
    "en": {
        "app_title": "Steam Flags",
        "welcome_title": "Steam Flags",
        "welcome_desc": "Generate Gamescope launch commands for Steam",
        "welcome_start": "Get Started",
        "lang_label": "Language:",
        "lang_system": "System",
        "lang_pt": "Português",
        "lang_en": "English",
        "enable_gamescope": "Enable Gamescope",
        "game_res": "Game Resolution",
        "out_res": "Output Resolution",
        "refresh_rate": "Refresh Rate",
        "scaling": "Scaling",
        "scaling_mode": "Mode (-S):",
        "scaling_default": "Default",
        "scaling_stretch": "Stretch",
        "scaling_integer": "Integer",
        "upscaling": "Upscaling (-F):",
        "upscaling_none": "None",
        "upscaling_fsr": "FSR",
        "upscaling_nis": "NIS",
        "fsr_sharpness": "FSR Sharpness:",
        "display_mode": "Display Mode",
        "display_window": "Window (Default)",
        "display_fullscreen": "Fullscreen (-f)",
        "display_borderless": "Borderless (-b)",
        "other_settings": "Other Settings",
        "grab_cursor": "Capture mouse cursor (--force-grab-cursor / -g)",
        "env_vars": "Environment Variables",
        "clear_preload": "Clear LD_PRELOAD",
        "amd_antilag": "AMD Anti-Lag",
        "vkbasalt": "vkBasalt",
        "feral_gamemode": "Feral Gamemode (gamemoderun)",
        "proton_settings": "Proton Settings",
        "dll_overrides": "WINEDLLOVERRIDES (comma-separated):",
        "dll_placeholder": "dxgi,dinput8",
        "generated_cmd": "Generated Command:",
        "cmd_placeholder": "Command will appear here as you change options...",
        "copy_clipboard": "Copy to Clipboard",
        "width": "Width (-w):",
        "height": "Height (-h):",
        "width_out": "Width (-W):",
        "height_out": "Height (-H):",
        "frequency": "Frequency (-r):",
        "cachyos_game_performance": "Game Performance (CachyOS)",
        "cachyos_antilag_warning": "Warning: ananicy-cpp must be disabled",
        "settings": "Settings",
        "settings_language": "Language",
        "settings_theme": "Theme",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "theme_system": "System",
        "theme_palestra": "Palmeiras",
        "copy_feedback": "✓ Copied!",
    },
}


def get_system_lang():
    lang = locale.getlocale()[0]
    if lang and lang.startswith("pt"):
        return "pt_BR"
    return "en"


def is_cachyos():
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("ID=") or line.startswith("ID_LIKE="):
                    if "cachyos" in line.lower():
                        return True
    except Exception:
        pass
    return False


class SteamFlags(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.settings = Gio.Settings(schema_id=APP_ID)
        self.current_lang = self._load_lang_preference()
        self.is_cachyos = is_cachyos()
        self.win = None
        self._css_provider = None
        self._apply_theme(self.settings.get_string("theme"))

    def _load_lang_preference(self):
        lang = self.settings.get_string("language")
        if lang in ("pt_BR", "en"):
            return lang
        return get_system_lang()

    def do_activate(self):
        if self.win is None:
            self.win = SteamFlagsWindow(application=self)
        self.win.present()

    def get_strings(self):
        return STRINGS[self.current_lang]

    def _apply_theme(self, theme):
        style_manager = Adw.StyleManager.get_default()
        if self._css_provider:
            Gtk.StyleContext.remove_provider_for_display(
                Gdk.Display.get_default(), self._css_provider
            )
            self._css_provider = None

        if theme == "light":
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        elif theme == "dark":
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        elif theme == "system":
            style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)
        else:
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)

        css_parts = []

        if theme == "palestra":
            css_parts.append(self._get_theme_palestra())
        elif theme == "light":
            css_parts.append(self._get_theme_light())
        elif theme == "dark":
            css_parts.append(self._get_theme_dark())

        if css_parts:
            self._css_provider = Gtk.CssProvider()
            self._css_provider.load_from_string("\n".join(css_parts))
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(),
                self._css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_USER,
            )

    def _get_theme_palestra(self):
        return """
            @define-color accent_color #006437;
            @define-color accent_bg_color #006437;
            @define-color accent_fg_color #FFFFFF;
            @define-color destructive_color #FF0000;
            @define-color destructive_bg_color #FF0000;
            @define-color destructive_fg_color #FFFFFF;
            @define-color success_color #006437;
            @define-color success_bg_color #006437;
            @define-color success_fg_color #FFFFFF;
            @define-color warning_color #FFD700;
            @define-color warning_bg_color #FFD700;
            @define-color warning_fg_color #000000;
            @define-color error_color #FF0000;
            @define-color error_bg_color #FF0000;
            @define-color error_fg_color #FFFFFF;
            headerbar {
                background: linear-gradient(180deg, #006437 0%, #004d2a 100%);
                color: #FFFFFF;
                border-bottom: 2px solid #FF0000;
            }
            headerbar title, headerbar subtitle {
                color: #FFFFFF;
            }
            headerbar button:not(.titlebutton):not(image) {
                color: #FFFFFF;
            }
            headerbar button:not(.titlebutton):not(image):hover {
                background: rgba(255,255,255,0.2);
            }
            .suggested-action {
                background: #006437;
                color: #FFFFFF;
                border: 1px solid #004d2a;
            }
            .suggested-action:hover {
                background: #00804a;
            }
            .accent {
                color: #006437;
            }
            .warning {
                color: #FF0000;
                font-weight: bold;
            }
            frame {
                border-color: #006437;
            }
            checkbutton check {
                background: #006437;
            }
            scale trough highlight {
                background: #006437;
            }
        """

    def _get_theme_light(self):
        return """
            @define-color accent_color #2e7d32;
            @define-color accent_bg_color #2e7d32;
            @define-color accent_fg_color #FFFFFF;
            @define-color destructive_color #c62828;
            @define-color destructive_bg_color #c62828;
            @define-color destructive_fg_color #FFFFFF;
            @define-color success_color #2e7d32;
            @define-color success_bg_color #2e7d32;
            @define-color success_fg_color #FFFFFF;
            @define-color warning_color #f57f17;
            @define-color warning_bg_color #f57f17;
            @define-color warning_fg_color #FFFFFF;
            @define-color error_color #c62828;
            @define-color error_bg_color #c62828;
            @define-color error_fg_color #FFFFFF;
            .suggested-action {
                background: #2e7d32;
                color: #FFFFFF;
            }
            .suggested-action:hover {
                background: #388e3c;
            }
            .accent {
                color: #2e7d32;
            }
            .warning {
                color: #e65100;
                font-weight: bold;
            }
            .success {
                color: #2e7d32;
            }
            .error {
                color: #c62828;
            }
            checkbutton check:checked {
                background: #2e7d32;
                border-color: #2e7d32;
            }
            scale trough highlight {
                background: #2e7d32;
            }
            headerbar {
                border-bottom: 1px solid #e0e0e0;
            }
        """

    def _get_theme_dark(self):
        return """
            @define-color accent_color #66bb6a;
            @define-color accent_bg_color #66bb6a;
            @define-color accent_fg_color #000000;
            @define-color destructive_color #ef5350;
            @define-color destructive_bg_color #ef5350;
            @define-color destructive_fg_color #000000;
            @define-color success_color #66bb6a;
            @define-color success_bg_color #66bb6a;
            @define-color success_fg_color #000000;
            @define-color warning_color #ffb74d;
            @define-color warning_bg_color #ffb74d;
            @define-color warning_fg_color #000000;
            @define-color error_color #ef5350;
            @define-color error_bg_color #ef5350;
            @define-color error_fg_color #000000;
            .suggested-action {
                background: #66bb6a;
                color: #000000;
            }
            .suggested-action:hover {
                background: #81c784;
            }
            .accent {
                color: #66bb6a;
            }
            .warning {
                color: #ffb74d;
                font-weight: bold;
            }
            .success {
                color: #66bb6a;
            }
            .error {
                color: #ef5350;
            }
            checkbutton check:checked {
                background: #66bb6a;
                border-color: #66bb6a;
            }
            scale trough highlight {
                background: #66bb6a;
            }
            headerbar {
                border-bottom: 1px solid #404040;
            }
        """


class SteamFlagsWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = self.get_application()
        self.strings = self.app.get_strings()
        self.set_title(self.strings["app_title"])
        self.set_default_size(600, 700)

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SteamFlags.png")
        if os.path.exists(icon_path):
            self.set_icon_name(icon_path)

        self._build_ui()
        self._connect_signals()
        self._update_command()

        if self.app.settings.get_boolean("welcome-shown"):
            self.stack.set_visible_child_name("main")
        else:
            self.stack.set_visible_child_name("welcome")

    def _build_ui(self):
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(200)
        self.set_content(self.stack)

        self._build_welcome_page()
        self._build_main_page()
        self._build_settings_page()

    def _build_welcome_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_valign(Gtk.Align.CENTER)
        box.set_halign(Gtk.Align.CENTER)
        box.set_margin_top(40)
        box.set_margin_bottom(40)
        box.set_margin_start(20)
        box.set_margin_end(20)

        label_emoji = Gtk.Label(label="\U0001F3AE")
        label_emoji.add_css_class("title-1")
        box.append(label_emoji)

        title = Gtk.Label(label=self.strings["welcome_title"])
        title.add_css_class("title-1")
        title.add_css_class("accent")
        box.append(title)

        desc = Gtk.Label(label=self.strings["welcome_desc"])
        desc.set_wrap(True)
        desc.set_max_width_chars(40)
        desc.add_css_class("body")
        box.append(desc)

        start_btn = Gtk.Button(label=self.strings["welcome_start"])
        start_btn.add_css_class("suggested-action")
        start_btn.set_size_request(180, 45)
        start_btn.connect("clicked", self._on_get_started)
        box.append(start_btn)

        self.stack.add_named(box, "welcome")

    def _build_main_page(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        toolbar = self._build_toolbar()
        main_box.append(toolbar)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        main_box.append(scrolled)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content.set_margin_top(12)
        content.set_margin_bottom(12)
        content.set_margin_start(16)
        content.set_margin_end(16)
        scrolled.set_child(content)

        self.enable_gamescope = Gtk.CheckButton(label=self.strings["enable_gamescope"])
        self.enable_gamescope.set_active(True)
        content.append(self.enable_gamescope)

        self._build_game_resolution(content)
        self._build_output_resolution(content)
        self._build_refresh_rate(content)
        self._build_scaling(content)
        self._build_display_mode(content)
        self._build_other_settings(content)
        self._build_env_vars(content)
        self._build_proton_settings(content)
        self._build_output_area(content)

        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        content.append(spacer)

        self.stack.add_named(main_box, "main")

    def _build_toolbar(self):
        header = Adw.HeaderBar()

        self.settings_btn = Gtk.Button()
        self.settings_btn.set_icon_name("emblem-system-symbolic")
        self.settings_btn.set_tooltip_text(self.strings["settings"])
        self.settings_btn.connect("clicked", self._on_settings_clicked)
        header.pack_end(self.settings_btn)

        return header

    def _on_settings_clicked(self, *_args):
        self.stack.set_visible_child_name("settings")

    def _build_game_resolution(self, parent):
        frame = Gtk.Frame(label=self.strings["game_res"])
        grid = Gtk.Grid(column_spacing=12, row_spacing=8)
        grid.set_margin_top(8)
        grid.set_margin_bottom(8)
        grid.set_margin_start(12)
        grid.set_margin_end(12)
        frame.set_child(grid)

        self.lbl_width = Gtk.Label(label=self.strings["width"], halign=Gtk.Align.START)
        grid.attach(self.lbl_width, 0, 0, 1, 1)
        self.spin_w = Gtk.SpinButton.new_with_range(0, 99999, 1)
        self.spin_w.set_tooltip_text("Internal game width (-w)")
        grid.attach(self.spin_w, 1, 0, 1, 1)

        self.lbl_height = Gtk.Label(label=self.strings["height"], halign=Gtk.Align.START)
        grid.attach(self.lbl_height, 0, 1, 1, 1)
        self.spin_h = Gtk.SpinButton.new_with_range(0, 99999, 1)
        self.spin_h.set_tooltip_text("Internal game height (-h)")
        grid.attach(self.spin_h, 1, 1, 1, 1)

        self.game_res_frame = frame
        parent.append(frame)

    def _build_output_resolution(self, parent):
        frame = Gtk.Frame(label=self.strings["out_res"])
        grid = Gtk.Grid(column_spacing=12, row_spacing=8)
        grid.set_margin_top(8)
        grid.set_margin_bottom(8)
        grid.set_margin_start(12)
        grid.set_margin_end(12)
        frame.set_child(grid)

        self.lbl_width_out = Gtk.Label(label=self.strings["width_out"], halign=Gtk.Align.START)
        grid.attach(self.lbl_width_out, 0, 0, 1, 1)
        self.spin_W = Gtk.SpinButton.new_with_range(0, 99999, 1)
        self.spin_W.set_tooltip_text("Gamescope output width (-W)")
        grid.attach(self.spin_W, 1, 0, 1, 1)

        self.lbl_height_out = Gtk.Label(label=self.strings["height_out"], halign=Gtk.Align.START)
        grid.attach(self.lbl_height_out, 0, 1, 1, 1)
        self.spin_H = Gtk.SpinButton.new_with_range(0, 99999, 1)
        self.spin_H.set_tooltip_text("Gamescope output height (-H)")
        grid.attach(self.spin_H, 1, 1, 1, 1)

        self.out_res_frame = frame
        parent.append(frame)

    def _build_refresh_rate(self, parent):
        frame = Gtk.Frame(label=self.strings["refresh_rate"])
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        hbox.set_margin_top(8)
        hbox.set_margin_bottom(8)
        hbox.set_margin_start(12)
        hbox.set_margin_end(12)
        frame.set_child(hbox)

        self.lbl_frequency = Gtk.Label(label=self.strings["frequency"])
        hbox.append(self.lbl_frequency)
        self.spin_r = Gtk.SpinButton.new_with_range(0, 999, 1)
        self.spin_r.set_tooltip_text("Display refresh rate (-r)")
        hbox.append(self.spin_r)

        self.hz_frame = frame
        parent.append(frame)

    def _build_scaling(self, parent):
        frame = Gtk.Frame(label=self.strings["scaling"])
        grid = Gtk.Grid(column_spacing=12, row_spacing=8)
        grid.set_margin_top(8)
        grid.set_margin_bottom(8)
        grid.set_margin_start(12)
        grid.set_margin_end(12)
        frame.set_child(grid)

        self.lbl_scaling_mode = Gtk.Label(label=self.strings["scaling_mode"], halign=Gtk.Align.START)
        grid.attach(self.lbl_scaling_mode, 0, 0, 1, 1)
        self.combo_scaling = Gtk.DropDown.new_from_strings([
            self.strings["scaling_default"],
            self.strings["scaling_stretch"],
            self.strings["scaling_integer"],
        ])
        self.combo_scaling.set_tooltip_text("Scaling mode (-S)")
        grid.attach(self.combo_scaling, 1, 0, 1, 1)

        self.combo_upscaling = Gtk.DropDown.new_from_strings([
            self.strings["upscaling_none"],
            self.strings["upscaling_fsr"],
            self.strings["upscaling_nis"],
        ])
        self.combo_upscaling.set_tooltip_text("Upscaling (-F)")
        self.lbl_upscaling = Gtk.Label(label=self.strings["upscaling"], halign=Gtk.Align.START)
        grid.attach(self.lbl_upscaling, 0, 1, 1, 1)
        grid.attach(self.combo_upscaling, 1, 1, 1, 1)

        self.sharpness_label = Gtk.Label(label=self.strings["fsr_sharpness"], halign=Gtk.Align.START)
        grid.attach(self.sharpness_label, 0, 2, 1, 1)
        self.spin_sharpness = Gtk.SpinButton.new_with_range(0, 20, 1)
        self.spin_sharpness.set_value(5)
        self.spin_sharpness.set_tooltip_text("FSR sharpness level")
        grid.attach(self.spin_sharpness, 1, 2, 1, 1)
        self.sharpness_label.set_visible(False)
        self.spin_sharpness.set_visible(False)

        self.scaling_frame = frame
        parent.append(frame)

    def _build_display_mode(self, parent):
        frame = Gtk.Frame(label=self.strings["display_mode"])
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        hbox.set_margin_top(8)
        hbox.set_margin_bottom(8)
        hbox.set_margin_start(12)
        hbox.set_margin_end(12)
        frame.set_child(hbox)

        self.radio_window = Gtk.ToggleButton(label=self.strings["display_window"])
        self.radio_window.set_active(True)
        self.radio_fullscreen = Gtk.ToggleButton(label=self.strings["display_fullscreen"])
        self.radio_borderless = Gtk.ToggleButton(label=self.strings["display_borderless"])

        self.radio_group = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.radio_group.add_css_class("linked")
        self.radio_group.append(self.radio_window)
        self.radio_group.append(self.radio_fullscreen)
        self.radio_group.append(self.radio_borderless)
        hbox.append(self.radio_group)

        self.display_frame = frame
        parent.append(frame)

    def _build_other_settings(self, parent):
        frame = Gtk.Frame(label=self.strings["other_settings"])
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        vbox.set_margin_top(8)
        vbox.set_margin_bottom(8)
        vbox.set_margin_start(12)
        vbox.set_margin_end(12)
        frame.set_child(vbox)

        self.check_grab = Gtk.CheckButton(label=self.strings["grab_cursor"])
        self.check_grab.set_tooltip_text("Force grab cursor")
        vbox.append(self.check_grab)

        self.other_frame = frame
        parent.append(frame)

    def _build_env_vars(self, parent):
        frame = Gtk.Frame(label=self.strings["env_vars"])
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        vbox.set_margin_top(8)
        vbox.set_margin_bottom(8)
        vbox.set_margin_start(12)
        vbox.set_margin_end(12)
        frame.set_child(vbox)

        self.check_clear_preload = Gtk.CheckButton(label=self.strings["clear_preload"])
        self.check_clear_preload.set_tooltip_text('Adds LD_PRELOAD=""')
        vbox.append(self.check_clear_preload)

        self.check_amd_antlag = Gtk.CheckButton(label=self.strings["amd_antilag"])
        self.check_amd_antlag.set_tooltip_text("Enable AMD Anti-Lag (adds ENABLE_AMD_ANTI_LAG=1)")
        vbox.append(self.check_amd_antlag)

        self.check_vkbasalt = Gtk.CheckButton(label=self.strings["vkbasalt"])
        self.check_vkbasalt.set_tooltip_text("Adds ENABLE_VKBASALT=1")
        vbox.append(self.check_vkbasalt)

        self.check_feral = Gtk.CheckButton(label=self.strings["feral_gamemode"])
        self.check_feral.set_tooltip_text("Run with gamemoderun wrapper")
        feral_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        feral_box.append(self.check_feral)
        self.lbl_antilag_warning = Gtk.Label(label=self.strings["cachyos_antilag_warning"])
        self.lbl_antilag_warning.add_css_class("warning")
        self.lbl_antilag_warning.set_visible(self.app.is_cachyos)
        feral_box.append(self.lbl_antilag_warning)
        vbox.append(feral_box)

        self.check_game_performance = Gtk.CheckButton(label=self.strings["cachyos_game_performance"])
        self.check_game_performance.set_tooltip_text("Run with game-performance wrapper (CachyOS)")
        self.check_game_performance.set_visible(self.app.is_cachyos)
        vbox.append(self.check_game_performance)

        parent.append(frame)

    def _build_proton_settings(self, parent):
        frame = Gtk.Frame(label=self.strings["proton_settings"])
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        vbox.set_margin_top(8)
        vbox.set_margin_bottom(8)
        vbox.set_margin_start(12)
        vbox.set_margin_end(12)
        frame.set_child(vbox)

        dll_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.lbl_dll_overrides = Gtk.Label(label=self.strings["dll_overrides"])
        dll_box.append(self.lbl_dll_overrides)
        self.dll_overrides_input = Gtk.Entry()
        self.dll_overrides_input.set_placeholder_text(self.strings["dll_placeholder"])
        self.dll_overrides_input.set_hexpand(True)
        self.dll_overrides_input.set_tooltip_text("DLLs to override (format: dll1,dll2)")
        dll_box.append(self.dll_overrides_input)
        vbox.append(dll_box)

        self.proton_frame = frame
        parent.append(frame)

    def _build_output_area(self, parent):
        output_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        output_box.append(Gtk.Label(label=self.strings["generated_cmd"], halign=Gtk.Align.START))

        self.cmd_output = Gtk.Entry()
        self.cmd_output.set_editable(False)
        self.cmd_output.set_sensitive(True)
        self.cmd_output.set_placeholder_text(self.strings["cmd_placeholder"])
        self.cmd_output.set_hexpand(True)
        output_box.append(self.cmd_output)

        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        btn_box.set_halign(Gtk.Align.END)
        self.copy_btn = Gtk.Button(label=self.strings["copy_clipboard"])
        self.copy_btn.set_sensitive(True)
        self.copy_btn.set_tooltip_text(self.strings["copy_clipboard"])
        self.copy_btn.add_css_class("suggested-action")
        self.copy_btn.connect("clicked", self._copy_to_clipboard)
        btn_box.append(self.copy_btn)
        output_box.append(btn_box)

        parent.append(output_box)

    def _build_settings_page(self):
        settings_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        header = Adw.HeaderBar()
        back_btn = Gtk.Button()
        back_btn.set_icon_name("go-previous-symbolic")
        back_btn.connect("clicked", self._on_settings_back)
        header.pack_start(back_btn)

        self.settings_title = Gtk.Label(label=self.strings["settings"])
        header.set_title_widget(self.settings_title)

        settings_box.append(header)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        settings_box.append(scrolled)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content.set_margin_top(12)
        content.set_margin_bottom(12)
        content.set_margin_start(16)
        content.set_margin_end(16)
        scrolled.set_child(content)

        lang_frame = Gtk.Frame(label=self.strings["settings_language"])
        lang_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        lang_box.set_margin_top(8)
        lang_box.set_margin_bottom(8)
        lang_box.set_margin_start(12)
        lang_box.set_margin_end(12)
        lang_frame.set_child(lang_box)

        self.settings_lang_dropdown = Gtk.DropDown.new_from_strings([
            self.strings["lang_system"],
            self.strings["lang_pt"],
            self.strings["lang_en"],
        ])
        lang_pref = self.app.settings.get_string("language")
        if lang_pref == "pt_BR":
            self.settings_lang_dropdown.set_selected(1)
        elif lang_pref == "en":
            self.settings_lang_dropdown.set_selected(2)
        else:
            self.settings_lang_dropdown.set_selected(0)
        self.settings_lang_dropdown.connect("notify::selected", self._on_lang_changed)
        lang_box.append(self.settings_lang_dropdown)
        content.append(lang_frame)

        theme_frame = Gtk.Frame(label=self.strings["settings_theme"])
        theme_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        theme_box.set_margin_top(8)
        theme_box.set_margin_bottom(8)
        theme_box.set_margin_start(12)
        theme_box.set_margin_end(12)
        theme_frame.set_child(theme_box)

        self.settings_theme_dropdown = Gtk.DropDown.new_from_strings([
            self.strings["theme_system"],
            self.strings["theme_light"],
            self.strings["theme_dark"],
            self.strings["theme_palestra"],
        ])
        theme_pref = self.app.settings.get_string("theme")
        theme_map = {"system": 0, "light": 1, "dark": 2, "palestra": 3}
        self.settings_theme_dropdown.set_selected(theme_map.get(theme_pref, 0))
        self.settings_theme_dropdown.connect("notify::selected", self._on_theme_changed)
        theme_box.append(self.settings_theme_dropdown)
        content.append(theme_frame)

        version_label = Gtk.Label(label=f"v{APP_VERSION}")
        version_label.set_margin_top(24)
        version_label.set_css_class("dim-label")
        content.append(version_label)

        self.stack.add_named(settings_box, "settings")

    def _on_settings_back(self, *_args):
        self.stack.set_visible_child_name("main")

    def _connect_signals(self):
        self.enable_gamescope.connect("toggled", self._on_update)
        self.spin_w.connect("value-changed", self._on_update)
        self.spin_h.connect("value-changed", self._on_update)
        self.spin_W.connect("value-changed", self._on_update)
        self.spin_H.connect("value-changed", self._on_update)
        self.spin_r.connect("value-changed", self._on_update)
        self.combo_scaling.connect("notify::selected", self._on_update)
        self.combo_upscaling.connect("notify::selected", self._on_update)
        self.radio_window.connect("toggled", self._on_update)
        self.radio_fullscreen.connect("toggled", self._on_update)
        self.radio_borderless.connect("toggled", self._on_update)
        self.check_grab.connect("toggled", self._on_update)
        self.check_feral.connect("toggled", self._on_update)
        self.check_game_performance.connect("toggled", self._on_update)
        self.spin_sharpness.connect("value-changed", self._on_update)
        self.check_clear_preload.connect("toggled", self._on_update)
        self.check_amd_antlag.connect("toggled", self._on_update)
        self.check_vkbasalt.connect("toggled", self._on_update)
        self.dll_overrides_input.connect("changed", self._on_update)
        self.enable_gamescope.connect("toggled", self._on_gamescope_toggled)
        self.combo_upscaling.connect("notify::selected", self._on_upscaling_changed)
        self._on_upscaling_changed()
        self._on_gamescope_toggled()

    def _on_upscaling_changed(self, *_args):
        idx = self.combo_upscaling.get_selected()
        is_fsr = idx == 1
        self.sharpness_label.set_visible(is_fsr)
        self.spin_sharpness.set_visible(is_fsr)

    def _on_gamescope_toggled(self, *_args):
        enabled = self.enable_gamescope.get_active()
        self.game_res_frame.set_visible(enabled)
        self.out_res_frame.set_visible(enabled)
        self.hz_frame.set_visible(enabled)
        self.scaling_frame.set_visible(enabled)
        self.display_frame.set_visible(enabled)
        self.check_grab.set_visible(enabled)
        if not enabled:
            self.check_grab.set_active(False)

    def _on_update(self, *_args):
        self._update_command()

    def _on_get_started(self, *_args):
        self.stack.set_visible_child_name("main")
        self.app.settings.set_boolean("welcome-shown", True)

    def _on_lang_changed(self, dropdown, *_args):
        selected = dropdown.get_selected()
        if selected == 0:
            lang_key = ""
        elif selected == 1:
            lang_key = "pt_BR"
        else:
            lang_key = "en"
        self.app.settings.set_string("language", lang_key)
        self.app.current_lang = self.app._load_lang_preference()
        self.strings = self.app.get_strings()
        self._refresh_ui_texts()

    def _on_theme_changed(self, dropdown, *_args):
        selected = dropdown.get_selected()
        theme_map = {0: "system", 1: "light", 2: "dark", 3: "palestra"}
        theme = theme_map.get(selected, "system")
        self.app.settings.set_string("theme", theme)
        self.app._apply_theme(theme)

    def _refresh_ui_texts(self):
        s = self.strings
        self.set_title(s["app_title"])
        self.enable_gamescope.set_label(s["enable_gamescope"])

        self.game_res_frame.set_label(s["game_res"])
        self.lbl_width.set_label(s["width"])
        self.lbl_height.set_label(s["height"])

        self.out_res_frame.set_label(s["out_res"])
        self.lbl_width_out.set_label(s["width_out"])
        self.lbl_height_out.set_label(s["height_out"])

        self.hz_frame.set_label(s["refresh_rate"])
        self.lbl_frequency.set_label(s["frequency"])

        self.scaling_frame.set_label(s["scaling"])
        self.lbl_scaling_mode.set_label(s["scaling_mode"])
        self.lbl_upscaling.set_label(s["upscaling"])
        self.sharpness_label.set_label(s["fsr_sharpness"])

        self.display_frame.set_label(s["display_mode"])
        self.radio_window.set_label(s["display_window"])
        self.radio_fullscreen.set_label(s["display_fullscreen"])
        self.radio_borderless.set_label(s["display_borderless"])

        self.other_frame.set_label(s["other_settings"])
        self.check_grab.set_label(s["grab_cursor"])

        self.check_clear_preload.set_label(s["clear_preload"])
        self.check_amd_antlag.set_label(s["amd_antilag"])
        self.check_vkbasalt.set_label(s["vkbasalt"])
        self.check_feral.set_label(s["feral_gamemode"])
        self.lbl_antilag_warning.set_label(s["cachyos_antilag_warning"])
        self.check_game_performance.set_label(s["cachyos_game_performance"])

        self.proton_frame.set_label(s["proton_settings"])
        self.lbl_dll_overrides.set_label(s["dll_overrides"])
        self.dll_overrides_input.set_placeholder_text(s["dll_placeholder"])

        self.cmd_output.set_placeholder_text(s["cmd_placeholder"])
        self.copy_btn.set_label(s["copy_clipboard"])
        self.copy_btn.set_tooltip_text(s["copy_clipboard"])

        self.settings_btn.set_tooltip_text(s["settings"])
        self.settings_title.set_label(s["settings"])

        old_theme = self.settings_theme_dropdown.get_selected()
        self.settings_theme_dropdown.set_model(Gtk.StringList.new([
            s["theme_system"], s["theme_light"], s["theme_dark"], s["theme_palestra"],
        ]))
        if old_theme < 4:
            self.settings_theme_dropdown.set_selected(old_theme)

        old_scaling = self.combo_scaling.get_selected()
        self.combo_scaling.set_model(Gtk.StringList.new([
            s["scaling_default"], s["scaling_stretch"], s["scaling_integer"],
        ]))
        if old_scaling < 3:
            self.combo_scaling.set_selected(old_scaling)

        old_upscaling = self.combo_upscaling.get_selected()
        self.combo_upscaling.set_model(Gtk.StringList.new([
            s["upscaling_none"], s["upscaling_fsr"], s["upscaling_nis"],
        ]))
        if old_upscaling < 3:
            self.combo_upscaling.set_selected(old_upscaling)

    def _update_command(self):
        env_vars = []

        if self.check_clear_preload.get_active():
            env_vars.append('LD_PRELOAD=""')
        if self.check_amd_antlag.get_active():
            env_vars.append('ENABLE_AMD_ANTI_LAG=1')
        if self.check_vkbasalt.get_active():
            env_vars.append('ENABLE_VKBASALT=1')
        if self.check_feral.get_active():
            env_vars.append("gamemoderun")
        if self.check_game_performance.get_active():
            env_vars.append("game-performance")

        dll_overrides = self.dll_overrides_input.get_text().strip()
        if dll_overrides:
            overrides = ";".join([f"{dll.strip()}=n,b" for dll in dll_overrides.split(",")])
            env_vars.append(f'WINEDLLOVERRIDES="{overrides}"')

        parts = []
        if env_vars:
            parts.extend(env_vars)

        if self.enable_gamescope.get_active():
            gamescope_parts = ["gamescope"]
            if self.spin_w.get_value() > 0:
                gamescope_parts.extend(["-w", str(int(self.spin_w.get_value()))])
            if self.spin_h.get_value() > 0:
                gamescope_parts.extend(["-h", str(int(self.spin_h.get_value()))])
            if self.spin_W.get_value() > 0:
                gamescope_parts.extend(["-W", str(int(self.spin_W.get_value()))])
            if self.spin_H.get_value() > 0:
                gamescope_parts.extend(["-H", str(int(self.spin_H.get_value()))])
            if self.spin_r.get_value() > 0:
                gamescope_parts.extend(["-r", str(int(self.spin_r.get_value()))])

            scaling_map = {0: None, 1: "stretch", 2: "integer"}
            scaling_val = scaling_map.get(self.combo_scaling.get_selected())
            if scaling_val:
                gamescope_parts.extend(["-S", scaling_val])

            upscale_map = {0: None, 1: "fsr", 2: "nis"}
            upscale_val = upscale_map.get(self.combo_upscaling.get_selected())
            if upscale_val:
                gamescope_parts.extend(["-F", upscale_val])
                if upscale_val == "fsr" and self.spin_sharpness.get_value() > 0:
                    gamescope_parts.extend(["--sharpness", str(int(self.spin_sharpness.get_value()))])

            if self.radio_fullscreen.get_active():
                gamescope_parts.append("-f")
            elif self.radio_borderless.get_active():
                gamescope_parts.append("-b")

            if self.check_grab.get_active():
                gamescope_parts.append("--force-grab-cursor")

            gamescope_parts.append("--")
            parts.extend(gamescope_parts)

        parts.append("%command%")
        cmd = " ".join(parts)
        self.cmd_output.set_text(cmd)

    def _copy_to_clipboard(self, *_args):
        clipboard = Gdk.Display.get_default().get_clipboard()
        text = self.cmd_output.get_text()
        clipboard.set(text)
        self.copy_btn.set_label(self.strings["copy_feedback"])
        from gi.repository import GLib
        GLib.timeout_add(1500, self._reset_copy_button)

    def _reset_copy_button(self):
        self.copy_btn.set_label(self.strings["copy_clipboard"])
        return False


def main():
    app = SteamFlags()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
