"""
This example shows connecting to the PN532 with I2C (requires clock
stretching support), SPI, or UART. SPI is best, it uses the most pins but
is the most reliable and universally supported.
After initialization, try waving various 13.56MHz RFID cards over it!
"""

import board
import busio
from digitalio import DigitalInOut
#
# NOTE: pick the import that matches the interface being used
#
# from adafruit_pn532.i2c import PN532_I2C
from adafruit_pn532.spi import PN532_SPI
#from adafruit_pn532.uart import PN532_UART

# I2C connection:
# i2c = busio.I2C(board.SCL, board.SDA)

# Non-hardware
#pn532 = PN532_I2C(i2c, debug=False)

# With I2C, we recommend connecting RSTPD_N (reset) to a digital pin for manual
# harware reset
# reset_pin = DigitalInOut(board.D6)
# On Raspberry Pi, you must also connect a pin to P32 "H_Request" for hardware
# wakeup! this means we don't need to do the I2C clock-stretch thing
# req_pin = DigitalInOut(board.D12)
# pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)

# SPI connection:
spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=True)

# UART connection
#uart = busio.UART(board.TX, board.RX, baudrate=115200, timeout=100)
#pn532 = PN532_UART(uart, debug=False)

ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

print('Waiting for RFID/NFC card...')
while True:

    def format_binary(byte_array):
        return ''.join('{:08b}_'.format(i) for i in uid)

    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    print('.', end="")
    # Try again if no card is available.
    if uid is None:
        continue
    print('Found card with UID:', format_binary(uid), flush=True)

    for i in range(0,16):
        block_data = pn532.mifare_classic_read_block(i)
        print('Block {}: '.format(i), format_binary(block_data), flush=True)
    #print(int.from_bytes(uid[1:-1], byteorder='little', signed=False), flush=True)

