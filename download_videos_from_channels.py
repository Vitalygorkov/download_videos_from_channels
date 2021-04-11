import sqlite3
from selenium import webdriver
import time
import random
import unicodedata
import re
from pytube import YouTube



#МОдуль для получения ссылок на видео
def save_link_in_db_from_channel(chan_for_download, number_of_scrolling):
    # создание пустой базы данных
    # number_of_scrolling = 10
    # print(number_of_scrolling)
    chan_for_download_list = [chan_for_download,]

    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome('chromedriver.exe', options=options)

    conn = sqlite3.connect('bazasearch_download.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS vidos(
       vidid INT,
       name TEXT,
       descr TEXT,
       prosm INT,
       pub TEXT,
       link TEXT PRIMARY KEY);
    """)
    conn.commit()

    # links = ['https://www.youtube.com/c/NickChernobaev/videos',]

    # функция сохранени ссылок в базу данных
    def get_links(link_list, number_of_scrolling):
        for link in link_list:
            driver.get(link)
            time.sleep(1)
            len_scroll = 3000
            for i in range(1, number_of_scrolling):
                driver.execute_script("window.scrollBy(0,{})".format(len_scroll))
                len_scroll += 6000
                time.sleep(1)
                print('прокрутка')
            for i in driver.find_elements_by_id('video-title'):
                vid_link = str(i.get_attribute('href'))
                vid_description = str(i.get_attribute('aria-label'))
                print(vid_link + '   ' + vid_description)
                try:
                    author_date = str(vid_description.split('Автор:', 1)[1]).split(' ', 1)[1].rstrip()
                except:
                    author_date = "author_date ошибка "
                    print("author_date ошибка" + str(vid_link))
                stro = unicodedata.normalize('NFKD', author_date)
                prosm_text = str(re.findall(r"\w{0}\s{0}\d+\s*\d*\s*\d* просм", stro))
                prosm_int = re.findall(r'\d+', prosm_text)
                try:
                    prosm_int = int(''.join(prosm_int))
                except:
                    prosm_int = 0
                    print('prosm_int исключение' + str(vid_link))

                vids = ('1', author_date, vid_description, prosm_int, '0', vid_link)
                print(vids)
                try:
                    cur.execute("INSERT INTO vidos VALUES(?, ?, ?, ?, ?, ?);", vids)
                    conn.commit()
                except sqlite3.IntegrityError as err:
                    print(str(err) + 'в ссылке: ' + link)
        driver.close()

    # запускаем функцию сохраняем ссылки в базу данных
    get_links(chan_for_download_list, number_of_scrolling)


def download_videos_from_db(nums):
    # Скачивание по ссылкамм из базы, нужно сделать в виде функции и очистка базы в конце.

    conn = sqlite3.connect('bazasearch_download.db')
    cur = conn.cursor()
    cur.execute("""SELECT link FROM vidos""")
    print(cur.execute("""SELECT link FROM vidos ORDER BY pub"""))
    # vid_links = cur.fetchall()
    vid_links = cur.fetchmany(nums)
    # print(vid_links)
    # for i in vid_links:
    #     print(i)

    # return 'просто текст результат функциии channel_download_module'
    for i in vid_links:
        yt = YouTube(i[0])
        yt.streams.get_by_itag(18).download()
        print(i[0])
    # нужно добавить очистку базы данных
    return 'просто текст результат функциии channel_download_module'

# скачивание видео по отдельным ссылкам.
def download_from_links(vid_links):
    vid_links = ['https://www.youtube.com/watch?v=oPr7555NIevI']
    for i in vid_links:
        yt = YouTube(i)
        yt.streams.get_by_itag(18).download()
        print(i)

# save_link_in_db_from_channel('https://www.youtube.com/c/DjangoSchool/videos', 3)

# download_videos_from_db(15)