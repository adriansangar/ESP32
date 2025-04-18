# ESP32

ESP32 WROOM 32D

## 09.03.2025

### Summary of Today's Steps

#### 1. Understanding the ESP-IDF Build Process

We reviewed the key steps in the ESP-IDF build process:

Project Configuration: Using CMake to generate the build system.

Compilation: Compiling source files (.c, .cpp) into object files (.o) using Ninja.

Linking: Linking objects and libraries to generate the .elf file.

Binary Generation: Converting the .elf file into a .bin file for flashing.

Key tools involved:

CMake: For generating the build system.

Ninja: For executing the build rules.

xtensa-esp32-elf-gcc: The cross-compiler for ESP32.

esptool.py: For flashing the firmware.

#### 2. Setting Up a Basic Python Environment

We created a Python script (my_idf.py) to automate the build process.

The script uses subprocess to run commands like cmake and ninja.

#### 3. Installing Missing Tools

We installed CMake and Ninja:

CMake: Downloaded and installed from cmake.org.

Ninja: Downloaded from GitHub and added to the PATH.

#### 4. Configuring the ESP-IDF Environment

We ensured the ESP-IDF environment was set up correctly:

Ran export.bat to configure environment variables:
Verified the PATH included the compiler (xtensa-esp32-elf-gcc).

#### 5. Next Steps

Once the environment is fully configured, the script (my_idf.py) should:

Generate the build system with cmake.

Compile the project with ninja.

Generate the .elf file in the build/ folder.

Compare the output with idf.py build -v to ensure consistency.

## 17.04.2025

Today i figured out that my python code done the last day does not work properly so I am going to start another folder, and another process.
First of all, i check out that the compiler is installed properly with the following command 'xtensa-esp32-elf-gcc --version'. Positive response.
