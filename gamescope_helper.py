#!/usr/bin/env python3
"""
Gamescope Helper - A utility to generate Gamescope launch commands for Steam
"""
import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QSpinBox, QComboBox, QRadioButton, QCheckBox,
    QLineEdit, QPushButton, QLabel, QButtonGroup, QGroupBox,
    QFrame, QScrollArea, QStackedWidget
)
from PyQt6.QtGui import QGuiApplication, QIcon, QPixmap
from PyQt6.QtCore import Qt


class GamescopeHelper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gamescope Helper")
        self.setMinimumWidth(500)
        self.resize(600, 700)
        self._setup_ui()
        self._connect_signals()
        self._update_command()

    def _setup_ui(self):
        # Main stacked widget to handle welcome screen and main interface
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Welcome screen
        self._create_welcome_screen()
        
        # Main interface
        self._create_main_interface()
        
        # Start with welcome screen
        self.stacked_widget.setCurrentIndex(0)

    def _create_welcome_screen(self):
        welcome_widget = QWidget()
        welcome_layout = QVBoxLayout(welcome_widget)
        welcome_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_layout.setSpacing(20)
        welcome_layout.setContentsMargins(20, 20, 20, 20)
        
        # Icon/Logo
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Try to use the PNG icon if available
        if os.path.exists("gamescope helper.png"):
            pixmap = QPixmap("gamescope helper.png")
            if not pixmap.isNull():
                # Scale the pixmap to a reasonable size
                scaled_pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                icon_label.setPixmap(scaled_pixmap)
        else:
            # Fallback to emoji
            icon_label.setText("🎮")
            font = icon_label.font()
            font.setPointSize(48)
            icon_label.setFont(font)
        welcome_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel("Gamescope Helper")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = title_label.font()
        font.setPointSize(24)
        font.setBold(True)
        title_label.setFont(font)
        welcome_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("Generate Gamescope launch commands for Steam")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setMaximumWidth(350)
        welcome_layout.addWidget(desc_label)
        
        # Start button
        start_button = QPushButton("Get Started")
        start_button.setMinimumSize(180, 45)
        font = start_button.font()
        font.setPointSize(10)
        start_button.setFont(font)
        start_button.clicked.connect(self._show_main_interface)
        welcome_layout.addWidget(start_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.stacked_widget.addWidget(welcome_widget)

    def _create_main_interface(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(16, 16, 16, 16)
        
        # Create scroll area for the main content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        main_layout.addWidget(scroll_area)
        
        # Content widget inside scroll area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(10)
        scroll_area.setWidget(content_widget)
        
        # --- Gamescope Master Switch ---
        self.enable_gamescope = QCheckBox("Habilitar Gamescope (Master Switch)")
        self.enable_gamescope.setChecked(True)
        self.enable_gamescope.setToolTip("Enable or disable Gamescope entirely")
        content_layout.addWidget(self.enable_gamescope)
        
        # --- Game Resolution ---
        self.game_res_group = QGroupBox("Game Resolution")
        game_res_layout = QGridLayout(self.game_res_group)
        self.spin_w = QSpinBox()
        self.spin_w.setRange(0, 99999)
        self.spin_w.setSuffix(" px")
        self.spin_w.setToolTip("Internal game width (-w)")
        self.spin_h = QSpinBox()
        self.spin_h.setRange(0, 99999)
        self.spin_h.setSuffix(" px")
        self.spin_h.setToolTip("Internal game height (-h)")
        game_res_layout.addWidget(QLabel("Width (-w):"), 0, 0)
        game_res_layout.addWidget(self.spin_w, 0, 1)
        game_res_layout.addWidget(QLabel("Height (-h):"), 1, 0)
        game_res_layout.addWidget(self.spin_h, 1, 1)
        content_layout.addWidget(self.game_res_group)
        
        # --- Output Resolution ---
        self.out_res_group = QGroupBox("Output Resolution")
        out_res_layout = QGridLayout(self.out_res_group)
        self.spin_W = QSpinBox()
        self.spin_W.setRange(0, 99999)
        self.spin_W.setSuffix(" px")
        self.spin_W.setToolTip("Gamescope output width (-W)")
        self.spin_H = QSpinBox()
        self.spin_H.setRange(0, 99999)
        self.spin_H.setSuffix(" px")
        self.spin_H.setToolTip("Gamescope output height (-H)")
        out_res_layout.addWidget(QLabel("Width (-W):"), 0, 0)
        out_res_layout.addWidget(self.spin_W, 0, 1)
        out_res_layout.addWidget(QLabel("Height (-H):"), 1, 0)
        out_res_layout.addWidget(self.spin_H, 1, 1)
        content_layout.addWidget(self.out_res_group)
        
        # --- Refresh Rate ---
        self.hz_group = QGroupBox("Refresh Rate")
        hz_layout = QHBoxLayout(self.hz_group)
        self.spin_r = QSpinBox()
        self.spin_r.setRange(0, 999)
        self.spin_r.setSuffix(" Hz")
        self.spin_r.setSpecialValueText("Default")
        self.spin_r.setToolTip("Display refresh rate (-r)")
        hz_layout.addWidget(QLabel("Frequency (-r):"))
        hz_layout.addWidget(self.spin_r)
        hz_layout.addStretch()
        content_layout.addWidget(self.hz_group)
        
        # --- Scaling ---
        self.scaling_group = QGroupBox("Scaling")
        scaling_layout = QGridLayout(self.scaling_group)
        self.combo_scaling = QComboBox()
        self.combo_scaling.addItem("Default", "")
        self.combo_scaling.addItem("Stretch", "stretch")
        self.combo_scaling.addItem("Integer", "integer")
        self.combo_scaling.setToolTip("Scaling mode (-S)")
        scaling_layout.addWidget(QLabel("Scaling (-S):"), 0, 0)
        scaling_layout.addWidget(self.combo_scaling, 0, 1)
        content_layout.addWidget(self.scaling_group)
        
        self.combo_upscaling = QComboBox()
        self.combo_upscaling.addItem("None", "")
        self.combo_upscaling.addItem("FSR", "fsr")
        self.combo_upscaling.addItem("NIS", "nis")
        self.combo_upscaling.setToolTip("Upscaling (-F)")
        scaling_layout.addWidget(QLabel("Upscaling (-F):"), 1, 0)
        scaling_layout.addWidget(self.combo_upscaling, 1, 1)
        content_layout.addWidget(self.scaling_group)
        
        # --- Display Mode ---
        self.display_group_box = QGroupBox("Display Mode")
        display_layout = QHBoxLayout(self.display_group_box)
        self.radio_window = QRadioButton("Window (Default)")
        self.radio_window.setChecked(True)
        self.radio_window.setToolTip("Windowed mode")
        self.radio_fullscreen = QRadioButton("Fullscreen (-f)")
        self.radio_fullscreen.setToolTip("Fullscreen mode")
        self.radio_borderless = QRadioButton("Borderless (-b)")
        self.radio_borderless.setToolTip("Borderless windowed mode")
        self.display_group = QButtonGroup(self)
        self.display_group.addButton(self.radio_window, 0)
        self.display_group.addButton(self.radio_fullscreen, 1)
        self.display_group.addButton(self.radio_borderless, 2)
        display_layout.addWidget(self.radio_window)
        display_layout.addWidget(self.radio_fullscreen)
        display_layout.addWidget(self.radio_borderless)
        content_layout.addWidget(self.display_group_box)
        
        # --- Proton Settings ---
        proton_group = QGroupBox("Proton Settings")
        proton_layout = QVBoxLayout(proton_group)
        dll_layout = QHBoxLayout()
        dll_layout.addWidget(QLabel("WINEDLLOVERRIDES (comma-separated):"))
        self.dll_overrides_input = QLineEdit()
        self.dll_overrides_input.setPlaceholderText("dxgi,dinput8")
        self.dll_overrides_input.setToolTip("DLLs to override (format: dll1,dll2)")
        dll_layout.addWidget(self.dll_overrides_input)
        proton_layout.addLayout(dll_layout)
        content_layout.addWidget(proton_group)
        
        # --- Other Settings ---
        self.other_group = QGroupBox("Other Settings")
        other_layout = QVBoxLayout(self.other_group)
        self.check_grab = QCheckBox("Capture mouse cursor (--force-grab-cursor / -g)")
        self.check_grab.setToolTip("Force grab cursor")
        other_layout.addWidget(self.check_grab)
        self.check_feral = QCheckBox("Feral Gamemode (gamemoderun)")
        self.check_feral.setToolTip("Run with gamemoderun wrapper")
        other_layout.addWidget(self.check_feral)
        sharp_layout = QHBoxLayout()
        sharp_layout.addWidget(QLabel("FSR Sharpness (--sharpness):"))
        self.spin_sharpness = QSpinBox()
        self.spin_sharpness.setRange(0, 20)
        self.spin_sharpness.setValue(5)
        self.spin_sharpness.setSuffix(" (0-20)")
        self.spin_sharpness.setToolTip("FSR sharpness level")
        sharp_layout.addWidget(self.spin_sharpness)
        sharp_layout.addStretch()
        other_layout.addLayout(sharp_layout)
        content_layout.addWidget(self.other_group)
        
        # --- Environment Variables ---
        env_group = QGroupBox("Environment Variables")
        env_layout = QVBoxLayout(env_group)
        self.check_clear_preload = QCheckBox("Limpar LD_PRELOAD")
        self.check_clear_preload.setToolTip('Adiciona LD_PRELOAD=""')
        env_layout.addWidget(self.check_clear_preload)
        self.check_mesa_anti_lag = QCheckBox("Mesa Anti-Lag")
        self.check_mesa_anti_lag.setToolTip('Adiciona ENABLE_LAYER_MESA_ANTI_LAG=1')
        env_layout.addWidget(self.check_mesa_anti_lag)
        self.check_vkbasalt = QCheckBox("vkBasalt")
        self.check_vkbasalt.setToolTip('Adiciona ENABLE_VKBASALT=1')
        env_layout.addWidget(self.check_vkbasalt)
        content_layout.addWidget(env_group)
        
        # --- Output Area ---
        output_layout = QVBoxLayout()
        output_layout.setSpacing(8)
        output_label = QLabel("Generated Command:")
        output_layout.addWidget(output_label)
        self.cmd_output = QLineEdit()
        self.cmd_output.setReadOnly(True)
        self.cmd_output.setPlaceholderText("Command will appear here as you change options...")
        self.cmd_output.setMinimumHeight(30)
        output_layout.addWidget(self.cmd_output)
        btn_layout = QHBoxLayout()
        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.setEnabled(False)
        self.copy_btn.setMinimumHeight(35)
        btn_layout.addStretch()
        btn_layout.addWidget(self.copy_btn)
        output_layout.addLayout(btn_layout)
        content_layout.addLayout(output_layout)
        
        # Add stretch to push everything to top
        content_layout.addStretch()
        main_layout.addLayout(content_layout)
        self.stacked_widget.addWidget(main_widget)

    def _connect_signals(self):
        self.spin_w.valueChanged.connect(self._update_command)
        self.spin_h.valueChanged.connect(self._update_command)
        self.spin_W.valueChanged.connect(self._update_command)
        self.spin_H.valueChanged.connect(self._update_command)
        self.spin_r.valueChanged.connect(self._update_command)
        self.combo_scaling.currentIndexChanged.connect(self._update_command)
        self.combo_upscaling.currentIndexChanged.connect(self._update_command)
        self.display_group.buttonClicked.connect(self._update_command)
        self.check_grab.stateChanged.connect(self._update_command)
        self.check_feral.stateChanged.connect(self._update_command)
        self.spin_sharpness.valueChanged.connect(self._update_command)
        self.check_clear_preload.stateChanged.connect(self._update_command)
        self.check_mesa_anti_lag.stateChanged.connect(self._update_command)
        self.check_vkbasalt.stateChanged.connect(self._update_command)
        self.dll_overrides_input.textChanged.connect(self._update_command)
        self.enable_gamescope.stateChanged.connect(self._update_gamescope_enabled)
        self.copy_btn.clicked.connect(self._copy_to_clipboard)
        self.combo_upscaling.currentIndexChanged.connect(self._on_upscaling_changed)
        self._on_upscaling_changed()
        self._update_gamescope_enabled()

    def _on_upscaling_changed(self):
        is_fsr = self.combo_upscaling.currentData() == "fsr"
        self.spin_sharpness.setEnabled(is_fsr)

    def _update_gamescope_enabled(self):
        enabled = self.enable_gamescope.isChecked()
        self.game_res_group.setEnabled(enabled)
        self.out_res_group.setEnabled(enabled)
        self.hz_group.setEnabled(enabled)
        self.scaling_group.setEnabled(enabled)
        self.display_group_box.setEnabled(enabled)
        self.other_group.setEnabled(enabled)
        self._update_command()

    def _update_command(self):
        env_vars = []

        # Environment variables
        if self.check_clear_preload.isChecked():
            env_vars.append('LD_PRELOAD=""')
        if self.check_mesa_anti_lag.isChecked():
            env_vars.append('ENABLE_LAYER_MESA_ANTI_LAG=1')
        if self.check_vkbasalt.isChecked():
            env_vars.append('ENABLE_VKBASALT=1')

        # WINEDLLOVERRIDES
        dll_overrides = self.dll_overrides_input.text().strip()
        if dll_overrides:
            overrides = ";".join([f"{dll.strip()}=n,b" for dll in dll_overrides.split(",")])
            env_vars.append(f'WINEDLLOVERRIDES="{overrides}"')

        # Add gamemoderun wrapper if enabled
        if self.check_feral.isChecked():
            env_vars.append("gamemoderun")

        parts = []
        if env_vars:
            parts.extend(env_vars)

        # Gamescope command
        if self.enable_gamescope.isChecked():
            gamescope_parts = ["gamescope"]

            if self.spin_w.value() > 0:
                gamescope_parts.extend(["-w", str(self.spin_w.value())])
            if self.spin_h.value() > 0:
                gamescope_parts.extend(["-h", str(self.spin_h.value())])
            if self.spin_W.value() > 0:
                gamescope_parts.extend(["-W", str(self.spin_W.value())])
            if self.spin_H.value() > 0:
                gamescope_parts.extend(["-H", str(self.spin_H.value())])

            if self.spin_r.value() > 0:
                gamescope_parts.extend(["-r", str(self.spin_r.value())])

            scaling_val = self.combo_scaling.currentData()
            if scaling_val:
                gamescope_parts.extend(["-S", scaling_val])

            upscale_val = self.combo_upscaling.currentData()
            if upscale_val:
                gamescope_parts.extend(["-F", upscale_val])
            if upscale_val == "fsr" and self.spin_sharpness.value() > 0:
                gamescope_parts.extend(["--sharpness", str(self.spin_sharpness.value())])

            checked = self.display_group.checkedId()
            if checked == 1:
                gamescope_parts.append("-f")
            elif checked == 2:
                gamescope_parts.append("-b")

            if self.check_grab.isChecked():
                gamescope_parts.append("--force-grab-cursor")

            gamescope_parts.append("--")
            parts.extend(gamescope_parts)

        parts.append("%command%")
        cmd = " ".join(parts)
        self.cmd_output.setText(cmd)
        self.copy_btn.setEnabled(True)

    def _copy_to_clipboard(self):
        QGuiApplication.clipboard().setText(self.cmd_output.text())

    def _show_main_interface(self):
        self.stacked_widget.setCurrentIndex(1)

    def _show_welcome_screen(self):
        self.stacked_widget.setCurrentIndex(0)

    def closeEvent(self, event):
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Gamescope Helper")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("GamescopeHelper")
    
    # Set application icon if available
    if os.path.exists("gamescope helper.png"):
        app.setWindowIcon(QIcon("gamescope helper.png"))
    elif os.path.exists("gamescope helper.ico"):
        app.setWindowIcon(QIcon("gamescope helper.ico"))
    
    window = GamescopeHelper()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()