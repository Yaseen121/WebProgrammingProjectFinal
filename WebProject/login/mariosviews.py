from django.shortcuts import render, redirect
from login.models import User, Hobby
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from datetime import date
# Create your views here.
def index(request):
    hobbies = Hobby.objects.all()
    context = {
        'hobbies': hobbies
    }
    return render(request, 'login/index.html', context)

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
            generateSimilar(member)
            return redirect('loggedIn')

def loggedIn(request):
    return render(request, 'login/loggedIn.html')

def register(request):
    if 'username' in request.POST and 'password' in request.POST and 'email' in request.POST and 'gender' in request.POST and 'dob' in request.POST and 'image' in request.POST:
        u = request.POST['username']
        p = request.POST['password']
        e = request.POST['email']
        g = request.POST['gender']
        d = request.POST['dob']
        i = request.POST['image']
        user = User(username=u, email=e, password=p, gender=g, dob=d, image=i)
        h = request.POST.getlist('hobby[]')
        try: user.save()
        except IntegrityError: raise Http404('Username '+u+' already taken: Usernames must be unique')
        user.addHobbies(h)
        return render(request,'login/loggedIn.html')

    else:
        raise Http404('POST data missing')

def generateSimilar(user):
    #This function takes the signed in user as a parameter and generates a list with the users with the most similar hobbies
    #in descending order. If there are no other users with even 1 similar hobby then the results are random user list.
    #It assigns users a rank which is made up from giving 1 point for each similar hobby or 0 if different.
    count = 0;
    ranks = [0];
    users = [""];
    iterator = 0;
    print(user[0].hobby.all())
    all_users = User.objects.exclude(username=user[0].username)
    for x in all_users:
        users[iterator] = x.username
        count = count +1;
        print(x.hobby.all())
        print("These are the hobbies for user: ", x.username)
        if(x.hobby.all().count() == 0):
            print("This user has no hobbies")
        else:
            for k in user[0].hobby.all():
                for i in x.hobby.all():
                    if(k == i):
                        print("Match found! You share the following hobbies: ", k)
                        ranks[iterator] = ranks[iterator] + 1;
                    else:
                        ranks[iterator] = ranks[iterator] + 0;
        if(count != len(all_users)):
            iterator = iterator + 1;
            ranks.append(0)
            users.append("")

    print(users)
    print(ranks)
    ranks, users = zip(*sorted(zip(ranks, users), reverse=True))
    ranks, users = (list(t) for t in zip(*sorted(zip(ranks, users),reverse=True)))
    print(users,ranks)
    filterUsers(users)
    #return JsonResponse(users, safe=False)
    #can use the 'users' list to create the bullet points and then make ajax request to retrieve each users hobbies if needed
    #based on username


#def filterUsers(request):
    #This function assumes that the request contains the following:
    #variables to use: user_list(usernames from bulletpoints) or if sessions are implemented then we will use the session_id
    #to call generateSimilar() and filter that
    #Other variables required: minage,maxage,gender

    #for now we will use hard coded parameters in the codes along with the logged in users list of users with similar hobbies in the db (to be changed when sessions & front-end design is done)

def filterUsers(users):
    #this will change when sessions are used as we should be able to use django based
    #filtering methods and pass the list to generateSimilar to rank them again
    #Uses arrays in parallel as in generateSimilar()

    filteredList = []
    usersAge = []
    usersGender = []
    minAge=20
    maxAge=40
    gender='Male'

    for x in users:
        userDetails = User.objects.filter(username=x)
        usersAge.append(calculate_age(userDetails[0].dob))
        usersGender.append(userDetails[0].gender)

    print(users)
    print(usersAge)
    print(usersGender)

    for x in users:
        if(gender != '' && minAge || maxAge != 0):
            #i.e filter by gender AND age
            if(gender == 'Male'):
                if(usersGender == 'Male' && (usersAge >= minAge && usersAge <= maxAge))
                    #adduser to array
            else:
                if(usersGender == 'Female' && (usersAge >= minAge && usersAge <= maxAge))
                    #add user to array
        if(gender == '' && minAge || maxAge != 0):
            if usersAge >= minAge && usersAge <= maxAge
                #add user to array
        else:
            if usersGender == gender:
                #add user to array


def calculate_age(born):
    today = date.today()
    #print(today.year,today.month,today.day)
    #print(born.year,born.month,born.day)
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))




















def loggedIn(request):
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
        'users': all_users_ranked_list, # Create a new array and load each user indiv using userID after it has been sorted
        'userID': filteredUsersID,
        'ranks': ranks
    }
    return render(request, 'login/loggedIn.html', context)
