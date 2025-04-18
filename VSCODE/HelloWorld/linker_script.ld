ENTRY(app_main)

MEMORY {
    iram (rwx) : org = 0x40080000, len = 0x20000   /* IRAM del ESP32 */
    dram (rwx) : org = 0x3FFB0000, len = 0x14000    /* DRAM del ESP32 */
}

SECTIONS {
    .iram1.vectors : {
        *(.iram1.vectors)
    } > iram

    .text : {
        *(.text .text.*)
    } > iram

    .data : {
        *(.data)
    } > dram

    .bss : {
        *(.bss)
    } > dram

    /* Pila al final de la DRAM */
    _stack_end = ORIGIN(dram) + LENGTH(dram) - 4;
}