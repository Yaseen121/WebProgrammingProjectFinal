from django.shortcuts import render, redirect
from login.models import User, Hobby
from django.http import HttpResponse, Http404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, RegisterForm
from datetime import date
#from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    hobbies = Hobby.objects.all()
    form = LoginForm()
    form2 = RegisterForm()
    context = {
        'hobbies': hobbies,
        'form': form,
        'regform': form2
    }

    return render(request, 'login/index.html',  context)

def login(request):
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
        member = User.objects.filter(username=username, password=password)
        if (not member):
            raise Http404('Wrong password')
        else:
            print(member[0].id)
            request.session['userID'] = member[0].id
            request.session['username'] = member[0].username
            return redirect('loggedIn')

def oldloggedIn(request):
    return render(request, 'login/loggedIn.html')

def register(request):
    if request.method=='POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.image = request.FILES['image']
            form.save()
            return render(request,'login/loggedIn.html')
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

#@login_required
def loggedIn(request):
    #This function takes the signed in user as a parameter and generates a list with the users with the most similar hobbies
    #in descending order. If there are no other users with even 1 similar hobby then the results are random user list.
    #It assigns users a rank which is made up from giving 1 point for each similar hobby or 0 if different.
    user = User.objects.get(id=request.session['userID'])
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

    print(users)
    print(ranks)
    ranks, users = zip(*sorted(zip(ranks, users), reverse=True))
    ranks, users = (list(t) for t in zip(*sorted(zip(ranks, users),reverse=True)))
    print(users,ranks)
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

def filter(request):
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

            print(users)
            print(usersAge)
            print(usersGender)
            counter=0;
            filteredUsers = [];
            for x in users:
                if((gender != '') & (int(minAge) >= 0) & (int(maxAge) != 0)):
                    #i.e filter by gender AND age
                    if(gender == 'Male'):
                        if((usersGender[counter] == 'Male') & (usersAge[counter] >= int(minAge)) & (usersAge[counter] <= int(maxAge))):
                            #adduser to array
                            filteredUsers.append(User.objects.get(username=x.username))
                            #print("Add this user: " + x.username + "1")
                    else:
                        if((usersGender[counter] == 'Female') & (usersAge[counter] >= int(minAge)) & (usersAge[counter] <= int(maxAge))):
                            #add user to array
                            filteredUsers.append(User.objects.get(username=x.username))
                            #print("Add this user: " + x.username + "2")
                elif((gender != 'Male') & (gender != 'Female') & int(minAge) | int(maxAge) >= 0):
                    if ((usersAge[counter] >= int(minAge)) & (usersAge[counter] <= int(maxAge))):
                        #add user to array
                        filteredUsers.append(User.objects.get(username=x.username))
                        #print("Add this user: " + x.username + "3")
                    else:
                        if (usersGender[counter] == gender):
                            #add user to array
                            filteredUsers.append(User.objects.get(username=x.username))
                            #print("Add this user: " + x.username + "4")
                counter=counter+1
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
