#include <stdint.h>

// Dirección base de los registros UART0
#define UART0_BASE 0x3FF40000

#define UART_FIFO_REG       (*(volatile uint32_t *)(UART0_BASE + 0x0))
#define UART_INT_RAW_REG    (*(volatile uint32_t *)(UART0_BASE + 0x4))
#define UART_INT_ST_REG     (*(volatile uint32_t *)(UART0_BASE + 0x8))
#define UART_INT_ENA_REG    (*(volatile uint32_t *)(UART0_BASE + 0xC))
#define UART_INT_CLR_REG    (*(volatile uint32_t *)(UART0_BASE + 0x10))
#define UART_CLKDIV_REG     (*(volatile uint32_t *)(UART0_BASE + 0x14))
#define UART_CONF0_REG      (*(volatile uint32_t *)(UART0_BASE + 0x20))
#define UART_CONF1_REG      (*(volatile uint32_t *)(UART0_BASE + 0x24))
#define UART_STATUS_REG     (*(volatile uint32_t *)(UART0_BASE + 0x1C))

// Frecuencia de reloj APB por defecto en ESP32 (80 MHz)
#define APB_CLK_FREQ 80000000
#define BAUD_RATE    115200

void uart_init()
{
    // Divisor de reloj: clk_div = (APB_CLK * 16) / baudrate
    UART_CLKDIV_REG = ((APB_CLK_FREQ << 4) / BAUD_RATE);  // formato Q4

    // Configuración UART: 8N1 (8 bits, sin paridad, 1 stop)
    UART_CONF0_REG = 0;

    // FIFO: se puede dejar por defecto
    UART_CONF1_REG = 0;
}

void uart_send_char(char c)
{
    // Espera a que haya espacio en el FIFO
    while ((UART_STATUS_REG >> 16) & 0xFF); // FIFO lleno

    UART_FIFO_REG = c;
}

void uart_send_str(const char *str)
{
    while (*str)
    {
        uart_send_char(*str++);
    }
}

void bootloader_main()
{
    uart_init();
    uart_send_str("Hello from bootloader!\r\n");

    while (1)
    {
        // Quedarse aquí para evitar reinicios
    }
}
