import subprocess
import os

def run_command(command):
    """
    Ejecuta un comando en la terminal y muestra la salida.
    """
    print(f"Ejecutando: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)

def main():
    # Configurar el entorno del ESP-IDF
    os.environ["IDF_PATH"] = "C:/Git/esp-idf"  # Ajusta la ruta si es necesario

    # Generar el sistema de construcción con CMake
    run_command("cmake -G Ninja -DPYTHON_DEPS_CHECKED=1 -DESP_PLATFORM=1 -B build")

    # Compilar el proyecto con Ninja
    run_command("ninja -C build")

if __name__ == "__main__":
    main()