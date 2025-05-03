import subprocess
import serial
import time
import sys
import os

def enter_bootloader(port):
    """Secuencia precisa para entrar en modo bootloader (GPIO0 LOW + RESET)."""
    with serial.Serial(port, 115200) as ser:
        ser.dtr = False    # GPIO0 = LOW (modo bootloader)
        ser.rts = True     # EN = LOW (reset)
        time.sleep(0.1)
        ser.rts = False    # EN = HIGH
        time.sleep(0.5)    # Tiempo para estabilizar

def run_esptool_command(args):
    """Ejecuta esptool.py con manejo de errores mejorado."""
    cmd = [sys.executable, "-m", "esptool"] + args
    print("[CMD] " + " ".join(cmd))
    try:
        subprocess.run(cmd, check=True, timeout=30)
    except subprocess.TimeoutExpired:
        print("Error: Tiempo de espera agotado")
        sys.exit(1)

def flash_esp32(port, baud, boot_bin, partition_bin, app_bin):
    # 1. Forzar modo bootloader
    enter_bootloader(port)
    
    # 2. Flashear TODOS los binarios en UN solo comando
    run_esptool_command([
        "--port", port,
        "--baud", str(baud),
        "--after", "hard_reset",  # Reinicio automático al final
        "write_flash",
        "--flash_size", "4MB",
        "--flash_mode", "dio",
        "0x1000", boot_bin,
        "0x8000", partition_bin,
        "0x10000", app_bin
    ])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Flashea un ESP32 usando la CLI de esptool desde Python"
    )
    parser.add_argument("--port", default="COM3",
                        help="Puerto serie (e.g. COM3 o /dev/ttyUSB0)")
    parser.add_argument("--baud", type=int, default=115200,
                        help="Baud rate para write_flash")
    parser.add_argument("--boot", required=True,
                        help="Ruta al boot.bin a flashear")
    parser.add_argument("--partition", required=True,
                        help="Ruta al partition.bin a flashear")
    parser.add_argument("--app", required=True,
                        help="Ruta al app.bin a flashear")
    args = parser.parse_args()

    # Verificar existencia del binario
    if not os.path.isfile(args.boot):
        print(f"ERROR: no existe el bootloader")
        sys.exit(1)
    if not os.path.isfile(args.partition):
        print(f"ERROR: no existe el partition")
        sys.exit(1)
    if not os.path.isfile(args.app):
        print(f"ERROR: no existe el app")
        sys.exit(1)

    flash_esp32(args.port, args.baud, args.boot, args.partition, args.app)
