from django.shortcuts import render, redirect
from django.db import connection
import bcrypt

# Create your views here.
def login(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        password = data.get('psw')
        cur = connection.cursor()
        query = "select password from user where email = %s"
        cur.execute(query,[email])
        try:
            db_password = cur.fetchone()[0]
            correct=bcrypt.checkpw(password.encode('ascii'),db_password.encode('ascii'))
            if correct:
                request.session['email'] = email
                return redirect('/calculator')
        except:
                return render(request,'login.html')        
        cur.close()
    return render(request,'login.html')

def register(request):
    if request.method == "POST":
        data = request.POST
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        height = data.get('height')
        weight = data.get('weight')
        dob = data.get('dob')
        gender = "" if data.get('gender')=="M" else None
        cur = connection.cursor()
        hashed = bcrypt.hashpw(password.encode('ascii'), bcrypt.gensalt()).decode('ascii')
        query = '''
            insert 
            into user (username,email,password,height,weight,dob,gender) 
            values (%s,%s,%s,%s,%s,%s,%s);
        '''
        cur.execute(query,[name,email,hashed,height,weight,dob,gender])
        print([name,email,hashed,height,weight,dob,gender])
        cur.close()
        return redirect('/')
    return render(request,"register.html")

def logout(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect("/")