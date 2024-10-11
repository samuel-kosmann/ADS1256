import time

from ads1256.ads1256 import ADS1256
from ads1256.constants import ADS1256Constants as ADSC  # noqa: N817

if __name__ == '__main__':
    ads = ADS1256()
    ads.set_input(ADSC.POS_AIN0, ADSC.NEG_AINCOM)

    gain = 1

    while True:
        ads.set_gain(gain)
        ads.self_calibration()
        ads.wait_for_data_ready_low()

        value = ads.read_value()
        voltage = value * ads.volt_per_digit()

        print(f'{gain}\t', end='')
        print(f'{value}\t\t{voltage:.5f} V')

        prev_value = value

        gain *= 2
        if gain == 128:
            gain = 1
            time.sleep(0.1)

            print('---------------------------------')
            print('Gain\tRaw Value\tVoltage')
