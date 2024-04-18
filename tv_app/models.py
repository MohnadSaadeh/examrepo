from django.db import models
import re
# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        errorslogin = {}
        #DATE_REGEX = re.compile(r'^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') # using regex to validate email
        # add keys and values to errors dictionary for each invalid field
        if postData['log_reg'] == 'register':
            if len(postData['firstname']) < 2  :
                errors["firstname"] = "First Name should be at least 3 characters"
            if len(postData['lastname']) < 2:
                errors["lastname"] = "last Name should be at least 3 characters"
            if not EMAIL_REGEX.match(postData['email']): # using regex to validate email
                errors['email'] = "Invalid email address!"
            if len(postData['password']) < 8: 
                errors["password"] = "a password should be at least 8 characters"
            if postData['password'] != postData['Confirm_PW']:
                errors["password"] = "passwords should match"
            return errors
        if postData['log_reg'] == 'login':
            if not EMAIL_REGEX.match(postData['email']): # using regex to validate email
                errorslogin['email'] = "Invalid email address!"
            if len(postData['password']) < 8:
                errorslogin["password"] = "a password should be at least 8 characters"
            return errorslogin

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    conferm_password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # shows : all the shows of the user 
    objects = UserManager()


class ShowManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        DATE_REGEX = re.compile(r'^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$')
        # add keys and values to errors dictionary for each invalid field
        if len(postData['title']) < 3  :
            errors["title"] = "title should be at least 3 characters"
        # if ( postData['title']  == Show.objects.filter(title = postData['title'])):
        #     errors["title"] = "title should be unique"
        if Show.objects.filter(title=postData['title']).exists():
            errors["title"] = "Title should be unique"
        if len(postData['network']) < 3:
            errors["network"] = "Network should be at least 3 characters"
        if len(postData['comment']) < 3: # shuld be at least 10 characters
            errors["comment"] = "a comment should be at least 3 characters"
        if not DATE_REGEX.match(postData['release_date']):
            errors["release_date"] = "the Date shuld be like YYYY-MM-DD"
        return errors

class Show(models.Model):
    title  = models.CharField(max_length= 45)
    network = models.CharField(max_length= 45)
    release_date = models.DateField()
    comment = models.TextField(max_length= 255)
    the_user = models.ForeignKey(User, related_name="shows", on_delete=models.CASCADE) # user can add many shows
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # comments : all the comments of the show
    objects = ShowManager()


class Comment(models.Model):
    content = models.TextField(max_length= 255)
    show = models.ForeignKey(Show, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def create_a_comment(the_comment, show ,user):
    show = Show.objects.get(id = show )
    user = User.objects.get(id = user)
    return Comment.objects.create(content=the_comment, show=show , user = user)


def create_a_show(show_title, show_network, show_release_date , show_comment , user):
    user_show = User.objects.get(id = user)
    return Show.objects.create(title=show_title , network=show_network , release_date=show_release_date , comment=show_comment , the_user = user_show )

def all_shows():
    return Show.objects.all()

def view_a_show(id):
    return Show.objects.get(id = id)


def update_a_show(id, show_title, show_network, show_release_date, show_comment):
    show = Show.objects.get(id = id)
    show.title = show_title
    show.network = show_network
    show.release_date = show_release_date
    show.comment = show_comment
    show.save()
    return show

def delete_a_show(id):
    show = Show.objects.get(id = id)
    return show.delete()

def delete_a_comment(id): 
    comment = Comment.objects.get(id = id)
    return comment.delete()



def create_a_user(first_name, last_name, email, pw_hash, conf_pw_hash):
    return User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash, conferm_password=conf_pw_hash)