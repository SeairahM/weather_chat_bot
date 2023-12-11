class ConvertTemperature:

    def convert_kelvin_to_celsius(self, kelvin):
        celsius = kelvin - 273.15
        return round(celsius, 2)