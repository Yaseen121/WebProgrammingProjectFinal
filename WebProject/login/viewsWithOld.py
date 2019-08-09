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
#from .serializers import UserSerializer
#from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('loggedIn')
    else:
        hobbies = Hobby.objects.all()
        form = LoginForm()
        form2 = RegisterForm()
        context = {
            'hobbies': hobbies,
            'form': form,
            'regform': form2
        }
        return render(request, 'login/index.html',  context)

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
            if user is not None:
                login(request, user)
                return redirect('loggedIn')
            else:
                request.session.flush()
                raise Http404('Wrong password')
        else:
            print(form.errors)
            return redirect('index')

def myloginOld2(request):
    if not ('username' in request.POST and 'password' in request.POST):
        return render(request,'login/index.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        #try: member = User.objects.get(username=username)
        #except User.DoesNotExist: raise Http404('User does not exist')
        #if member.check_password(password):
            #return redirect('loggedIn')
        #else:
        #    raise Http404('Wrong password')
        ##########
        print(username)
        member = User.objects.filter(username=username)
        request.session['userID'] = member[0].id
        request.session['username'] = member[0].username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('loggedIn')
        else:
            request.session.flush()
            raise Http404('Wrong password')
        ################
        #member = User.objects.filter(username=username, password=password)
        #if (not member):
        #    raise Http404('Wrong password')
        #else:
        #    print(member[0].id)
        #    request.session['userID'] = member[0].id
        #    request.session['username'] = member[0].username
        #    return redirect('loggedIn')

def register(request):
    if request.method=='POST':
        usern = request.POST['username']
        passw = request.POST['password']
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.image = request.FILES['image']
            form.save()
            member = User.objects.get(username=usern)
            request.session['userID'] = member.id
            request.session['username'] = member.username
            print(passw)
            member.password = make_password(passw)
            member.save()
            user = authenticate(username=usern, password=passw)
            login(request, user)
            return redirect('loggedIn')
        else:
            if User.objects.filter(username=usern).exists():
                raise Http404('Username already in use')
            else:
                raise Http404('POST data missing')

def oldregister(request):
    if 'username' in request.POST and 'password' in request.POST and 'email' in request.POST and 'gender' in request.POST and 'dob' in request.POST and 'image' in request.POST:
        u = request.POST['username']
        p = request.POST['password']
        e = request.POST['email']
        g = request.POST['gender']
        d = request.POST['dob']
        i = request.POST['image']
        user = User(username=u, email=e, password=p, gender=g, dob=d)
        h = request.POST.getlist('hobby[]')
        try: user.save()
        except IntegrityError: raise Http404('Username '+u+' already taken: Usernames must be unique')
        user.addHobbies(h)
        return render(request,'login/loggedIn.html')

    else:
        raise Http404('POST data missing')

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

@login_required
def loggedIn(request):
    #This function takes the signed in user as a parameter and generates a list with the users with the most similar hobbies
    #in descending order. If there are no other users with even 1 similar hobby then the results are random user list.
    #It assigns users a rank which is made up from giving 1 point for each similar hobby or 0 if different.
    user = User.objects.get(id=request.session['userID'])
    print(user.userLikedBy.all().count())
    print(user.userLiked.all().count())
    count = 0;
    ranks = [0];
    users = [""];
    iterator = 0;
    all_users = User.objects.exclude(username=user.username)
    for x in all_users:
        #users[iterator] = x.username
        users[iterator] = x.id
        count = count +1;
        #print(x.hobby.all())
        #print("These are the hobbies for user: ", x.username)
        for k in user.hobby.all():
            for i in x.hobby.all():
                if(k == i):
                    #print("Match found! You share the following hobbies: ", k)
                    ranks[iterator] = ranks[iterator] + 1;
                else:
                    ranks[iterator] = ranks[iterator] + 0;
        if(count != len(all_users)):
            iterator = iterator + 1;
            ranks.append(0)
            users.append("")
    ###############
    #context = {
    #    'users': all_users, # Create a new array and load each user indiv using userID after it has been sorted
    #    'userID': users,
    #    'ranks': ranks
    #}
    #return render(request, 'login/loggedIn.html', context)
    ######################

    #inside ranks[] ==> amount of matched Hobbies
    #inside users[] ==> Usernames


    ranks, users = zip(*sorted(zip(ranks, users), reverse=True))
    ranks, users = (list(t) for t in zip(*sorted(zip(ranks, users),reverse=True)))
    #filterUsers(users)
    #return JsonResponse(users, safe=False)
    #can use the 'users' list to create the bullet points and then make ajax request to retrieve each users hobbies if needed
    #based on username
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
                            #print("Match found! You share the following hobbies: ", k)
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

            #all_users_ranked_list = serializers.serialize('json', all_users_ranked_list)

            results = [User.as_json() for User in all_users_ranked_list]
            jsonUser = user.username
            json = {
                'users': results,
                'curUser': jsonUser
                #'curuser': user,
                #'users': all_users_ranked_list, # Create a new array and load each user indiv using userID after it has been sorted
                #'userNames': filteredUsersNames,
                #'userEmails': filteredUsersEmails,
                #'ranks': ranks
            }
            print(json)
            return JsonResponse(json)

@login_required
def oldfilter(request):
    if request.method =="POST":
        minAge = request.POST['minAge']
        maxAge = request.POST['maxAge']
        gender = request.POST['gender']
        if minAge > maxAge:
            print("min cannot be greater than max")
            return redirect('loggedIn')
        else:
            print("minimum age :" + minAge)
            print("maximum age :" + maxAge)
            print("gender :" + gender)

            filteredList = []
            usersAge = []
            usersGender = []
            user = User.objects.get(id=request.session['userID'])
            users =  User.objects.exclude(username=user.username)
            for x in users:
                userDetails = User.objects.filter(username=x)
                usersAge.append(calculate_age(x.dob))
                usersGender.append(x.gender)

            counter=0;
            current = dt.now()
            if (minAge!=""):
                min_date = date(current.year - int(minAge), current.month, current.day)
            if (maxAge!=""):
                max_date = date(current.year - int(maxAge), current.month, current.day)

            if((gender=="Both") & (minAge=="") & (maxAge=="")):
                #Get everyone but current user
                filteredUsers = User.objects.exclude(username=user.username)
            elif((gender!="") & (minAge=="") & (maxAge=="")):
                #Get all the chosen gender excluding current user
                filteredUsers = User.objects.filter(gender=gender).exclude(username=user.username)
            elif((gender=="Both") & (minAge!="") & (maxAge=="")):
                #Get all users older than min age exlcuding current user
                filteredUsers = User.objects.filter(dob__lte=min_date).exclude(username=user.username)
            elif((gender=="Both") & (minAge=="") & (maxAge!="")):
                #Get all users less than max age exlcuding current user
                filteredUsers = User.objects.filter(dob__gte=max_date).exclude(username=user.username)
            elif((gender!="") & (minAge!="") & (maxAge=="")):
                #Get all users older than min age and of selected gender exlcuding current user
                filteredUsers = User.objects.filter(dob__lte=min_date, gender=gender).exclude(username=user.username)
            elif((gender!="") & (minAge=="") & (maxAge!="")):
                #Get all users less than max age and of selected gender exlcuding current user
                filteredUsers = User.objects.filter(dob__gte=max_date, gender=gender).exclude(username=user.username)
            elif((gender=="Both") & (minAge!="") & (maxAge!="")):
                #Get users between max and min age excluding current user
                filteredUsers = User.objects.filter(dob__gte=max_date, dob__lte=min_date).exclude(username=user.username)
            else:
                    #Get users between max and min age excluding current user
                    filteredUsers = User.objects.filter(dob__gte=max_date, dob__lte=min_date, gender=gender).exclude(username=user.username)

            print(filteredUsers)

            count = 0;
            ranks = [0];
            filteredUsersID = [""];
            iterator = 0;
            for x in filteredUsers:
                filteredUsersID[iterator] = x.id
                count = count +1;

                if(x.hobby.all().count() == 0):
                    print("This user has no hobbies")
                else:
                    for k in user.hobby.all():
                        for i in x.hobby.all():
                            if(k == i):
                                #print("Match found! You share the following hobbies: ", k)
                                ranks[iterator] = ranks[iterator] + 1;
                            else:
                                ranks[iterator] = ranks[iterator] + 0;
                if(count != len(filteredUsers)):
                    iterator = iterator + 1;
                    ranks.append(0)
                    filteredUsersID.append("")

            ranks, filteredUsersID = zip(*sorted(zip(ranks, filteredUsersID), reverse=True))
            ranks, filteredUsersID = (list(t) for t in zip(*sorted(zip(ranks, filteredUsersID),reverse=True)))

            all_users_ranked_list = []
            for x in filteredUsersID:
                all_users_ranked_list.append(User.objects.get(id=x))
            context = {
                'curuser': user,
                'users': all_users_ranked_list, # Create a new array and load each user indiv using userID after it has been sorted
                'userID': filteredUsersID,
                'ranks': ranks
            }
            return render(request, 'login/loggedIn.html', context)

def calculate_age(born):
    today = date.today()
    #print(today.year,today.month,today.day)
    #print(born.year,born.month,born.day)
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def logout_view(request):
    logout(request)
    print("Logged out")
    request.session.flush()
    return redirect('/')

def like(request):
    if request.method =="POST":
        likingUser = User.objects.get(username=request.session['username'])
        likedUser = request.POST['username']
        likedUserObj = User.objects.get(username=likedUser)
        new_like, created = Like.objects.get_or_create(user=likingUser, userLiked=likedUserObj)
        if not created:
            # the user already liked this picture before
            print("already liked")
            return HttpResponse("Already Liked")
        else:
            # oll korrekt
            print("liked")
            newLikeNum = likedUserObj.userLikedBy.all().count()
            return HttpResponse(str(newLikeNum) + " Success")
