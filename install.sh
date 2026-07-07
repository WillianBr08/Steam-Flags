#!/bin/bash
set -e

INSTALL_DIR="$HOME/.local/bin"
REPO="WillianBr08/Gamescope-Helper"
APP_NAME="Gamescope_Helper-x86_64.AppImage"

echo "Baixando Steam Flags..."
mkdir -p "$INSTALL_DIR"
curl -fsSL "https://github.com/$REPO/releases/latest/download/$APP_NAME" -o "$INSTALL_DIR/steam-flags"
chmod +x "$INSTALL_DIR/steam-flags"

if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$HOME/.bashrc"
    echo "Adicionado ao PATH. Reinicie o terminal ou execute:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo "Steam Flags instalado em $INSTALL_DIR/steam-flags"
echo "Execute: steam-flags"
