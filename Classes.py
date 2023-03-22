

class My_Weather:
    def __init__(self, temperature, wind_speed, pressure, humidity, description):
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.pressure = pressure
        self.humidity = humidity
        self.description = description
    def __str__(self):
        return  f'Current Temperature: {self.temperature}\nWind Speed: {self.wind_speed}\n' \
                f'Current Pressure: {self.pressure}\nCurrent Humidity: {self.humidity}' \
                f'\nWeather Description: {self.description}'

    def temperature(self):
        return self.__temperature

    def wind_speed(self):
        return self.__wind_speed

    def pressure(self):
        return self.__pressure

    def humidity(self):
        return self.__humidity

    def description(self):
        return self.__description
