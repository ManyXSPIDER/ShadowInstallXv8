#!/usr/bin/env bash

set -u

APP_URL="https://shadowinstallxv8.onrender.com/shadowxv.py"
APP_FILE="shadowxv.py"
LOG_FILE="shadowxv.log"

echo "======================================"
echo "      ShadowXV Python Auto Installer"
echo "======================================"
echo

# --------------------------------------
# Detect OS
# --------------------------------------
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "[ShadowXV] OS: ${PRETTY_NAME:-unknown}"
else
    echo "[ShadowXV] Cannot Detect Operating System"
    exit 1
fi

echo "[ShadowXV] Architecture: $(uname -m)"
echo

# --------------------------------------
# Root / sudo
# --------------------------------------
if [ "$(id -u)" -eq 0 ]; then
    SUDO=""
elif command -v sudo >/dev/null 2>&1; then
    SUDO="sudo"
else
    echo "[ShadowXV] Root or Sudo Is Required"
    exit 1
fi

# --------------------------------------
# Detect Package Manager
# --------------------------------------
echo "[ShadowXV] Detecting Package Manager"

if command -v apt-get >/dev/null 2>&1; then
    PKG="apt"
elif command -v dnf >/dev/null 2>&1; then
    PKG="dnf"
elif command -v yum >/dev/null 2>&1; then
    PKG="yum"
elif command -v apk >/dev/null 2>&1; then
    PKG="apk"
elif command -v pacman >/dev/null 2>&1; then
    PKG="pacman"
elif command -v zypper >/dev/null 2>&1; then
    PKG="zypper"
else
    PKG=""
fi

if [ -z "$PKG" ]; then
    echo "[ShadowXV] No Supported Package Manager Found"
    exit 1
fi

echo "[ShadowXV] Package Manager: $PKG"
echo

# --------------------------------------
# Update System
# --------------------------------------
echo "[+] Updating system..."

case "$PKG" in

    apt)
        if ! $SUDO apt-get update; then
            echo "[ShadowXV] Apt Update Failed"
            exit 1
        fi

        $SUDO apt-get upgrade -y
        ;;

    dnf)
        if ! $SUDO dnf makecache; then
            echo "[ShadowXV] Dnf Update Failed"
            exit 1
        fi

        $SUDO dnf upgrade -y
        ;;

    yum)
        if ! $SUDO yum makecache; then
            echo "[ShadowXV] Yum Update Failed"
            exit 1
        fi

        $SUDO yum update -y
        ;;

    apk)
        if ! $SUDO apk update; then
            echo "[ShadowXV] Apk Update Failed"
            exit 1
        fi

        $SUDO apk upgrade
        ;;

    pacman)
        if ! $SUDO pacman -Syu --noconfirm; then
            echo "[ShadowXV] Pacman Update Failed"
            exit 1
        fi
        ;;

    zypper)
        if ! $SUDO zypper refresh; then
            echo "[ShadowXV] Zypper Refresh Failed."
            exit 1
        fi

        $SUDO zypper update -y
        ;;

esac

echo
echo "[ShadowXV] System Update Complete"
echo

# --------------------------------------
# Install Python
# --------------------------------------
if command -v python3 >/dev/null 2>&1; then

    echo "[ShadowXV] Python Already Installed"
    python3 --version

else

    echo "[ShadowXV] Python Not Found"
    echo "[ShadowXV] Installing Python"

    case "$PKG" in

        apt)
            $SUDO apt-get install -y python3
            ;;

        dnf)
            $SUDO dnf install -y python3
            ;;

        yum)
            $SUDO yum install -y python3
            ;;

        apk)
            $SUDO apk add python3
            ;;

        pacman)
            $SUDO pacman -S --noconfirm python
            ;;

        zypper)
            $SUDO zypper install -y python3
            ;;

    esac

fi

# --------------------------------------
# Verify Python
# --------------------------------------
echo

if ! command -v python3 >/dev/null 2>&1; then
    echo "[ShadowXV] Python 3 Installation Failed"
    exit 1
fi

echo "[ShadowXV] Python 3:"
python3 --version
echo

# --------------------------------------
# Checked wget
# --------------------------------------
if command -v wget >/dev/null 2>&1; then

    echo "[ShadowXV] wget Already Installed"
    wget --version | head -n 1

else

    echo "[ShadowXV] wget Not Found"
    echo "[ShadowXV] Installing Wget"

    case "$PKG" in

        apt)
            $SUDO apt-get install -y wget
            ;;

        dnf)
            $SUDO dnf install -y wget
            ;;

        yum)
            $SUDO yum install -y wget
            ;;

        apk)
            $SUDO apk add wget
            ;;

        pacman)
            $SUDO pacman -S --noconfirm wget
            ;;

        zypper)
            $SUDO zypper install -y wget
            ;;

        *)
            echo "[ShadowXV] Cannot Automatically Install Wget"
            exit 1
            ;;

    esac
fi

# --------------------------------------
# Verify Wget
# --------------------------------------
echo

if ! command -v wget >/dev/null 2>&1; then
    echo "[ShadowXV] Wget Installation Failed"
    exit 1
fi

echo "[ShadowXV] Wget Ready"
echo

# --------------------------------------
# Download
# --------------------------------------
echo "[ShadowXV] Downloading shadowxv.py"
echo

if ! wget -O "$APP_FILE" "$APP_URL"; then
    echo "[ShadowXV] Failed To Download shadowxv.py"
    rm -f "$APP_FILE"
    exit 1
fi

# --------------------------------------
# Verify Downloaded File
# --------------------------------------
if [ ! -s "$APP_FILE" ]; then
    echo "[ShadowXV] Downloaded shadowxv.py Is Empty"
    rm -f "$APP_FILE"
    exit 1
fi

echo
echo "[ShadowXV] shadowxv.py Downloaded Successfully"
echo "[ShadowXV] Size: $(wc -c < "$APP_FILE") Bytes"
echo

# --------------------------------------
# Stop Previous Instance If Running
# --------------------------------------
if pgrep -f "python3.*${APP_FILE}" >/dev/null 2>&1; then
    echo "[ShadowXV] Existing shadowxv.py Process Found"
    echo "[ShadowXV] Stopping Process"

    pkill -f "python3.*${APP_FILE}" || true
    sleep 1
fi

# --------------------------------------
# Starting
# --------------------------------------
echo "[ShadowXV] Starting"

nohup python3 "$APP_FILE" > "$LOG_FILE" 2>&1 &

APP_PID=$!

sleep 2

# --------------------------------------
# Verify Process
# --------------------------------------
if kill -0 "$APP_PID" >/dev/null 2>&1; then

    echo
    echo "======================================"
    echo "           ShadowXV Is GG"
    echo "======================================"
    echo
    echo "PID:  $APP_PID"
    echo "File: $(pwd)/$APP_FILE"
    echo "Log:  $(pwd)/$LOG_FILE"
    echo clear
    echo

else

    echo
    echo "[ShadowXV] Exited Immediately"
    echo "[ShadowXV] Last Log Output:"
    echo "--------------------------------------"
    tail -30 "$LOG_FILE" 2>/dev/null || true
    echo "--------------------------------------"
    exit 1

fi
