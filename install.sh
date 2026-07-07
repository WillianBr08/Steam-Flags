#!/bin/bash

INSTALL_DIR="$HOME/.local/bin"
REPO="WillianBr08/Steam-Flags"
APP_NAME="Steam_Flags-x86_64.AppImage"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"

echo "=== Steam Flags Installer ==="
echo ""

# [1] Baixar AppImage
echo "[1/4] Baixando Steam Flags..."
mkdir -p "$INSTALL_DIR"
if ! curl -fsSL "https://github.com/$REPO/releases/latest/download/$APP_NAME" -o "$INSTALL_DIR/steam-flags"; then
    echo "ERRO: Falha ao baixar o AppImage"
    exit 1
fi
chmod +x "$INSTALL_DIR/steam-flags"
echo "OK"

# [2] Baixar icone
echo "[2/4] Baixando icone..."
mkdir -p "$ICON_DIR"
if ! curl -fsSL "https://raw.githubusercontent.com/$REPO/main/SteamFlags.png" -o "$ICON_DIR/steam-flags.png"; then
    echo "ERRO: Falha ao baixar icone"
    exit 1
fi
echo "OK"

# [3] Criar .desktop
echo "[3/4] Criando atalho no menu..."
mkdir -p "$DESKTOP_DIR"

cat > "$DESKTOP_DIR/steam-flags.desktop" << DESKTOP
[Desktop Entry]
Name=Steam Flags
Exec=$INSTALL_DIR/steam-flags
Icon=$ICON_DIR/steam-flags.png
Type=Application
Comment=Configure Steam launch options for Linux gaming.
Terminal=false
Categories=Utility;
StartupNotify=true
DESKTOP

chmod +x "$DESKTOP_DIR/steam-flags.desktop"

# Atualizar caches
update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor/" 2>/dev/null || true
echo "OK"

# [4] Configurar PATH
echo "[4/4] Configurando PATH..."
export PATH="$HOME/.local/bin:$PATH"

if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$HOME/.bashrc" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi
echo "OK"

echo ""
echo "==========================="
echo "Steam Flags instalado!"
echo ""
echo "Execute: steam-flags"
echo "==========================="
