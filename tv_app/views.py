from django.shortcuts import render ,redirect
from . import models
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'log_reg_page.html')


def register(request):
    errors = models.User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        first_name = request.POST['firstname'] 
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        conferm_password = request.POST['Confirm_PW']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash for the password
        conf_pw_hash = bcrypt.hashpw(conferm_password.encode(), bcrypt.gensalt()).decode() #create the hash to conferm password
        models.create_a_user(first_name, last_name, email, pw_hash, conf_pw_hash)
        
        return redirect('/')

def login(request):
    errorslogin = models.User.objects.basic_validator(request.POST)
    if len(errorslogin) > 0:
        for key, value in errorslogin.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        user = models.User.objects.filter(email=request.POST['email'])
        if user: #if True , if user exists
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/shows')
            else:
                messages.error(request, "Invalid Password")
        else:
            messages.error(request, "Invalid email you have to register")
        return redirect('/')


def tv_shows(request):
    if 'user_id' not in request.session:  # if user is not logged in (not in the session)
        return redirect('/')
    all__the_shows = models.all_shows()
    context = {
        "all_shows" : all__the_shows ,
        'user': models.User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'shows.html', context)



# def shows(request):
#     all__the_shows = models.all_shows()
#     context = {
#         "all_shows" : all__the_shows
#     }
#     return render(request, 'shows.html' , context)

# def tv_shows(request):
#     return redirect('/shows')

def add_show_page(request):
    return render(request, 'add_show.html')

def get_show(request):
    errors = models.Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/new')
    else:
        show_title = request.POST['title'] 
        show_network = request.POST['network']
        show_release_date = request.POST['release_date']
        show_comment = request.POST['comment']
        models.create_a_show(show_title, show_network, show_release_date , show_comment)
        return redirect('/new')

def view_a_show(request, id):
    if 'user_id' not in request.session:  # if user is not logged in (not in the session)
        return redirect('/')
    the_show = models.view_a_show(id)
    the_comments = models.view_a_show(id).comments.all()
    context = {
        "a_show" : the_show ,
        "all_comments" : the_comments
    }
    return render(request, 'view_a_show.html', context)

def edit_a_show(request, id):
    if 'user_id' not in request.session:  # if user is not logged in (not in the session)
        return redirect('/')
    the_show = models.view_a_show(id)
    context = {
        "a_show" : the_show
    }
    return render(request, 'edit_a_show.html', context)

def update_a_show(request, id):
    errors = models.Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect(f'/edit_a_show/{id}' )
    else:
        show_title = request.POST['title']
        show_network = request.POST['network']
        show_release_date = request.POST['release_date']
        show_comment = request.POST['comment']
        models.update_a_show(id, show_title, show_network, show_release_date, show_comment)
        return redirect(f'/shows/{id}')


def post_a_comment(request ,id):
    show = models.view_a_show(id = id )
    the_comment = request.POST['comment']
    models.create_a_comment(the_comment, show )
    return redirect(f'/shows/{id}')
    


def delete_a_show(request, id):
    models.delete_a_show(id)
    return redirect('/shows')


def logout(request):
    request.session.clear()
    return redirect('/')