import pandas as pd

data = pd.read_csv("C:/Users/shelk/Desktop/Data/adult.data", )
# 1. Сколько мужчин и женщин (признак sex) представлено в этом наборе данных?
print("Male:", data[' Male'].value_counts()[0])
print("Female:", data[' Male'].value_counts()[1])

# 2. Каков средний возраст (признак age) женщин?
print("Средний возраст:", data.loc[data[' Male'] == ' Female', '39'].mean())

# 3. Какова доля граждан Германии (признак native-country)?
result = (float(((data[' United-States'] == ' Germany').sum()) / data.shape[0]))
print("Доля граждан", result * 100, "%")

# 4-5. Каковы средние значения и среднеквадратичные отклонения возраста тех,
# кто получает более 50K в год (признак salary) и тех, кто получает менее 50K в год?
av_age1 = data.loc[data[' <=50K'] == ' >50K', '39'].mean()
print("ср. знач >50K:", av_age1)
av_age2 = data.loc[data[' <=50K'] == ' <50K', '39'].mean()
print("ср. знач <50K:", av_age1)
# std
std_age1 = data.loc[data[' <=50K'] == ' >50K', '39'].std()
print("станд откл. знач >50K:", std_age1)
std_age2 = data.loc[data[' <=50K'] == ' <=50K', '39'].std()
print("станд откл. знач <50K:", std_age2)

# 6. Правда ли, что люди, которые получают больше 50k, имеют как минимум высшее образование?
# (признак education – Bachelors, Prof-school, Assoc-acdm, Assoc-voc, Masters или Doctorate)
spec50 = (data.loc[data[' <=50K'] == ' >50K', ' Bachelors'].unique())
print("Образование:", ",".join(spec50))
if " 11th" in spec50:
    print("no, <50K образование:11th")
else:
    print("yes")

# 7. Выведите статистику возраста для каждой расы (признак race) и каждого пола. Используйте groupby и describe.
# Найдите таким образом максимальный возраст мужчин расы Amer-Indian-Eskimo.
print("Статистика возраста для каждой расы и каждого пола:")
for (White, Male), element in data.groupby([' White', ' Male', ]):
    print("Race: {0}, sex: {1}".format(White, Male))
    print(element['39'].describe())

# 8. Среди кого больше доля зарабатывающих много (>50K): среди женатых или холостых мужчин (признак marital-status)?
# Женатыми считаем тех, у кого marital-status начинается с Married
# (Married-civ-spouse, Married-spouse-absent или Married-AF-spouse), остальных считаем холостыми.
marr = data.loc[((data[' Male'] == ' Male') & (
    data[' Never-married'].isin([' Married-civ-spouse', ' Married-spouse-absent', ' Married-AF-spouse'])) & (
                         data[' <=50K'] == ' >50K'))].value_counts()
unmarr = data.loc[((data[' Male'] == ' Male') & (
    data[' Never-married'].isin([' Separated', ' Never-married', ' Divorced', ' Widowed'])) & (
                           data[' <=50K'] == ' >50K'))].value_counts()
print("Доля женатых:", (marr.count()))
print("Доля неженатых:", unmarr.count())

if (marr.count() > unmarr.count()):
    print("Доля женатых >50K больше")
else:
    print("Доля неженатых >50K больше")

# 9. Какое максимальное число часов человек работает в неделю (признак hours-per-week)?
# Сколько людей работают такое количество часов и каков среди них процент зарабатывающих много?
max = data[' 40'].max()
print("max число часов:", max)

number = data[data[' 40'] == max].shape[0]
print("кол-во людей работающих max часов:", number)

rich = float(data[(data[' 40'] == max) & (data[' <=50K'] == ' >50K')].shape[0]) / number
print("процент зарабатывающих много", rich * 100, "%")

