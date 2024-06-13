from machine import Pin, UART, SoftI2C
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

# Initialize I2C for RTC
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# RTC DS3231 address
RTC_ADDR = 0x68

def bcd_to_dec(bcd):
    return (bcd // 16) * 10 + (bcd % 16)

def read_rtc_time():
    try:
        i2c.writeto(RTC_ADDR, b'\x00')  # Set register pointer to 00h
        data = i2c.readfrom(RTC_ADDR, 7)
        
        second = bcd_to_dec(data[0] & 0x7F)
        minute = bcd_to_dec(data[1] & 0x7F)
        hour = bcd_to_dec(data[2] & 0x3F)
        day = bcd_to_dec(data[4] & 0x3F)
        month = bcd_to_dec(data[5] & 0x1F)
        year = bcd_to_dec(data[6]) + 2000  # Assuming year is stored as offset from 2000
        
        return year, month, day, hour, minute, second
    except Exception as e:
        print(f"Error reading RTC time: {e}")
        return None

def send_data(data):
    enable_pin.value(1)  # Enable the transceiver for sending
    uart.write(data)
    time.sleep(0.1)
    enable_pin.value(0)  # Disable the transceiver after sending

# Main loop to send current time continuously
while True:
    rtc_time = read_rtc_time()
    if rtc_time:
        year, month, day, hour, minute, second = rtc_time
        time_string = f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}\n"
        send_data(time_string)
        print(time_string)
    else:
        print("Failed to read time from RTC")
    
    time.sleep(1)
