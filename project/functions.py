from datetime import date, datetime, timedelta
from .models import User, Tasks
from sqlalchemy import func


def prevFourDays(taskTable):
    today=datetime.today()
    tomorrow=today+timedelta(days=1)
    four_daysago=today - timedelta(days=4)
    difference=today-four_daysago
    past_four_days_users=0 
    for dt in taskTable:
        if dt.date<today and dt.date>=four_daysago:
            past_four_days_users+=1
    return past_four_days_users

def country_city_dict(userTable, c2, c4):
    country_dict={}
    for country in c2:
        country_dict[country]=[]
        for city in c4:
            for k in userTable:
                if city == k.city:
                    if k.country==country:
                        if city not in country_dict[country]:
                            country_dict[country].append(city)
    key_list=list(country_dict.keys())
    return country_dict,key_list

def users_by_city(userTable, c4):
    users_list_city=[]
    users_from_city=0
    for i in c4:
        users_from_city=0
        for j in userTable:
            if i==j.city:
                users_from_city+=1
        users_list_city.append(users_from_city)
    return users_list_city,users_from_city

def get_Cities(userTable):
    c3=[]
    for cities in userTable:
        c3.append(cities.city)
    c4=[]
    city_count=0
    for cities in c3:
        if cities not in c4:
            city_count+=1
            c4.append(cities)
    return c4,city_count

def users_by_country(userTable, c2):
    users_list_country=[]
    users_from_country=0
    for i in c2:
        users_from_country=0
        for j in userTable:
            if i ==j.country:
                users_from_country+=1
        users_list_country.append(users_from_country)
    return users_list_country,users_from_country

def get_Countries(userTable):
    c1=[]
    for countries in userTable:
        c1.append(countries.country)
    c2=[]
    country_count=0
    for countries in c1:
        if countries not in c2:
            country_count += 1
            c2.append(countries)
    return c2,country_count



def getCitynumpercountry(country_dict, key_list):
    cities_by_country=[]
    for country in key_list:
        cities_by_country.append(len(country_dict[country]))
    return cities_by_country



def new_func():
    today=date.today()
    day_beforeEreYesterday=today-timedelta(days=4)
    tasks_list=Tasks.query.filter(func.date(Tasks.date).between(day_beforeEreYesterday,today)).all()

    tasks_list_2=[]
    for t in tasks_list:
        tasks_list_2.append(t.date.strftime('%m/%d/%Y'))

    tasks_dates=[]
    for i in range(5):
        tasks_dates.append(today-timedelta(days=4-i))
        tasks_dates[i]=tasks_dates[i].strftime('%m/%d/%Y')

    tasknum=[]
    for i in range(len(tasks_dates)):
        tasknum.append(0)
        for j in range(len(tasks_list_2)):
            if tasks_list_2[j]==tasks_dates[i]:
                tasknum[i]+=1


    return tasks_list_2,tasks_dates,tasknum