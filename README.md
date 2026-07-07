<p align="center">
  <img src="SteamFlags.png" width="100" alt="Steam Flags">
</p>

<h1 align="center">Steam Flags</h1>

<p align="center">
  Configure opcoes de lancamento do Steam para Linux.<br>
  Configure Steam launch options for Linux gaming.
</p>

<p align="center">
  <code>Gamescope · FSR · NIS · Gamemode · Multi-idioma</code>
</p>

---

## Instalacao

```bash
curl -fsSL https://raw.githubusercontent.com/WillianBr08/Steam-Flags/main/install.sh | bash
```

Ou baixe o AppImage em [Releases](https://github.com/WillianBr08/Steam-Flags/releases).

## Como usar

1. Abra o Steam Flags
2. Configure as opcoes de Gamescope
3. Copie o comando gerado
4. Cole nas opcoes de inicializacao do jogo no Steam

```
gamemoderun gamescope -w 1280 -h 720 -W 1920 -H 1080 -r 60 -F fsr --sharpness 8 -f -- %command%
```

## Features

- Resolucao dupla (jogo + saida)
- Upscaling com FSR e NIS
- Sharpness ajustavel
- Modo de tela: janela, fullscreen, borderless
- Feral Gamemode
- Variaveis de ambiente (LD_PRELOAD, AMD Anti-Lag, VKBasalt)
- Preview do comando em tempo real
- Copiar com um clique
- Multi-idioma (Portugues, Ingles, Sistema)
- Temas (System, Light, Dark)

## Rodar do codigo fonte

```bash
pip install PyGObject
sudo apt install libgtk-4-dev libadwaita-1-dev
glib-compile-schemas schemas/
GSETTINGS_SCHEMA_DIR=schemas python3 steam_flags.py
```

## Building

```bash
pip install pyinstaller
pyinstaller --onefile --windowed steam_flags.py
```


<p align="center">
  <sub>Steam Flags v0.3.0 · Open Source · Linux</sub>
</p>

---

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/WillianBr08/Steam-Flags/main/install.sh | bash
```

Or download the AppImage from [Releases](https://github.com/WillianBr08/Steam-Flags/releases).

## How to use

1. Open Steam Flags
2. Configure your Gamescope settings
3. Copy the generated command
4. Paste it into Steam's launch options for your game

```
gamemoderun gamescope -w 1280 -h 720 -W 1920 -H 1080 -r 60 -F fsr --sharpness 8 -f -- %command%
```

## Features

- Dual resolution (game + output)
- FSR and NIS upscaling
- Adjustable sharpness
- Display modes: windowed, fullscreen, borderless
- Feral Gamemode
- Environment variables (LD_PRELOAD, AMD Anti-Lag, VKBasalt)
- Real-time command preview
- One-click copy
- Multi-language (Portuguese, English, System)
- Themes (System, Light, Dark)

## Run from source

```bash
pip install PyGObject
sudo apt install libgtk-4-dev libadwaita-1-dev
glib-compile-schemas schemas/
GSETTINGS_SCHEMA_DIR=schemas python3 steam_flags.py
```

## Building

```bash
pip install pyinstaller
pyinstaller --onefile --windowed steam_flags.py
```


<p align="center">
  <sub>Steam Flags v0.3.0 · Open Source · Linux</sub>
</p>
