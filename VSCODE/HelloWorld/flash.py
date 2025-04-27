import subprocess
import serial
import time
import sys
import os

def enter_bootloader(port, baud):
    """Forzar modo bootloader manipulando RTS/EN y DTR/BOOT."""
    ser = serial.Serial(port, baud, timeout=1)       # Abrir puerto serie
    ser.setRTS(False); ser.setDTR(False)             # EN=0, BOOT=0
    time.sleep(0.1)
    ser.setRTS(True)                                 # EN=1, BOOT=0 → bootloader
    time.sleep(0.1)
    ser.close()

def run_esptool_command(args):
    """Ejecuta esptool.py con los argumentos dados y comprueba errores."""
    cmd = [sys.executable, "-m", "esptool"] + args
    print("Ejecutando:", " ".join(cmd))
    subprocess.run(cmd, check=True)

def flash_esp32(port, baud, boot_bin, partition_table_bin, app_bin):
    # 1. Entrada al bootloader
    enter_bootloader(port, baud)                          # :contentReference[oaicite:6]{index=6}

    # 2. Borrar la flash completa
    run_esptool_command([
        "--port", port,
        "erase_flash"
    ])                                                      # :contentReference[oaicite:7]{index=7}
        # 3. Escribir el binario en la dirección 0x1000
    run_esptool_command([
        "--port", port,
        "--baud", str(baud),
        "write_flash", "-z", "0x1000", boot_bin
    ])  

        # 3. Escribir el binario en la dirección 0x1000
    run_esptool_command([
        "--port", port,
        "--baud", str(baud),
        "write_flash", "-z", "0x8000", partition_table_bin
    ])    

    # 3. Escribir el binario en la dirección 0x1000
    run_esptool_command([
        "--port", port,
        "--baud", str(baud),
        "write_flash", "-z", "0x10000", app_bin
    ])                                                                                                

    print("¡Flasheo completado!")

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
