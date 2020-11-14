from django.db import models
import re


class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(form['email']):
            errors['email'] = 'Email must be valid'
        if len(form['first_name']) < 3:
            errors['first_name'] = 'First Name must be longer than 3 characters'
        if len(form['last_name']) < 3:
            errors['last_name'] = 'Last Name must be longer than 3 characters'
        if len(form['password']) == 0:
            errors['password'] = 'Password is required'
        if len(form['email']) == 0:
            errors['email'] = 'Email required'
        if form['password'] != form['confirm']:
            errors['password'] = 'Confirmation Mismatch'
        return errors



class User(models.Model):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Record(models.Model):

    name = models.CharField(max_length=255)
    device = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    problem_details = models.CharField(max_length=150)
    notes = models.TextField()
    technician = models.ForeignKey(User, related_name='tech_owned', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)