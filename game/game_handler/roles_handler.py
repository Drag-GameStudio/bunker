import random
from lobby.models import Session, User
from game.models import UserInfo

PROFESSIONS = [
    "Врач общей практики", "Стоматолог", "Фельдшер", "Психолог", "Массажист",
    "Хирург-любитель", "Айтишник", "Системный администратор", "Программист",
    "Электрик", "Автомеханик", "Инженер-строитель", "Архитектор", "Метеоролог",
    "Учитель биологии", "Учитель физики", "Учитель труда", "Школьный сторож",
    "Повар", "Кондитер", "Бармен", "Пекарь", "Фермер", "Садовник", "Пчеловод",
    "Охотник", "Рыбак", "Выживальщик", "Спелеолог", "Спасатель", "Пожарный",
    "Военный", "Сапёр", "Полицейский", "Следователь", "Юрист", "Адвокат",
    "Детектив-любитель", "Химик", "Биолог", "Физик", "Геолог", "Археолог",
    "Медсестра", "Микробиолог", "Генетик", "Фармацевт", "Ботаник", "Эколог",
    "Техник по вентиляции", "Сантехник", "Уборщик", "Клинер", "Менеджер по продажам",
    "Оператор колл-центра", "Флорист", "Парикмахер", "Косметолог", "Тату-мастер",
    "Швея", "Кожевник", "Столяр", "Кузнец", "Гончар", "Ювелир", "Реставратор",
    "Писатель", "Поэт", "Художник", "Музыкант", "Актёр", "Блогер", "Фотограф",
    "Журналист", "Редактор", "Переводчик", "Преподаватель языков", "Историк",
    "Полиглот", "Картограф", "Программист-игродел", "Робототехник", "IT-рекрутер",
    "Руководитель проектов", "Логист", "Пилот-дронов", "Оператор видеонаблюдения",
    "Психотерапевт", "Экстрасенс", "Астролог", "Нутрициолог", "Диетолог",
    "Инструктор по йоге", "Тренер по выживанию", "Библиотекарь", "Архивариус",
    "Почтальон", "Писарь", "Плотник", "Навигатор", "Дизайнер интерфейсов",
    "3D-моделер", "Механик-робототехник", "Энтомолог", "Орнитолог", "Фальсификатор",
    "Хакер", "Фокусник", "Карикатурист", "Наставник", "Мотиватор", "Социальный работник",
    "Медиатор", "Дипломат", "Шаман", "Травник", "Фаерщик", "Выращиватель грибов",
    "Лоцман", "Топограф", "Дегустатор", "Пивовар", "Сборщик мусора", "Формовщик"
]
AGES = list(range(100))[10:]
ITEMS = [
    "Набор инструментов", "Генератор на бензине", "Канистра с бензином",
    "Аптечка", "Рация", "Палатка", "Спальный мешок", "Карта местности",
    "Компас", "Охотничий нож", "Котелок", "Гармошка", "Гитара", "Телескоп",
    "Микроскоп", "Набор семян", "Фонарик", "Запас батареек", "Свечи", "Спички",
    "Зажигалка", "Огниво", "Рюкзак", "Солнечная панель", "Аккумулятор",
    "Удочка", "Ружьё", "Патроны", "Рогатка", "Арбалет", "Стрела с верёвкой",
    "Верёвка", "Крюк", "Лопата", "Топор", "Пила", "Молоток", "Гвозди",
    "Кирка", "Очки ночного видения", "Маска", "Противогаз", "Фильтры для воды",
    "Фляга", "Термос", "Консервы", "Сухпай", "Поваренная книга", "Сковородка",
    "Ноутбук", "Жёсткий диск", "USB-флешка", "Карты Таро", "Маскарадный костюм",
    "Фотокамера", "Старый дневник", "Радиоприёмник", "Магнитофон", "Кассеты",
    "Пластинки", "Книга по медицине", "Книга по психологии", "Учебник по выживанию",
    "Альбом для рисования", "Краски", "Шахматы", "Карты игральные", "Настольная игра",
    "Кубик Рубика", "Дрон", "Набор для взлома замков", "Набор по химии",
    "Проводка", "Паяльник", "Набор для шитья", "Иглы и нитки", "Кусок ткани",
    "Старый флаг", "Медаль", "Игрушечный робот", "Кукла", "Бинокль", "Лупа",
    "Зелье (неизвестное)", "Амулет", "Стеклянная бутылка", "Глиняная чаша",
    "Пластиковые тарелки", "Мыло", "Зубная щётка", "Туалетная бумага",
    "Мешок картошки", "Мешок сахара", "Уголь", "Песочные часы", "Калькулятор",
    "Маленький сейф", "Ключ (от чего — неизвестно)", "Табличка 'Не входить'",
    "Блокнот с шифром", "Карта звёздного неба", "Флаг с символом", "Стетоскоп",
    "Скалка", "Зонтик", "Резиновый мяч", "Жевательная резинка", "Набор фейерверков",
    "Гаечный ключ", "Секундомер", "Брелок с компасом", "Ключ-карта", "Очки виртуальной реальности"
]
HOBBYS = [
    "Собирает пробки от бутылок", "Играет на ложках", "Смотрит на стены", 
    "Разговаривает с растениями", "Косплеит овощи", "Коллекционирует пакеты", 
    "Запоминает бесполезные факты", "Переводит песни с кошачьего", 
    "Бодается с козами", "Притворяется холодильником", "Собирает волосы из расчёсок", 
    "Развивает телепатию с холодильником", "Собирает камни с именами", 
    "Пишет фанфики про чайники", "Играет в шахматы сам с собой и проигрывает", 
    "Делает скульптуры из макарон", "Пугает голубей", "Коллекционирует пустые рулоны от туалетной бумаги",
    "Сочиняет гимны для бытовых предметов", "Ставит диагнозы незнакомцам по походке",
    "Плетёт одежду из пакетов", "Тренирует блох", "Ведёт дневник чужого сна", 
    "Ищет лицо Иисуса в котлетах", "Имитирует звуки микроволновки", "Делает фейковые документы для котов", 
    "Коллекционирует неловкие молчания", "Играет в прятки в одиночку", 
    "Ходит на свидания с деревьями", "Считает ананасы в магазинах", 
    "Пишет любовные письма кефирным бутылкам", "Смотрит обзоры на стены", 
    "Разгадывает кроссворды, не зная слов", "Угадывает цвет чужих носков", 
    "Оценивает вкус воздуха", "Пишет стендапы для тараканов", 
    "Вышивает портреты политиков на капусте", "Собирает тени от облаков", 
    "Сочиняет рэп о молоке", "Имитирует диалоги птиц", "Разводит жвачки", 
    "Реконструирует мифические рецепты", "Сканирует баркоды ради вдохновения", 
    "Игнорирует гравитацию", "Собирает коллекцию 'Да ну нафиг!'", 
    "Снимает ТикТоки с пылью", "Варит суп из воспоминаний", 
    "Охотится за невидимыми мухами", "Читает книги задом наперёд", 
    "Пишет стихи холодильнику", "Собирает запахи", "Имитирует звуки лифтов"
]
FACTS = [
    "Боится замкнутого пространства", "Имеет аллергию на пыль", 
    "Ходит во сне", "Знает 3 языка", "Прошёл курсы массажа", 
    "Никогда не пил алкоголь", "Был в армии", "Травмирован левый глаз", 
    "Не чувствует запахов", "Имеет фобию темноты", 
    "Может не есть 5 дней подряд", "Разбирается в грибах", 
    "Разводил пчёл", "Занимался скалолазанием", "Не умеет плавать", 
    "Имеет группу крови AB-", "Перенёс операцию на сердце", 
    "Прошёл курсы первой помощи", "Занимался йогой 5 лет", 
    "Разбирается в оружии", "Имеет водительские права", 
    "Плохо видит без очков", "Носит слуховой аппарат", 
    "Всё записывает в блокнот", "С детства занимается рисованием", 
    "Участвовал в спасательной операции", "Имеет судимость (погашена)", 
    "Никогда не болел простудой", "Может часами молчать", 
    "Разбирается в электронике", "Боится животных", "Был волонтёром в приюте", 
    "Прошёл курс экстремального выживания", "Разбирается в психологии", 
    "Интроверт", "Знает систему Морзе", "Имеет родинку в форме звезды", 
    "Хронически опаздывает", "Панически боится уколов", "Любит читать", 
    "Каждое утро делает зарядку", "В прошлом — сектант", 
    "Не чувствует боли (временно)", "Ненавидит громкие звуки", 
    "Имеет железный имплант", "Знает, как варить самогон", 
    "Когда-то жил в лесу", "Носит линзы", "Плохо переносит жару", 
    "Не доверяет технологиям", "Умеет шить", "Имеет опыт ухода за пожилыми", 
    "Может выучить стих за минуту", "Разбирается в законах", 
    "Плохо спит", "Знает основы боевых искусств", "Быстро учится", 
    "Считает, что мир — симуляция", "Имеет вшитый чип (не работает)", 
    "Был в медитационном ретрите 30 дней", "Боится быть один", 
    "Очень вынослив", "Знает, как строить печи", "Часто говорит сам с собой"
]
HEALTHS = [
    "Астма", "Аллергия на орехи", "Аллергия на пыльцу", "Лёгкая форма диабета", 
    "Глаукома", "Гастрит", "Мигрени", "Хронический насморк", 
    "Сколиоз", "Травма колена", "Нарушение слуха (частичное)", 
    "Нарушение зрения (сильная близорукость)", "Эпилепсия (редкие приступы)", 
    "Повышенное давление", "Пониженное давление", "Псориаз", 
    "Хроническая усталость", "Синдром раздражённого кишечника", 
    "Нарушение сна", "Храп", "Зубные импланты (старые)", 
    "Частые головные боли", "Тахикардия", "Плоскостопие", 
    "Фобия замкнутого пространства", "Панические атаки", 
    "Синдром дефицита внимания", "Аритмия", "Тремор рук", 
    "Травма позвоночника (лёгкая)", "Проблемы с суставами", 
    "Непереносимость лактозы", "Зрение только на один глаз", 
    "Частые судороги в ногах", "Ожирение 1-й степени", 
    "Недостаточный вес", "Склонность к депрессии", 
    "Сниженный иммунитет", "Нарушение координации", 
    "Старое незалеченное переломанное ребро", "Протез ноги", 
    "Ограниченная подвижность шеи", "Частые простуды", 
    "Нарушение речи (заикание)", "Тонзиллит", "Цистит", 
    "Хрупкие кости", "Ломкие ногти", "Редкие приступы агрессии", 
    "Невралгия", "Синдром хронической боли", 
    "Нарушение обмена веществ", "Проблемы с печенью", 
    "Слабое сердце (врождённый порок)", "Проблемы с ЖКТ", 
    "Аллергия на лекарства", "Сенсорная перегрузка", 
    "Синдром беспокойных ног", "Медленное заживление ран", 
    "Проблемы с памятью", "Потеря обоняния", "Хрупкие сосуды"
]


def get_random_el_from_array(arr: list) -> any:
    return arr[round((len(arr) - 1) * random.random())]

def generete_user_data():
    user_data = {}
    user_data["profession"] = get_random_el_from_array(PROFESSIONS)
    user_data["age"] = get_random_el_from_array(AGES)
    user_data["hobby"] = get_random_el_from_array(HOBBYS)
    user_data["item"] = get_random_el_from_array(ITEMS)
    user_data["fact"] = get_random_el_from_array(FACTS)
    user_data["health"] = get_random_el_from_array(HEALTHS)

    return user_data


def give_roles(session: Session):
    users_in_session: list[User] = User.objects.filter(session=session)
    for user in users_in_session:
        user_data = generete_user_data()
        user_info_model = UserInfo(user=user)
        user_info_model.profession = user_data["profession"]
        user_info_model.age = user_data["age"]
        user_info_model.hobby = user_data["hobby"]
        user_info_model.item = user_data["item"]
        user_info_model.fact = user_data["fact"]
        user_info_model.health = user_data["health"]

        user_info_model.save()