# 10. Посчитайте среднее время работы (hours-per-week) зарабатывающих мало
# и много (salary) для каждой страны (native-country).
for (country, salary), sub_df in data.groupby([' United-States', ' <=50K']):
    print(country, salary, round(sub_df[' 40'].mean(), 2))

import pandas as pd
import seaborn as sns

df = pd.read_csv("C:/Users/shelk/Desktop/howpop_train.csv")
print(df.shape)
print(df.head(3).T)
df.drop(
    filter(lambda c: c.endswith("_lognorm"), df.columns),
    axis=1,  # axis = 1: столбцы
    inplace=True,
)  # избавляет от необходимости сохранять датасет
print(df.describe().T)
print(df.describe(include=["object", "bool"]).T)  # бинарные и категориальные переменные
# настройка внешнего вида графиков в seaborn
sns.set_style("dark")
sns.set_palette("RdBu")
sns.set_context(
    "notebook", font_scale=1.5, rc={"figure.figsize": (15, 5), "axes.titlesize": 18}
)
print(df.published.dtype)
df["published"] = pd.to_datetime(df.published, yearfirst=True)
print(df.published.dtype)
df["year"] = [d.year for d in df.published]
df["month"] = [d.month for d in df.published]

df["dayofweek"] = [d.isoweekday() for d in df.published]
df["hour"] = [d.hour for d in df.published]
"""
1. В каком месяце (и какого года) было больше всего публикаций?
март 2016
март 2015
апрель 2015
апрель 2016
"""
dateFrame = df[df.year > 2014].groupby(['year', 'month'], sort=True)['post_id'].count()
dateFrame.sort_values(ascending=False, inplace=True)
val = dateFrame.head(1).index.values[0]
print("Больше всего публикаций:", val)
"""
2. Проанализируйте публикации в месяце из предыдущего вопроса
Выберите один или несколько вариантов:

Один или несколько дней сильно выделяются из общей картины
На хабре всегда больше статей, чем на гиктаймсе
По субботам на гиктаймс и на хабрахабр публикуют примерно одинаковое число статей
"""

dateFrame = df[(df.year == val[0]) & (df.month == val[1])].copy()
dateFrame = dateFrame.groupby('dayofweek')['post_id'].count().T
dateFrame.plot(kind='bar', rot=90, grid=True)
# plt.show()
"""
3. Когда лучше всего публиковать статью?
Больше всего просмотров набирают статьи, опубликованные в 12 часов дня
У опубликованных в 10 утра постов больше всего комментариев
Больше всего просмотров набирают статьи, опубликованные в 6 часов утра
Максимальное число комментариев на гиктаймсе набрала статья, опубликованная в 9 часов вечера
На хабре дневные статьи комментируют чаще, чем вечерние
"""
dateFrame = df.groupby(['hour'], sort=True)['views'].sum()
dateFrame.sort_values(ascending=False, inplace=True)
dateFrame.plot(kind='bar', rot=90, grid=True, title='Views')
# plt.show()

"""
4. Кого из топ-20 авторов чаще всего минусуют?
@Mordatyj
@Mithgol
@alizar
@ilya42
"""
dateFrame = df.copy()
dateFrame = dateFrame.groupby(['author'], sort=True)['post_id'].count()
dateFrame.sort_values(ascending=False, inplace=True)
topAuthor = dateFrame.head(20).index.values

dateFrame = df[df.author.isin(topAuthor)].groupby(['author'], sort=True)['votes_minus'].count()
dateFrame.plot(kind='bar', grid=True, rot=45)
# plt.show()

"""
5. Сравните субботы и понедельники
Правда ли, что по субботам авторы пишут в основном днём, а по понедельникам — в основном вечером?
"""
dateFrame = df.copy()
dateFrame = \
dateFrame[(dateFrame.dayofweek.isin([1, 6]))
          & (dateFrame.hour >= 12)].groupby(['dayofweek', 'hour'], sort=True)['post_id'].count()
dateFrame.plot(kind='bar', grid=True, rot=45)
# plt.show()
