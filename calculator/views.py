from django.shortcuts import render
from django.db import connection

# Create your views here.
def calculate(request):
    cur = connection.cursor()
    query = '''
        select 
        username, weight, height, TIMESTAMPDIFF(YEAR, dob, CURDATE()) AS age, gender
        from user
        where email = %s;
    '''
    cur.execute(query,[request.session['email']])
    data = cur.fetchone()
    cur.close()
    dictionary = {
        'name' : data[0],
        'weight' : data[1],
        'height' : data[2],
        'age' : data[3],
        'gender' : data[4],
    }
    
    if request.method=="POST":
        data = request.POST
        name=data.get('name')
        weight=float(data.get('weight'))
        height=float(data.get('height'))
        age=data.get('age')
        gender=data.get('gender')
        goal=data.get('goal')
        cur = connection.cursor()
        cur.execute("select height, weight from user where email = %s;",[request.session['email']])
        old_height,old_weight=cur.fetchone()
        if not (weight == old_weight and height == old_height):
            cur.execute("update user set height = %s, weight = %s where email = %s;",[height,weight,request.session['email']])
        bmi = round(weight*10000/(height*height),2)
        cur.close()
        
        return render(request,'bmi.html',{'bmi':bmi})
    return render(request, 'main.html',dictionary)

def plan(request):
    cur = connection.cursor()
    query = '''
        select 
        username, gender, height, weight 
        from user 
        where email = %s;
    '''
    cur.execute(query,[request.session['email']])
    data = cur.fetchone()
    bmi = round(data[3]*10000/(data[2]*data[2]),2)
    dictionary = {
        'name' : data[0],
        'gender': "Male" if data[1] == "" else "Female",
        'bmi': bmi,
    }
    if data[1] == "":
        cur.execute("select diet from plan where %s between bmi_start and bmi_end and gender = '';",[bmi])
    else:
        cur.execute("select diet from plan where %s between bmi_start and bmi_end and gender is NULL;",[bmi])
    diet = cur.fetchone()
    dictionary['diet'] = diet[0].split("\n")[:-1]
    return render(request,"plan.html",dictionary)