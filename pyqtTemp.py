import Adafruit_GPIO
from Adafruit_MAX31856 import MAX31856 as MAX31856

# Raspberry Pi hardware SPI configuration.
SPI_PORT   = 0
SPI_DEVICE = 0

class adatemp:
	def __init__(self):
		self.sensor = MAX31856(hardware_spi=Adafruit_GPIO.SPI.SpiDev(SPI_PORT, SPI_DEVICE))
	
	def temp(self):
		return self.sensor.read_temp_c()
