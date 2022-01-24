import os
import random
from PIL import Image


# Получить рандомный предмет после определения уникальности
def get_item(folder_name, percent):
    item_list = os.listdir(f"data/items/{folder_name}/{percent}")
    if len(item_list) > 0:
        return [percent, random.choice(item_list)]


# Получить процент редкости предмета
# Используемая редкость предметов (5%, 10%, 20%, 50%, 80%)
def percent_checker(folder_name):
    rare_percent = random.randint(1, 100)
    if rare_percent <= 5:
        return get_item(folder_name, 5)
    elif rare_percent <= 10:
        return get_item(folder_name, 10)
    elif rare_percent <= 20:
        return get_item(folder_name, 20)
    elif rare_percent <= 50:
        return get_item(folder_name, 50)
    elif rare_percent <= 80:
        return get_item(folder_name, 80)
    else:
        return None


# В случае успеха, возвращает объект с изображением усов
# Также в 2м аргументе % редкости предмета
def add_mustache():
    item = percent_checker("mustache")
    # Дополнительно делаем уникальность 40%
    if random.randint(0, 100) > 60 and item is not None:
        return [Image.open(f"data/items/mustache/{item[0]}/{item[1]}").convert("RGBA"), item[0]]


# В случае успеха, возвращает объект с изображением предмета
# Также в 2м аргументе % редкости предмета
def add_subjects():
    item = percent_checker("subjects")
    # Дополнительно делаем уникальность 40%
    if random.randint(0, 100) > 60 and item is not None:
        return [Image.open(f"data/items/subjects/{item[0]}/{item[1]}").convert("RGBA"), item[0]]


# В случае успеха, возвращает объект с изображением шляпы
# Также в 2м аргументе % редкости предмета
def add_hat():
    item = percent_checker("hats")
    # Дополнительно делаем уникальность 40%
    if random.randint(0, 100) > 60 and item is not None:
        return [Image.open(f"data/items/hats/{item[0]}/{item[1]}").convert("RGBA"), item[0]]