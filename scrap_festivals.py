# import requests
# from bs4 import BeautifulSoup
# import lxml
# from proxy import proxyes
# import json
#
# # сосздадим словарь заголовок
# header = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
# }
#
# fest_urls_list = []
# # Нам нужно будет генерировать ссылки и отправлять запросы через цикл for от 0 до 144
# for i in range(0, 144, 24):
# # for i in range(0, 24, 24):
#     url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=2%20Aug%202023&to_date=&maxprice=500&o={i}&bannertitle=August'
#
#     req = requests.get(url=url, headers=header)  # в ответ нам прилетит словарь
#     json_data = json.loads(req.text)
#     html_response = json_data['html']
#     with open(f'data/index_{i}.html', 'w') as file:
#         file.write(html_response)
#
#
#     with open(f'data/index_{i}.html') as file:
#         src = file.read()
#
#     soup = BeautifulSoup(src, 'lxml')
#     cards = soup.find_all('a', class_='card-details-link')
#     # теперь создадим список под наши ссылки fest_urls_list
#     for item in cards:
#         fest_url = 'https://www.skiddle.com' + item.get('href')
#         fest_urls_list.append(fest_url)
#
# #print(fest_urls_list)
# # Пол дела сделано, после того ка мы собрали все ссылки нам надо написать код для перехода
# # по каждой этой ссылке для сбора информации
# count = 0
# result_festival_info = []
# for url_item in fest_urls_list:
#     count += 1
#     print(count)
#     # отправляем запрос
#     req = requests.get(url=url_item, headers=header)
#     # создадим блок try/except
#     try:
#         soup = BeautifulSoup(req.text, 'lxml')
#         fest_info_block = soup.find('div', class_='MuiPaper-root')
#         fest_name = soup.find('div', class_='MuiBox-root').find('h1')
#
#
#     # осталось лишь собрать данные
#         items_info_location = [item.text.strip() for item in fest_info_block]
#         items_info_names = [item.text.strip() for item in fest_name]
#         result_festival_info.append(' '.join(items_info_names + items_info_location))
#         # print(result_festival_info)
#
#
#     except Exception as ex:
#         print(ex)
#         print('Damn...There was some error')
#
# with open('fest_list_info.json', 'a', encoding='utf-8') as file:
#     json.dump(result_festival_info, file, indent=4, ensure_ascii=False)