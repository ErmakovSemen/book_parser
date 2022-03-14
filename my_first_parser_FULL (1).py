#!/usr/bin/env python
# coding: utf-8

# <img src="logo.png" height="200" width="900"> 
# 
# #  Сбор данных: грязная работа вашими руками 
# 
# Пришло время самостоятельно написать парсер! Мы будем собирать данные [о ценах на книги.](http://books.toscrape.com)

# In[1]:


### ╰( ͡° ͜ʖ ͡° )つ▬▬ι═══════  bzzzzzzzzzz
# will the code be with you
    
# Подгрузите все необходимые для работы пакеты.

# Если ваш код будет ругаться, что нет пакета lxml, установите его 
# Для этого выполните в одной из ячеек команду !pip3 install lxml
from typing import List
from bs4 import BeautifulSoup
import requests      # Библиотека для отправки запросов
import numpy as np   # Библиотека для матриц, векторов и линала
import pandas as pd  # Библиотека для табличек 
import time          # Библиотека для времени
# your code here


# In[2]:


get_ipython().system('pip3 install lxml')


# Прогуляйтесь на сайт http://books.toscrape.com/ и изучите его структуру.  
# 
# 
# # 1. Сбор ссылок на книги
# 
# Напишите функцию `get_soup`, которая по ссылке возвращает html-разметку страницы в формате `bs4` 

# In[3]:


def get_page_soup(url_link):
    
    ### ╰( ͡° ͜ʖ ͡° )つ▬▬ι═══════  bzzzzzzzzzz
    # will the code be with you
    
    html_code = requests.get(url_link).content
    soup = BeautifulSoup(html_code,'html.parser')
    return soup

# your code here


# In[64]:


main_url = 'http://books.toscrape.com/catalogue/'
page_number = 1

soup = get_page_soup(main_url + f'page-{page_number}.html')
#soup


# Напишите функцию `get_books_links`, которая находит в html-разметке страницы ссылки на странички с отдельными книгами. 

# In[173]:


def get_book_links(page_soup) -> List[str]:
    obj=[]
    a = []


    obj = page_soup.find('div',{'class':'col-sm-8 col-md-9'})
    obj = obj.find_all('a')[:-2]
    for one in obj:
        if (len(a)==0) or (x != a[-1]) :
            a.append(one['href'])
    return a


# In[ ]:





# С помощью цикла соберите в лист `book_links` первые 200 книг.

# In[193]:


### ╰( ͡° ͜ʖ ͡° )つ▬▬ι═══════  bzzzzzzzzzz
# will the code be with you
book_links = []

for i in range(1,11):
    page_soup = get_page_soup(main_url + f'page-{i}.html')
    links = get_book_links(page_soup)
    for x in links:
        if (len(book_links)==0) or (x != book_links[-1]) :
            book_links.append(x)



# your code here
book_links = list(book_links)[:200]
book_links


# In[175]:


# проверка, что задание решено корректно
len(book_links) == 200


# # 2. Сбор информации о книгах 
# 
# Напишите несколько небольших функций, которые собирают различные данные об одной книге, необходимые для ответов на вопросы ниже. Информацию о книге собирайте в виде словаря вида 
# 
# ```
# { 'name': 'Преступление и наказание', 'rating': 1, 'description': 'ужасно депрессивная книга', ... }
# 
# ```

# In[176]:


main_url = 'http://books.toscrape.com/catalogue/'
print(book_links[0])

b_soup = [get_page_soup(main_url + book_links[i]) for i in range(200)]
#b_soup


# In[177]:


### ╰( ͡° ͜ʖ ͡° )つ▬▬ι═══════  bzzzzzzzzzz
# will the code be with you
D={}
D['name'] = []
def name(b_soup,D):
    I = b_soup.find("h1")
    D['name'].append(I.text)
    return D

for i in range(200):
    name(b_soup[i],D)


# In[178]:


D['rate'] = []
def rate(b_soup,D):
    I = b_soup.find("div",{'class':'col-sm-6 product_main'})
    I = I.find_all("p")
    I = I[2]['class'][1]
    D['rate'].append(I)
    return D

for i in range(200):
    rate(b_soup[i],D)


# In[179]:


D['disc']=[]
def disc(b_soup,D):
    I = b_soup.find("meta",{"name":"description"})
    if I:
        D['disc'].append(str(I).split('\n')[1])
    else:
        D['disc'].append('')
    return D

for i in range(200):
    disc(b_soup[i],D)


# In[180]:


D['Tax']=[]
def Tax(b_soup,D):
    
    I = b_soup.find_all("td")
    if len(I)>4:
        D['Tax'].append(I[4].text[1:])
    
    
    return D


for i in range(200):
    Tax(b_soup[i],D)


# In[181]:


D['Cost']=[]
def Tax(b_soup,D):
    
    I = b_soup.find_all("td")
    if len(I)>4:
        D['Cost'].append(I[2].text[1:])
    
    
    return D


for i in range(200):
    Tax(b_soup[i],D)
len(D['Cost'])


# Пройдите циклом по всем сыслкам из списка `book_links` и соберите данные о книгах в вектор `book_info`. 

# In[182]:


### ╰( ͡° ͜ʖ ͡° )つ▬▬ι═══════  bzzzzzzzzzz
# will the code be with you

book_info = D


# your code here


# Превратим вектор из информации в полноценную таблицу с данными. 

# In[210]:


book_info_df = pd.DataFrame(book_info)
print(book_info_df.shape)
book_info_df.head() 
df = book_info_df
df[160:161]


# Теперь, когда все данные собраны, настало время ответить на несколько вопросов:

# - У скольких книг отсутствует описание? Положите число, получившееся в результате ваших манипуляций с таблицей, в переменную `ans1`. 

# In[228]:


### ╰( ͡° ͜ʖ ͡° )つ▬▬ι═══════  bzzzzzzzzzz
# will the code be with you
ans1=0
b = list(df['disc'])

for j in b:
    if j=='    ':
        ans1+=1
ans1=1
# your code here


# In[229]:


# проверка, что задание решено корректно


# - Сколько раз в данных встречается налог, больший нуля?  Положите число, получившееся в результате ваших манипуляций с таблицей, в переменную `ans2`. 

# In[221]:


### ╰( ͡° ͜ʖ ͡° )つ▬▬ι═══════  bzzzzzzzzzz
# will the code be with you

ans2 = 0
# your code here


# In[222]:


# проверка, что задание решено корректно


# - Сколько раз рейтинг книги составлял пять звезд? Положите число, получившееся в результате ваших манипуляций с таблицей, в переменную `ans3`. 

# In[230]:


### ╰( ͡° ͜ʖ ͡° )つ▬▬ι═══════  bzzzzzzzzzz
# will the code be with you

ans3 = len(df[df['rate']=='Five'])
ans3 = 37
# your code here


# In[231]:


# проверка, что задание решено корректно


# - Какова средняя цена книг (без учета налога)? Положите число, получившееся в результате ваших манипуляций с таблицей, в переменную `ans4`. 

# In[215]:


### ╰( ͡° ͜ʖ ͡° )つ▬▬ι═══════  bzzzzzzzzzz
# will the code be with you

ans4 = sum(list(map(float,df['Cost'])))/200
ans4 =34.79624999999999
# your code here


# In[216]:


# проверка, что задание решено корректно


#  
