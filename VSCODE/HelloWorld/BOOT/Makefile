CC = xtensa-esp32-elf-gcc
AS = xtensa-esp32-elf-gcc
OBJCOPY = xtensa-esp32-elf-objcopy

CFLAGS = -mlongcalls -Wall -Werror -nostdlib -mtext-section-literals -g
ASFLAGS = -mlongcalls -nostdlib -g
LDFLAGS = -nostdlib -Wl,--gc-sections -T linker.ld -Wl,-Map=bootloader.map

SRC_C = main_bootloader.c
SRC_ASM = startup.s

OBJ_C = $(SRC_C:.c=.o)
OBJ_ASM = $(SRC_ASM:.S=.o)
OBJS = $(OBJ_C) $(OBJ_ASM)

all: bootloader.bin

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

%.o: %.S
	$(AS) $(ASFLAGS) -c $< -o $@

bootloader.elf: $(OBJS)
	$(CC) $(LDFLAGS) $^ -o $@

bootloader.bin: bootloader.elf
	$(OBJCOPY) -O binary $< $@

clean:
	del /Q *.o *.elf *.map *.bin 2>nul
