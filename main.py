from logging import exception

import requests
import webbrowser

class Nasa_app:


    def __init__(self):
        self.api_root = "https://images-api.nasa.gov"
        self.search_endpoint = self.api_root + "/search"


    def get_image_by_name(self, name, year_start, year_end):
        params = {
            'q' : name,
            'media_type' : 'image',
            'year_start' : year_start,
            'year_end' : year_end
        }
        try:
            response = requests.get(self.search_endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            return data

        except requests.exceptions.HTTPError as http_err:
            return f"Упс! Ошибка {http_err}"

        except Exception as err:
            return err


    def run(self):
        print("=" * 50)
        print("ДОБРО ПОЖАЛОВАТЬ В ПРИЛОЖЕНИЕ!")
        print("=" * 50)
        print("powered by NASA Image and Video library API")
        print()

        while True:
            print("\n" + "-" * 30)
            print("Введите название объекта который вы бы хотели найти или 'exit' если хотите выйти ")
            print("(пример ввода: mars rover, hubble telescope, black hole, earth from space")

            name = input()

            if name == 'exit':
                print("До свидания! Спасибо за использование приложения!")
                break

            print("Введите год начиная с которого вы бы хотели найти изображение (например 1990)")

            year_start = input()

            print("Введите год заканчивая которым вы бы хотели найти изображение (например 2000)")

            year_end = input()

            print("Подождите, уже ищем изображение!")

            results = self.get_image_by_name(name, year_start, year_end)

            print("Успешно! Поиск завершен!")
            print(f"Найдено элементов: {len(results.get('collection', {}).get('items', []))}")

            items = results.get('collection', {}).get('items', [])

            first_image_url = None
            first_image_title = None

            for i, item in enumerate(items[:5]):
                data = item.get('data', [{}])[0]
                links = item.get('links', [])

                for link in links:
                    if link.get('rel') in ['preview', 'orig']:
                        first_image_url = link.get('href')
                        first_image_title = data.get('title', 'Без названия')
                        break

                if first_image_url:
                    break

            for i, item in enumerate(items[:3]):
                print(f"\n{'=' * 50}")
                print(f"РЕЗУЛЬТАТ {i + 1}")
                print(f"{'=' * 50}")

                data = item.get('data', [{}])[0]
                links = item.get('links', [])

                title = data.get('title', 'Без названия')
                description = data.get('description', 'Нет описания')
                date_created = data.get('date_created', 'Дата неизвестна')
                nasa_id = data.get('nasa_id', 'Без ID')

                print(f"🏷️  Название: {title}")
                print(f"📅 Дата создания: {date_created}")
                print(f"🆔 NASA ID: {nasa_id}")
                print(f"📝 Описание: {description[:200]}...")

                image_found = False
                for link in links:
                    if link.get('rel') in ['preview', 'orig']:
                        if not image_found:
                            print(f"Изображение: {link.get('href')}")
                            image_found = True

                if not image_found:
                    print("Ссылки на изображения не найдены")

            if first_image_url:
                try:
                    webbrowser.open(first_image_url)
                    print(f"🌐 Открываю изображение в браузере...")
                except Exception as e:
                    print(f"Не удалось открыть в браузере: {e}")
            else:
                print("\nНе найдено ни одного изображения для открытия")


if __name__ == "__main__":

    app = Nasa_app()
    app.run()
