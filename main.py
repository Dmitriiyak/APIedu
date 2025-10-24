import requests
import os
from dotenv import load_dotenv

load_dotenv()

class Weather_App:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

        if not self.api_key:
            print("ОШИБКА: API ключ не найден!")
            print("Убедитесь, что файл .env существует и содержит OPENWEATHER_API_KEY")
            exit(1)
    def get_weather(self, city_name):
        params = {
            'q': city_name,  # город
            'appid': self.api_key,  # API ключ
            'units': 'metric',  # единицы измерения (метрические = Цельсий)
            'lang': 'ru'  # язык ответа (русский)
        }
        try:
            print(f"Отправляем запрос для города: {city_name}")
            response = requests.get(self.base_url, params=params)

            response.raise_for_status()

            weather_data = response.json()

            # Форматируем и возвращаем данные
            return self._format_weather_data(weather_data)

        except requests.exceptions.HTTPError as http_err:
            # Обрабатываем HTTP ошибки (404, 401 и т.д.)
            error_message = f"HTTP ошибка: {http_err}"
            if response.status_code == 401:
                return "❌ Ошибка авторизации. Проверьте API ключ."
            elif response.status_code == 404:
                return f"❌ Город '{city_name}' не найден."
            else:
                return f"❌ Ошибка: {error_message}"

        except Exception as err:
            # Обрабатываем все остальные ошибки
            return f"❌ Произошла непредвиденная ошибка: {err}"

    def _format_weather_data(self, data):
        city = data['name']
        country = data['sys']['country']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        description = data['weather'][0]['description']
        wind_speed = data['wind']['speed']

        formatted_weather = f"""
        🌍 ПОГОДА В {city.upper()}, {country}:
        Температура: {temperature}°C 
        (ощущается как {feels_like}°C)
        💧 Влажность: {humidity}%
        📊 Давление: {pressure} гПа
        🌬️  Скорость ветра: {wind_speed} м/с
        📝 Описание: {description.capitalize()}
        """

        return formatted_weather

    def run(self):
        print("=" * 50)
        print("🌤️  ДОБРО ПОЖАЛОВАТЬ В ПРИЛОЖЕНИЕ ПОГОДЫ!")
        print("=" * 50)
        print("Это приложение использует реальные данные с OpenWeatherMap API")
        print()


        while True:
            print("\n" + "-" * 30)
            city = input("Введите название города (или 'выход' для завершения): ").strip()

            if city.lower() in ['выход', 'exit', 'quit', 'q']:
                print("👋 До свидания! Спасибо за использование приложения!")
                break

            if not city:
                print("⚠️  Пожалуйста, введите название города")
                continue

            print(f"\n🔍 Ищем погоду для: {city}")
            result = self.get_weather(city)
            print(result)

if __name__ == "__main__":

    app = Weather_App()
    app.run()