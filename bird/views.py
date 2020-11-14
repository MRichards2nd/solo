from django.shortcuts import render, redirect
import bcrypt
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'records': Record.objects.all()
    }
    return render(request, 'success.html', context)

def login(request):
    if request.method == 'POST':
        logged_user = User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user = logged_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/success')
    return redirect('/')

def register(request):
    if request.method == "GET":
        return redirect('/')

    errors = User.objects.validate(request.POST)
    if errors:
        for (key,value) in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_pw=request.POST['password']
        hash_pw=bcrypt.hashpw(user_pw.encode(),bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name = request.POST['first_name'],
                                       last_name = request.POST['last_name'],
                                       email = request.POST['email'],
                                       password = hash_pw)
        #request.session['user_id'] = new_user.id
        messages.success(request, "Successful Registration!")
        return redirect('/')

def create(request):
    return render(request, 'record.html')

def add_record(request):
    Record.objects.create(
        name = request.POST['name'],
        device = request.POST['device'],
        code = request.POST['code'],
        problem_details = request.POST['problem_details'],
        notes = request.POST['notes'],
        technician = User.objects.get(id=request.session['user_id'])
    )
    return redirect('/success')

def view_record(request, id):
    context = {
        'record': Record.objects.get(id=id)
    }
    return render(request, 'view.html', context)

def edit_record(request, id):
    context = {
        'record': Record.objects.get(id=id)
    }
    return render(request, 'edit.html', context)

def update_record(request, id):
    record_update = Record.objects.get(id=id)
    record_update.notes = request.POST['notes']
    record_update.save()
    return redirect('/success')

def delete(request, id):
    record_delete = Record.objects.get(id=id)
    record_delete.delete()
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')