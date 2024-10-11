import time

from ads1256.ads1256 import ADS1256
from ads1256.constants import ADS1256Constants as ADSC  # noqa: N817

if __name__ == '__main__':
    ads = ADS1256()
    ads.set_input(ADSC.POS_AIN0, ADSC.NEG_AINCOM)
    ads.set_gain(1)

    while True:
        value = ads.read_value()
        voltage = value * ads.volt_per_digit()

        # You can also directly read the voltage.
        # voltage = ads.read_voltage()

        print(f'{value}\t\t{voltage:.5f} V')

        time.sleep(0.01)
