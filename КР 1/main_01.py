import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# pd.set_option('display.max_columns', None) # Убираю ограничение на количество столбцов

# Задание:

# Удалить строки, где ни в одном столбце нет данных. Самую первую строку, где хранятся данные "Response" вперемешку с другими - удалить. 
# Столбцы нумеруются с 0. Все столбцы нужно перевести на русский и назвать в зависимости от описания задания. Столбцы с 3-8 показывают, 
# смотрел ли человек фильм. Если данные есть в столбце 3, то он смотрел 1 часть, в 4 столбце 2 часть и т.д. 
# Заменить текст на False/True. 
# Столбцы 9-14 В названии указать каждую часть по очереди, 9 столбец 1 часть Star Wars, 10 столбец 2 часть и т.д. 
# Данные в столбцах указывают какой рейтинг фильму выставили зрители, от лучшего (1) к худшему (6). 
# Столбцы 15-28 показывают имена героев и отношение к ним. 
# Столбец "Household Income" разбить на два столбца с левой границей и правой границей суммы. 
# Если границы нет, то ставится 999999 или -999999, заменяя +inf и -inf. 
# После чего получить список людей, где мужчины поставили 4-6 часть на 1-2 место, а 1-3 часть на 5-6. 
# Посчитать сколько мужчин из списка ранее фанаты стар трека, а сколько нет. Найти топ-10 женщин, 
# которые являются фанатами стар трека и поставили одну из 4-6 частей на 1 место. Вывести общее количество людей которым больше всего 
# нравится 1 фильм, 2 фильм и т.д. (стоит 1 место). Сгруппировать людей по полу и вывести график зависимости пола от оценки каждой части 
# (сколько мужчин и женщин оценили 1 часть максимально и т.д.). Также необходимо взять среднее значение оценки каждого фильма 
# по диапазону возраста и вывести на графике зависимость возраста от средней оценки каждого фильма.

# Загрузка датасета:

data = pd.read_excel('info.xlsx')

print()
print("Входные данные: ")
print(data)

data = data.drop(data.index[0]) # Удаляю первую строку

data[['Gender']] = data[['Gender']].fillna("Male")
data = data.fillna(0)

# Удаляю все строки, где ни в одном столбце нет данных 
#data = data.dropna(how='all') 

data.replace("", np.nan, inplace=True) # Заменяю пробелы, и пустые строки, на NaN значения, для корректного их удаления
data.replace(" ", np.nan, inplace=True)

data = data.dropna(how='all', subset=data.columns[2:]) # Удаляю все строки, где нет данных везде, кроме первых 2х столбцов

for col in data.columns[2:8]: # Для всех столбцов с 3 по 8
    data[col] = data[col].notna() # Проверить, есть ли в ячейке значения. Заменить значения в ячейке на True/False, в зависимости от их наличия

# Переименовываю все столбцы
column_translations = {
    "RespondentID": "ID респондента",
    "Have you seen any of the 6 films in the Star Wars franchise?": "Вы видели хотя бы один из 6 фильмов франшизы Звездные войны?",
    "Do you consider yourself to be a fan of the Star Wars film franchise?": "Считаете ли вы себя фанатом кинофраншизы Звездные войны?",
    "Which of the following Star Wars films have you seen? Please select all that apply.": "Какие из следующих фильмов Звездные войны вы видели? Пожалуйста, выберите все подходящие варианты. Star Wars: Episode I The Phantom Menace",
    "Unnamed: 4": "Star Wars: Episode II  Attack of the Clones",
    "Unnamed: 5": "Star Wars: Episode III  Revenge of the Sith",
    "Unnamed: 6": "Star Wars: Episode IV  A New Hope",
    "Unnamed: 7": "Star Wars: Episode V The Empire Strikes Back",
    "Unnamed: 8": "Star Wars: Episode VI Return of the Jedi",
    "Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.": "Пожалуйста, расставьте фильмы Звездные войны в порядке предпочтения, где 1 - ваш любимый фильм во франшизе, а 6 - наименее любимый. Star Wars: Часть 1",
    "Unnamed: 10": "Star Wars: Часть 2",
    "Unnamed: 11": "Star Wars: Часть 3",
    "Unnamed: 12": "Star Wars: Часть 4",
    "Unnamed: 13": "Star Wars: Часть 5",
    "Unnamed: 14": "Star Wars: Часть 6",
    "Please state whether you view the following characters favorably, unfavorably, or are unfamiliar with him/her.": "Пожалуйста, укажите, относитесь ли вы благосклонно к следующим персонажам, неблагосклонно или не знакомы с ним/ней. Han Solo",
    "Unnamed: 16": "Luke Skywalker",
    "Unnamed: 17": "Princess Leia Organa",
    "Unnamed: 18": "Anakin Skywalker",
    "Unnamed: 19": "Obi Wan Kenobi",
    "Unnamed: 20": "Emperor Palpatine",
    "Unnamed: 21": "Darth Vader",
    "Unnamed: 22": "Lando Calrissian",
    "Unnamed: 23": "Boba Fett",
    "Unnamed: 24": "C-3P0",
    "Unnamed: 25": "R2 D2",
    "Unnamed: 26": "Jar Jar Binks",
    "Unnamed: 27": "Padme Amidala",
    "Unnamed: 28": "Yoda",
    "Which character shot first?": "Какой персонаж выстрелил первым?",
    "Are you familiar with the Expanded Universe?": "Вы знакомы с Расширенной вселенной?",
    "Do you consider yourself to be a fan of the Expanded Universe?Œæ": "Считаете ли вы себя фанатом Расширенной вселенной?",
    "Do you consider yourself to be a fan of the Star Trek franchise?": "Считаете ли вы себя фанатом франшизы Звездный путь?",
    "Gender": "Пол",
    "Age": "Возраст",
    "Household Income": "Доход домохозяйства",
    "Education": "Образование",
    "Location (Census Region)": "Местоположение (регион переписи)"
}

