import time
import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219

#NOTE: Run with sudo or root privilege, or import board will not work
def getBattery():
    i2c_bus = board.I2C()
    ina1 = INA219(i2c_bus,addr=0x40)
    ina1.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    ina1.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    ina1.bus_voltage_range = BusVoltageRange.RANGE_16V
    return ina1.bus_voltage

if __name__ == '__main__':
    print(getBattery())
