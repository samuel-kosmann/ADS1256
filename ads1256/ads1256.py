import time

import gpiod
import spidev
from gpiod.line import Direction, Value

from ads1256.ads1256_constants import ADS1256Constants as Ads


class ADS1256:
    def __init__(self, configuration):
        self.configuration = configuration

        self.v_ref = 2.5
        self.pga_gain = 1
        self.volts_per_digit = self.v_ref * 2.0 / (self.pga_gain * (2**23 - 1))

        self._configure_spi()
        self._configure_gpio()

        # Reset the chip to get into a known state.
        self.reset()

        # Read th chip ID to verify if the SPI communcication is working
        # and check if the expected value is returned.
        chip_id = self.read_chip_id()
        if chip_id != 3:
            print(f'ADS1256: Got wronmg chip ID. Expected 3, got {chip_id} instead.')

    def _configure_spi(self):
        self.spi = spidev.SpiDev()
        self.spi.open(
            self.configuration['spi_bus'],
            self.configuration['spi_device'],
        )
        self.spi.max_speed_hz = self.configuration['spi_frequency']
        # The ADS1256 uses SPI MODE 1 this means CPOL=0 and CPHA=1.
        self.spi.mode = 0b01

    def _configure_gpio(self):
        self.DRDY_PIN = self.configuration['data_ready_pin']
        # self.DEBUG_PIN = 21
        self.gpio = gpiod.request_lines(
            '/dev/gpiochip0',
            consumer='ads1256',
            config={
                self.DRDY_PIN: gpiod.LineSettings(direction=Direction.INPUT),
                # self.DEBUG_PIN: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
            },
        )

    def read_register(self, address):
        self.spi.writebytes([Ads.CMD_RREG | address, 0x00])
        time.sleep(Ads.DOUT_DELAY)
        response = self.spi.readbytes(1)[0]
        return response

    def wait_for_data_ready_low(self):
        while True:
            value = self.gpio.get_value(self.DRDY_PIN)
            if value == Value.INACTIVE:
                break
            time.sleep(1e-6)

    def reset(self):
        self.spi.writebytes([Ads.CMD_RESET])
        self.wait_for_data_ready_low()

    def read_chip_id(self):
        chip_id = self.read_register(Ads.REG_STATUS) >> 4
        return chip_id

    def read_value(self, channel):
        self.wait_for_data_ready_low()

        self.spi.writebytes([Ads.CMD_WREG | Ads.REG_MUX, 0x00, channel, Ads.CMD_SYNC])
        time.sleep(Ads.SYNC_TIMEOUT)

        self.spi.writebytes([Ads.CMD_WAKEUP])
        time.sleep(Ads.T_11_TIMEOUT)

        self.spi.writebytes([Ads.CMD_RDATA])
        time.sleep(Ads.DOUT_DELAY)

        response = self.spi.readbytes(3)
        return int.from_bytes(response, 'big', signed=True)

    def read_voltage(self, channel):
        value = self.read_value(channel)
        voltage = value * self.volts_per_digit
        return voltage


if __name__ == '__main__':
    from ads1256.ads1256_default_config import ads1256_default_config

    ads = ADS1256(ads1256_default_config)

    while True:
        value = ads.read_voltage(Ads.POS_AIN5 | Ads.NEG_AINCOM)
        print(value)
        time.sleep(0.01)
