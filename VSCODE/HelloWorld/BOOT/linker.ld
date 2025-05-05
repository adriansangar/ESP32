ENTRY(_start)

MEMORY
{
    iram (rx)  : ORIGIN = 0x40080000, LENGTH = 0x20000   /* Instrucciones */
    dram (rw)  : ORIGIN = 0x3FFB0000, LENGTH = 0x20000   /* Datos */
}

SECTIONS
{
    .text.literal :
    {
        *(.literal .text.literal .literal.*)
    } > iram

    .text :
    {
        *(.text .text.*)
    } > iram

    .rodata :
    {
        *(.rodata .rodata.*)
    } > dram

    .data :
    {
        _sdata = .;
        *(.data)
        _edata = .;
    } > dram

    .bss :
    {
         _bss_start = .;
        *(.bss)
        *(COMMON)
        _bss_end = .;
    } > dram

    .stack (COPY) :
    {
        _stack_top = .;
    } > dram
}
