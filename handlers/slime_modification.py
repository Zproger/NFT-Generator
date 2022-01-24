import os
import time
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from handlers.storage import *
from handlers.rare_items import *


# Добавляем текст к изображению
def generate_text():
    overlay = Image.new("RGBA", (500, 150), color=(0, 0, 0, 80))
    dr1 = ImageDraw.Draw(overlay)
    fnt = ImageFont.truetype('data/fonts/Ubuntu-Bold.ttf', size=104)
    text = str(random.randint(100, 999)).encode("utf-8").hex()
    dr1.text(
        (14, 14),
        f"0x{text}",
        font=fnt,
        fill=(255, 255, 255, 160),
    )
    return overlay


# Изменить цвет слайма
def change_color(slime_image):
    # Извлекаем пиксели
    slime_pixels = slime_image.load()

    # Генерируем диапазон смещения байта RGBA
    r_byte = random.randint(0, 70)
    g_byte = random.randint(0, 70)
    b_byte = random.randint(0, 70)

    # Редактируем пиксели слайма
    for w in range(WIDTH):
        for h in range(HEIGHT):
            # Получаем текущий пиксель и кортеж RGBA
            pixel = slime_pixels[w, h]

            if pixel != (0, 0, 0, 0):
                # Меняем цвет на рандомный диапазон
                # Красим только объект слайма
                slime_pixels[w, h] = (
                    pixel[0] + r_byte,
                    pixel[1] + g_byte,
                    pixel[2] + b_byte,
                    255
                )


def create_image(image_name):
    # Задний фон изображения
    background = random.choice(RGB_BASE)

    # Создаем объект изображения в памяти
    img = Image.new("RGB", (WIDTH, HEIGHT), background)
    original_slime = Image.open("data/original.png").convert("RGBA")

    # Генерируем текст и редактируем слайма
    overlay = generate_text()
    change_color(original_slime)

    # Добавляем слайма
    img.paste(original_slime, (0, 0), original_slime)

    # Добавляем усы
    mustache = add_mustache()
    if mustache is not None:
        change_color(mustache[0])
        img.paste(mustache[0], (0, 0), mustache[0])
    else:
        mustache = 100

    # Добавляем шляпу
    hat = add_hat()
    if hat is not None:
        change_color(hat[0])
        img.paste(hat[0], (0, 0), hat[0])
    else:
        hat = 100

    # Добавляем предмет
    subject = add_subjects()
    if subject is not None:
        change_color(subject[0])
        img.paste(subject[0], (0, 0), subject[0])
    else:
        subject = 100

    # Добавляем текст с HEX значением
    img.paste(overlay, (100, 100), overlay)

    # Сохраняем результат в отдельную папку
    if not os.path.exists(f"result/{image_name}"):
        os.mkdir(f"result/{image_name}")
    img.save(f"result/{image_name}/{image_name}.png")

    # Добавляем характеристики каждого слайма
    with open(f"result/{image_name}/specifications.txt", "w") as file:
        # Вероятность получить такого же персонажа в %
        mustache_percent = mustache[1] if isinstance(mustache, list) else mustache
        hat_percent = hat[1] if isinstance(hat, list) else hat
        subject_percent = subject[1] if isinstance(subject, list) else subject
        character_rarity = ((mustache_percent * 0.01) * (hat_percent * 0.01) * (subject_percent * 0.01)) * 100

        data = "Редкость предметов (шанс получить предмет в %)\n\n"\
        f"Усы: {mustache_percent}%\n"\
        f"Шляпа: {hat_percent}%\n"\
        f"Оружие: {subject_percent}%\n\n"\
        "Вероятность получить такого же персонажа в %\n"\
        f"-> {character_rarity}%"
        file.write(data)

    # Сохраняем результат в общую папку
    if not os.path.exists("result/all_slimes"):
        os.mkdir("result/all_slimes")
    img.save(f"result/all_slimes/{image_name}({str(character_rarity).replace('.', ',')}).png")

