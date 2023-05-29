from time import time
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date, datetime, timedelta
from .models import User, Tasks
from . import db
from sqlalchemy import desc,func
from .functions import *



views=Blueprint('views', __name__)

@views.route('/')
def mainpage():
    userTable=User.query.all()
    taskTable=Tasks.query.all()

    # Getting a list of Countries
    c2, country_count = get_Countries(userTable)

    # List of Users countrywise
    users_list_country, users_from_country = users_by_country(userTable, c2)
    
    #List of Cities
    c4, city_count = get_Cities(userTable)

    # List of user citywise
    users_list_city, users_from_city = users_by_city(userTable, c4)

    #Storing countries and their cities as a dict
    country_dict, key_list = country_city_dict(userTable, c2, c4)

    # Getting past 4 days
    past_four_days_users = prevFourDays(taskTable)

    cities_by_country = getCitynumpercountry(country_dict, key_list)

    
    tasks_list_2, tasks_dates, tasknum = new_func()

    return render_template('homepage.html',tasks_dates=tasks_dates,tasknum=tasknum,cities_by_country=cities_by_country,past_four_days_users=past_four_days_users,key_list=key_list,country_dict=country_dict,c2=c2,country_count=country_count,c4=c4,city_count=city_count,users_from_country=users_from_country, users_list_country=users_list_country,l1=len(c2),l2=len(c4),users_from_city=users_from_city,users_list_city=users_list_city,userTable=userTable)









@views.route('/adduser', methods=['GET','POST'])
def add_user():
    if request.method=='POST':
        name=request.form.get('Name')
        email=request.form.get('email')
        city=request.form.get('city')
        country=request.form.get('country')
        

        

        if len(email)<4:
            flash('Email must have more than 3 characters.', category='error')
        elif len(name)<2:
            flash('Name must have more than 1 character.', category='error')
        elif User.query.filter_by(email=email).first():
            flash('The user already exists', category='error')
        else:
            flash('User added', category='success')
            
            new_user=User(name=name,email=email,city=city,country=country)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('views.mainpage'))
        
        
    return render_template('adduser.html')


@views.route('/addtask', methods=['GET','POST'])
def add_task():
    if request.method=='POST':
        user_id=request.form.get('uid')
        task=request.form.get('task')

        i=User.query.filter_by(id=user_id).first()

        if len(task)<1:
            flash('Task must have more than 1 character.', category='error')
        elif not i:
            flash('No such user id exists',category='error')
        else:
            flash('Task added', category='success')
            new_task=Tasks(user_id=user_id,data=task)
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('views.mainpage'))

    ids = User.query.with_entities(User.id).order_by(desc(User.id)).all()
    return render_template('addtask.html',ids=ids)


@views.route('/showtasks',methods=['GET','POST'])
def show_tasks():
    if request.method=='POST':
        tasks=Tasks.query.order_by(Tasks.user_id).all()
        userTable=User.query.all()
        taskTable=Tasks.query.all()
        user_name=request.form.get('Uname')
        render_template('showtasks.html',userTable=userTable,taskTable=taskTable,user_name=user_name)

    user_name=request.form.get('Uname')
    tasks=Tasks.query.order_by(Tasks.user_id).all()
    userTable=User.query.all()
    taskTable=Tasks.query.all()
    return render_template('showtasks.html',userTable=userTable ,taskTable=taskTable,user_name=user_name)




@views.route("/delete/<int:id>")
def task_delete(id):
    task_tobe_deleted=Tasks.query.get_or_404(id)

    try:
        db.session.delete(task_tobe_deleted)
        db.session.commit()
        return redirect("/")
    except:
        return 'There was a problem with deletion'



@views.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    task=Tasks.query.get_or_404(id)

    if request.method=='POST':
        task.data=request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue again'
    else:
        return render_template('update.html',task=task)