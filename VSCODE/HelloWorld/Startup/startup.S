.section .iram1.vectors, "ax"
.global _start

_start:
    .literal_position
    movi sp, _stack_end
    call0 hardware_init
    call0 app_main
    loop:
        j loop