data.rename(columns=column_translations, inplace=True)




# Разбиваем столбец 'Доход домохозяйства' на два столбца
data[['Левая граница', 'Правая граница']] = data['Доход домохозяйства'].str.split('-', expand=True)

# Удаляем символы доллара и запятые
data['Левая граница'] = data['Левая граница'].str.replace('$', '').str.replace(',', '')
data['Правая граница'] = data['Правая граница'].str.replace('$', '').str.replace(',', '')

# Преобразуем строки в числа
data['Левая граница'] = pd.to_numeric(data['Левая граница'], errors='coerce')
data['Правая граница'] = pd.to_numeric(data['Правая граница'], errors='coerce')

# Заменяем все значения, которые не вписываются в диапазон от -999999 до 999999, на -∞ и ∞ соответственно
data['Левая граница'] = data['Левая граница'].where(data['Левая граница'] > -999999, -np.inf)
data['Правая граница'] = data['Правая граница'].where(data['Правая граница'] < 999999, np.inf)

# Заменяем все значения NaN на 0
data = data.fillna(0)



# Длинная строка "Star Wars: Часть 1"
str1 = "Пожалуйста, расставьте фильмы Звездные войны в порядке предпочтения, где 1 - ваш любимый фильм во франшизе, а 6 - наименее любимый. Star Wars: Часть 1"

# Преобразую строковые значения цифр, в числовые
data[str1] = data[str1].astype(float)
data['Star Wars: Часть 2'] = data['Star Wars: Часть 2'].astype(float)
data['Star Wars: Часть 3'] = data['Star Wars: Часть 3'].astype(float)
data['Star Wars: Часть 4'] = data['Star Wars: Часть 4'].astype(float)
data['Star Wars: Часть 5'] = data['Star Wars: Часть 5'].astype(float)
data['Star Wars: Часть 6'] = data['Star Wars: Часть 6'].astype(float)

# Список мужчин, которые поставили 4-6 часть на 1-2 место, а 1-3 часть на 5-6
men_pref = data[
    (data['Пол'] == 'Male') & 
        (   (data['Star Wars: Часть 4'].isin([1, 6])) | 
            (data['Star Wars: Часть 5'].isin([1, 2])) | 
            (data['Star Wars: Часть 6'].isin([1, 2])) |
            (data[str1].isin([5, 6]))                 |
            (data['Star Wars: Часть 2'].isin([5, 6])) |
            (data['Star Wars: Часть 3'].isin([5, 6])))
        ]

print()
print("Список мужчин, которые поставили 4-6 часть на 1-2 место, а 1-3 часть на 5-6")
print(men_pref)

# Сколько мужчин из списка ранее фанаты стар трека, а сколько нет
star_trek_fans = men_pref['Считаете ли вы себя фанатом франшизы Звездный путь?'].value_counts()

print()
print("Сколько мужчин из списка ранее фанаты стар трека, а сколько нет")
print(star_trek_fans)

# Топ-10 женщин, которые являются фанатами стар трека и поставили одну из 4-6 частей на 1 место
women_pref = data[(data['Пол'] == 'Female') & 
                  (data['Считаете ли вы себя фанатом франшизы Звездный путь?'] == 'Yes') & 
                  ((data['Star Wars: Часть 4'] == 1) | 
                   (data['Star Wars: Часть 5'] == 1) | 
                   (data['Star Wars: Часть 6'] == 1))]
top_10_women = women_pref.head(10)

print()
print("Топ-10 женщин, которые являются фанатами стар трека и поставили одну из 4-6 частей на 1 место")
print(top_10_women)

# Общее количество людей которым больше всего нравится 1 фильм, 2 фильм и т.д. (стоит 1 место)
fav_films = data[[str1, 'Star Wars: Часть 2', 'Star Wars: Часть 3', 'Star Wars: Часть 4', 'Star Wars: Часть 5', 'Star Wars: Часть 6']].apply(lambda x: (x == 1).sum())

print()
print("Общее количество людей которым больше всего нравится 1 фильм, 2 фильм и т.д. (стоит 1 место)")
print(fav_films)

# Группируем людей по полу и выводим график зависимости пола от оценки каждой части
gender_pref = data.groupby('Пол')[[str1, 'Star Wars: Часть 2', 'Star Wars: Часть 3', 'Star Wars: Часть 4', 'Star Wars: Часть 5', 'Star Wars: Часть 6']].mean()

gender_pref.transpose().plot(kind='bar')

plt.ylabel('Оценка каждой части')
# plt.legend("График зависимости пола от оценки каждой части")
plt.show()

# Шаг 6: Беру среднее значение оценки каждого фильма по диапазону возраста и вывести на графике зависимость возраста от средней оценки каждого фильма
age_pref = data.groupby('Возраст')[[str1, 'Star Wars: Часть 2', 'Star Wars: Часть 3', 'Star Wars: Часть 4', 'Star Wars: Часть 5', 'Star Wars: Часть 6']].mean()
age_pref.plot(kind='bar')

plt.ylabel('Оценка каждой части')
plt.legend("123456")
plt.show()




print("------------------------------------")

# Установка максимального количества строк
pd.set_option('display.max_rows', 100)

# Установка максимального количества столбцов
pd.set_option('display.max_columns', None)


print(data)
data.to_csv('output_1.csv', index=False)
