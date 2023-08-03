import bs4
import requests
from bs4 import BeautifulSoup
import xlsxwriter

main_url = 'https://trade59.ru/'

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}
data = [['Наименование', 'Цена', 'Ссылка', 'Картинка']]


def get_soup(url):
    res = requests.get(url=url, headers=header)
    return bs4.BeautifulSoup(res.text, 'html.parser')


# Передадим в нашу функцию главный url + id каталога с которого мы будем парсить
categories_page = get_soup(main_url + 'catalog.html?cid=7')
# Таким образом мы получим страницу на которой можем искать какие-то элементы
catigories = categories_page.findAll('a', class_='cat_item_color')
# Теперь нам просто необходимо перебрать циклом и вызвать функцию get_soup()-куда мы передаём
# главный url + достаём из нашего тега 'a' ссылку на категорию которую мы перебираем
for item in catigories:
    subcategories_page = get_soup(main_url + item['href'])
    # для подкатегории(тоесть - для второй страницы)мы будем делать всё тоже-самое
    subcategories = subcategories_page.findAll('a', class_='cat_item_color')
    for subcat in subcategories:
        iphone_page = get_soup(main_url + subcat['href'])
        # перейда на страницу айфонов той категории которой нам нужно, мы увидим, что они
        # находятся в теле тегов 'div'
        iphones_14_128 = iphone_page.findAll('div', class_='items-list')
        # И снова переберём список полученных телефонов
        for iphone in iphones_14_128:
            iphones_14_128_href = iphone.find('a').get('href').strip()
            title = iphone.find('a')['title'].strip()
            # так как в блоке 'div', class_='price' есть ещё какой-то текст, мы будем
            # искать первый попавшийся через find(text=True)
            price = iphone.find('div', class_='price').find(text=True).strip()
            # Находим фото с телефоном и обращаемся к его атрибуту style, достаём от туда
            # необходимый нам url и меняем папку tn на sourse, при этом отрезая всё лишнее
            # ('url(', ')'))
            img = iphone.find('div', class_='image')['style'].split('url(')[1].split(')')[
                0].replace('/tn/', '/source/')
            # Отлично теперь нам осталось это всё сохранить в виде XL-таблицы
            # Для этого создаём список data в который передаём список с названиями сталбцов
            data.append([title, price, main_url + iphones_14_128_href, main_url + img])

# Теперь открываем файл на запись и создаём новую страницу на которой мы перебираем
# каждый элемент из нашего списка data и сохраняем с номером строки и информацией о нём.
with xlsxwriter.Workbook('Iphones.xlsx') as file:
    worksheet = file.add_worksheet()

    for row_num, info in enumerate(data):
        worksheet.write_row(row_num, 0, info)