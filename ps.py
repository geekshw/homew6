# from bs4 import BeautifulSoup
# import requests
# import time

# count_news = 0

# # Открываем файл для записи
# with open('news_headlines.txt', 'w', encoding='utf-8') as file:
#     for page in range(1, 11):  # Assuming 10 pages of news
#         url = f'https://24.kg/page_{page}'
#         response = requests.get(url)
        
#         if response.status_code == 200:  # Check if request was successful
#             soup = BeautifulSoup(response.text, 'lxml')
#             all_news = soup.find_all('div', class_='title')
            
#             for news in all_news:
#                 count_news += 1
#                 file.write(f'{count_news}. {news.text.strip()}\n')  # Write news headline to file, strip extra whitespace
#         else:
#             file.write(f'Failed to retrieve page {page}. Status code: {response.status_code}\n')
        
#         time.sleep(1)  # Optional: Add a delay to be polite to the server

# # Закрываем файл после завершения записи
# print(f'Total news articles scraped: {count_news}')
