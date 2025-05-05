    .section .entry, "ax"
    .align 4
    .global _start

_start:
    call0 zero_bss     // Limpia la sección .bss
    call0 bootloader_main         // Llama a la función principal
    j .                // Bucle infinito al final

// Rellenar la sección .bss a cero
zero_bss:
    movi a0, _bss_start  // Dirección de inicio de .bss
    movi a1, _bss_end    // Dirección de fin de .bss

1:
    beq a0, a1, 2f
    movi a2, 0
    s32i a2, a0, 0
    addi a0, a0, 4
    j 1b
2:
    ret
