from django.shortcuts import render, redirect
from login.models import User, Hobby, Like
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from django.template import loader
from .forms import LoginForm, RegisterForm
from datetime import date, datetime as dt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.mail import EmailMessage

#If a user is authenticated i.e there is a session for this user, they are redirected to the loggedIn page to use the page.
#If the user is not logged in, they are presented with a login and register page.
def index(request):
    #Doesnt allow admin users to go to loggedIn page (auto logs out)
    #This is because when super user is created he doesnt use the extension type that we defined so its not the same
    #And thus loading any page as an admin created using the command would result in an error 
    if request.user.is_superuser:
         logout_view(request)
    if not request.user.is_superuser and request.user.is_authenticated:
        return redirect('loggedIn')
    else:
        form = LoginForm()
        form2 = RegisterForm()
        context = {
            'form': form,
            'regform': form2
        }
        return render(request, 'login/index.html',  context)

#This function processes the login operation. It creates a session for a newly logged in user or returns an error if the login credentials are invalid.
def mylogin(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            member = User.objects.filter(username=username)
            request.session['userID'] = member[0].id
            request.session['username'] = member[0].username
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('loggedIn')
        else:
            #Form was not valid so reload index with form errors
            #Reload index page with form errors
            form2 = RegisterForm()
            context = {
                'form': form,
                'regform': form2,
            }
            return render(request, "login/index.html", context)

#This function processes the register operation. It creates a session for a newly registered user or returns an error if the username or email already exist in the DB.
def register(request):
    if request.method=='POST':
        usern = request.POST['username']
        passw = request.POST['password']
        email = request.POST['email']
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.image = request.FILES['image']
            form.save()
            member = User.objects.get(username=usern)
            request.session['userID'] = member.id
            request.session['username'] = member.username
            member.password = make_password(passw)
            member.save()
            user = authenticate(username=usern, password=passw)
            login(request, user)
            return redirect('loggedIn')
        else:
            request.session.flush()
            logInForm = LoginForm()
            #Reloads login form + the register form with ther errors
            #Reloads the inex page with this context so the corresponding errors are displayed
            context = {
                'form': logInForm,
                'regform': form,
            }
            return render(request, "login/index.html", context)


#Method that was used to test the profile card template that we created
#No longer used but kept as we adapted and re-used some of the logic elsewhere
@login_required
def profile(request, id):
    if request.method =="GET":
        user = User.objects.get(id=id)
        context = {
            'u' : user.username,
            'e' : user.email,
            'g' : user.gender,
            'd' : user.dob,
            'img' : user.image.url,
            'h' : user.hobby.all()
        }
    return render(request, 'login/profile.html', context)

#This function uses the default @login_required decorator that makes it so you can only run this function when logged in
#The function takes the signed in user from the session variable in user as a parameter and generates a list with the users with the most similar hobbies
#in descending order. If there are no other users with even 1 similar hobby then the results are random user list.
#It assigns users a rank which is made up from giving 1 point for each similar hobby or 0 if different.
@login_required
def loggedIn(request):
    #Doesnt allow admin user to access logged in page as admin does not have correct model fields and thus causes errors
    if request.user.is_superuser:
        return redirect ('index')
    user = User.objects.get(id=request.session['userID'])
    #print(user.userLikedBy.all().count())#How to get list of users who the logged in user is liked by
    #print(user.userLiked.all().count())#How to get list of users who the logged in likes
    count = 0;
    ranks = [0];
    users = [""];
    iterator = 0;
    all_users = User.objects.exclude(username=user.username)
    ##If no other users just display newly registered user
    if not all_users:
        context = {
            'curuser': user,
            'userID': users,
            'ranks': ranks
        }
        return render(request, 'login/loggedIn.html', context)
    for x in all_users:
        users[iterator] = x.id
        count = count +1;
        for k in user.hobby.all():
            for i in x.hobby.all():
                if(k == i):
                    ranks[iterator] = ranks[iterator] + 1;
                else:
                    ranks[iterator] = ranks[iterator] + 0;
        if(count != len(all_users)):
            iterator = iterator + 1;
            ranks.append(0)
            users.append("")

    ranks, users = zip(*sorted(zip(ranks, users), reverse=True))
    ranks, users = (list(t) for t in zip(*sorted(zip(ranks, users),reverse=True)))

    all_users_ranked_list = []
    for x in users:
        all_users_ranked_list.append(User.objects.get(id=x))
    context = {
        'curuser': user,
        'users': all_users_ranked_list, # Create a new array and load each user indiv using userID after it has been sorted
        'userID': users,
        'ranks': ranks
    }
    return render(request, 'login/loggedIn.html', context)

#This function handles the filtering functionality based on the paramaters received from the AJAX request on the front-end.
#The results from the filtering are then sorted based on hobbies once again and returned to the front-end via JSON to be displayed.
#The sort is done the same way as in the previous function
@login_required
def filter(request):
    if request.method =="POST":
        minAge = request.POST['minAge']
        maxAge = request.POST['maxAge']
        gender = request.POST['gender']
        filteredList = []
        usersAge = []
        user = User.objects.get(username=request.session['username'])
        users =  User.objects.exclude(username=user.username)
        for x in users:
            userDetails = User.objects.filter(username=x)
            usersAge.append(calculate_age(x.dob))

        counter=0;
        current = dt.now()
        if (minAge!=""):
            min_date = date(current.year - int(minAge), current.month, current.day)
        if (maxAge!=""):
            max_date = date(current.year - int(maxAge), current.month, current.day)

        if((gender=="Both") & (minAge=="") & (maxAge=="")):
            #Get everyone but current user
            filteredUsers = User.objects.exclude(username=user.username)
        elif((gender!="Both") & (minAge=="") & (maxAge=="")):
            #Get all the chosen gender excluding current user
            filteredUsers = User.objects.filter(gender=gender).exclude(username=user.username)
        elif((gender=="Both") & (minAge!="") & (maxAge=="")):
            #Get all users older than min age exlcuding current user
            filteredUsers = User.objects.filter(dob__lte=min_date).exclude(username=user.username)
        elif((gender=="Both") & (minAge=="") & (maxAge!="")):
            #Get all users less than max age exlcuding current user
            filteredUsers = User.objects.filter(dob__gte=max_date).exclude(username=user.username)
        elif((gender!="Both") & (minAge!="") & (maxAge=="")):
            #Get all users older than min age and of selected gender exlcuding current user
            filteredUsers = User.objects.filter(dob__lte=min_date, gender=gender).exclude(username=user.username)
        elif((gender!="Both") & (minAge=="") & (maxAge!="")):
            #Get all users less than max age and of selected gender exlcuding current user
            filteredUsers = User.objects.filter(dob__gte=max_date, gender=gender).exclude(username=user.username)
        elif((gender=="Both") & (minAge!="") & (maxAge!="")):
            #Get users between max and min age excluding current user
            filteredUsers = User.objects.filter(dob__gte=max_date, dob__lte=min_date).exclude(username=user.username)
        else:
            #Get users between max and min age excluding current user
            filteredUsers = User.objects.filter(dob__gte=max_date, dob__lte=min_date, gender=gender).exclude(username=user.username)

        if not filteredUsers:
            message="There are no users that satsify your requirements"
            return JsonResponse({'status':'false','message':message}, status=500)
        else:

            count = 0;
            ranks = [0];
            filteredUsersNames = [""];
            filteredUsersEmails = [""];
            iterator = 0;
            for x in filteredUsers:
                filteredUsersNames[iterator] = x.username
                count = count +1;

                for k in user.hobby.all():
                    for i in x.hobby.all():
                        if(k == i):
                            ranks[iterator] = ranks[iterator] + 1;
                        else:
                            ranks[iterator] = ranks[iterator] + 0;
                if(count != len(filteredUsers)):
                    iterator = iterator + 1;
                    ranks.append(0)
                    filteredUsersNames.append("")

            ranks, filteredUsersNames = zip(*sorted(zip(ranks, filteredUsersNames), reverse=True))
            ranks, filteredUsersNames = (list(t) for t in zip(*sorted(zip(ranks, filteredUsersNames),reverse=True)))
            all_users_ranked_list = []
            for x in filteredUsersNames:
                all_users_ranked_list.append(User.objects.get(username=x))
                filteredUsersEmails.append((User.objects.get(username=x)).email)

            results = [User.as_json() for User in all_users_ranked_list]
            jsonUser = user.username
            json = {
                'users': results,
                'curUser': jsonUser
            }
            return JsonResponse(json)

#This function returns the age of a user given the DOB in an integer form.
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

#This function handles the logout functionality i.e flushing the session.
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('/')

#This function handles the 'like' extra feature. It communicates the like to the database and also notifies the liked user via email.
@login_required
def like(request):
    if request.method =="POST":
        likingUser = User.objects.get(username=request.session['username'])#Gets the current user
        likedUser = request.POST['username']
        likedUserObj = User.objects.get(username=likedUser)#Gets the user that is being liked
        #Create the like if it doesnt already exist
        new_like, created = Like.objects.get_or_create(user=likingUser, userLiked=likedUserObj)
        if not created:
            # the user already liked this picture before
            return HttpResponse("Already Liked")
        else:
            newLikeNum = likedUserObj.userLikedBy.all().count()
            #Creates the message for email saying who the user was liked by
            message = "You've been liked by " + likingUser.username
            toEmail = likedUserObj.email
            #Create and send the email
            email = EmailMessage("You've been liked", message, to=[toEmail])
            email.send()
            return HttpResponse(str(newLikeNum) + " Success")
