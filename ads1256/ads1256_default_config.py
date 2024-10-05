ads1256_default_config = {
    ############################# SPI configuration ############################
    'spi_bus': 0,
    'spi_device': 0,
    # The ADS1256 supports a minimum of 1/10th of the output sample data rate
    # in Hz to 1/4th of the oscillator CLKIN_FREQUENCY. With the recommended
    # oscillator freuency of 7.68 MHz this results in a maximum SPI frequency
    # of 1.92 MHz. Since the Raspberry pi only supports power-of-two fractions
    # of the 250MHz system clock, the closest value would be 1953125 Hz, which
    # is slightly out of spec for the ADS1256.
    # Choosing 250MHz/256 = 976563 Hz is a safe choice.
    'spi_frequency': 976563,
    ############################ GPIO configuration ############################
    'data_ready_pin': 22,
    'power_down_input': 27,
    ################################## Timings #################################
}
