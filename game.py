import json

class Player():
    """Класс игрока. Имеет имя и пол."""

    def __init__(self, id=None, name='', location=None, sex='ж'):
        self.id = id  # id игрока, понадобится для бота
        self.name = name  # Имя игрока
        self.location = location  # Текущая локация игрока
        self.num_locations = 0  # Количество локаций, посещённых игроком
        self.sex = sex  # Пол игрока
        self.ending = '' if 'м' in self.sex.lower() else 'а'  # Окончение глаголов для мужского и женского пола

    def set_sex(self, sex):
        self.sex = sex  # Пол игрока
        self.ending = '' if 'м' in self.sex.lower() else 'а'  # Окончение глаголов для мужского и женского пола

    def __str__(self):
        return f'Имя: {self.name}, id: {self.id}, sex: {self.sex}'

class Location():
    """Класс локации. Имеет название, описание и варианты действий."""

    def __init__(self, name, description, actions, photo_path=None):
        self.name = name
        self.description = description
        self.actions = actions
        self.photo_path = photo_path  # Добавляем атрибут для пути к фотографии

class Game():
    """Класс игры. Задаётся игрок и json-файл с локациями."""

    def __init__(self, player, json_file):
        self.player = player  # Объект класса Player
        self.process_input = lambda x: str(x).replace('{ending}', self.player.ending).replace('{name}', self.player.name)
        self.process_output = lambda x: str(x)
        self.locations = parse_json(json_file, self.process_input)  # Словарь вида {название_локации: объект_класса_Location}
        self.player.location = self.locations['начало']  # Начальная локация игрока
        self.output = lambda x: print(self.process_output(x))  # Функция вывода текста

    def get_actions(self):
        """Возвращает список действий в текущей локации."""
        actions = self.player.location.actions.keys()
        return list(actions)

    def output_actions(self):
        """Выводит варианты действий."""
        location = self.player.location
        markup = answers_with_choice(location.actions.keys())

        # Чтение пути к фотографии для текущей локации из файла locations.json
        with open('locations.json', 'r') as locations_file:
            locations_data = json.load(locations_file)
            photo_path = locations_data.get(location.name, {}).get("photo_path")

        # Выводим путь к фотографии в консоль для отладки
        print(f"Путь к фотографии для {location.name}: {photo_path}")

        # Проверяем наличие фотографии и отправляем ее
        if photo_path:
            photo_full_path = photo_path  # Используем путь к папке media/Фото
            print(f"Полный путь к фотографии: {photo_full_path}")

            send_message_with_photo(self.player.id, location.description, photo_full_path)
        else:
            bot.send_message(self.player.id, f"{self.process_output(location.description)}", reply_markup=markup)
    def take_an_action(self, choice):
        """Делает выбранное действие и обновляет аттрибуты игрока."""
        self.player.num_locations += 1

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(self.get_actions()):
                action = self.get_actions()[choice - 1]
            else:
                self.output("Некорректный выбор. Пожалуйста, выберите снова.")
                return
        else:
            action = choice

        self.player.location = self.locations[self.player.location.actions[action]]

        if self.player.location.name == 'начало':
            self.player.num_locations = 0

        elif self.player.location.name == 'кабинет223' and self.player.num_locations > 4:
            self.player.location = self.locations['lose-late']

def parse_json(filename, process_str=lambda x: x):
    file = open(filename, encoding='utf-8').read()
    file = process_str(file)
    file = json.loads(file)
    all_locations = {}
    for location_name in file['locations']:
        location = file['locations'][location_name]
        photo_path = location.get("photo_path")
        all_locations[location_name] = Location(location_name, location['description'], location['actions'], photo_path)
    return all_locations

if __name__ == '__main__':
    player = Player(name='Иван', sex='м')
    game = Game(player, 'locations.json')
    while game.player.location.name != "exit":
        game.output(game.player.location.description)
        game.output_actions()
        choice = input("Выберите действие: ")
        game.take_an_action(choice)
