from machine import Pin, UART
import time

# Configuration constants
MODBUS_BAUD = 9600
MODBUS_RX_PIN = 16
MODBUS_TX_PIN = 17
MODBUS_ENABLE_PIN = 4

# Initialize UART with the specified baud rate and pins
uart = UART(2, baudrate=MODBUS_BAUD, tx=Pin(MODBUS_TX_PIN), rx=Pin(MODBUS_RX_PIN))

# Initialize the enable pin for RS485 transceiver
enable_pin = Pin(MODBUS_ENABLE_PIN, Pin.OUT)

# Function to send data over RS485
def send_data(data):
    enable_pin.value(1)  # Enable the transceiver for sending
    uart.write(data)
    time.sleep(0.1)
    enable_pin.value(0)  # Disable the transceiver after sending
    

# Main loop to send data continuously
while True:
    send_data('hello...\n')
    print('hello...')
    time.sleep(1)

