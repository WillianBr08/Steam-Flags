#!/bin/bash
set -e

INSTALL_DIR="$HOME/.local/bin"
REPO="WillianBr08/Steam-Flags"
APP_NAME="Steam_Flags-x86_64.AppImage"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons"

echo "Baixando Steam Flags..."
mkdir -p "$INSTALL_DIR"
curl -fsSL "https://github.com/$REPO/releases/latest/download/$APP_NAME" -o "$INSTALL_DIR/steam-flags"
chmod +x "$INSTALL_DIR/steam-flags"

echo "Criando atalho no menu de aplicativos..."
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR/hicolor/256x256/apps"

curl -fsSL "https://raw.githubusercontent.com/$REPO/main/SteamFlags.png" -o "$ICON_DIR/hicolor/256x256/apps/steam-flags.png"

cat > "$DESKTOP_DIR/steam-flags.desktop" << DESKTOP
[Desktop Entry]
Name=Steam Flags
Exec=$INSTALL_DIR/steam-flags
Icon=steam-flags
Type=Application
Comment=Configure Steam launch options for Linux gaming.
Terminal=false
Categories=Utility;
DESKTOP

chmod +x "$DESKTOP_DIR/steam-flags.desktop"
update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true

echo "Configurando PATH..."
export PATH="$HOME/.local/bin:$PATH"

if ! grep -q '$HOME/.local/bin' "$HOME/.bashrc" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo "PATH adicionado ao .bashrc"
fi

echo ""
echo "Steam Flags instalado!"
echo "Execute: steam-flags"
