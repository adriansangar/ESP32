CC = xtensa-esp32-elf-gcc
AS = xtensa-esp32-elf-gcc
OBJCOPY = xtensa-esp32-elf-objcopy

CFLAGS = -mlongcalls -Wall -Werror -nostdlib -mtext-section-literals
ASFLAGS = -mlongcalls -nostdlib
LDFLAGS = -nostdlib -Wl,--gc-sections -T linker_script.ld -Wl,-Map=firmware.map

SRC_C = main.c
SRC_ASM = startup/startup.S

OBJ_C = $(SRC_C:.c=.o)
OBJ_ASM = $(SRC_ASM:.S=.o)
OBJS = $(OBJ_C) $(OBJ_ASM)

all: firmware.bin

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

%.o: %.S
	$(AS) $(ASFLAGS) -c $< -o $@

firmware.elf: $(OBJS)
	$(CC) $(LDFLAGS) $^ -o $@

firmware.bin: firmware.elf
	$(OBJCOPY) -O binary $< $@

clean:
	del /Q *.o *.elf *.map *.bin 2>nul
	del /Q startup\*.o 2>nul