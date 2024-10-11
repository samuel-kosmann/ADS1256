import time

from ads1256.ads1256 import ADS1256
from ads1256.constants import ADS1256Constants as ADSC  # noqa: N817

if __name__ == '__main__':
    ads = ADS1256()
    ads.self_calibration()

    channel = [
        ADSC.POS_AIN0,
        ADSC.POS_AIN1,
        ADSC.POS_AIN2,
        ADSC.POS_AIN3,
        ADSC.POS_AIN4,
        ADSC.POS_AIN5,
        ADSC.POS_AIN6,
        ADSC.POS_AIN7,
    ]

    while True:
        for i in range(len(channel)):
            ads.set_input(channel[i], ADSC.NEG_AINCOM)

            # After changing input channel a sync is required.
            ads.sync()

            value = ads.read_value()
            voltage = value * ads.volt_per_digit()

            print(f'{i}\t{value}\t\t{voltage:.5f} V')

        print('---------------------------------')
        print('Channel\tRaw Value\tVoltage')

        time.sleep(0.1)
