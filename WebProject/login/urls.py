from django.urls import path
from django.contrib.auth import views as auth_views
from login import views

urlpatterns = [
	# main page
    path('', views.index, name='index'),
    path('mylogin/', views.mylogin, name="mylogin"),
    path('register/', views.register, name="register"),
    path('profile/<int:id>/', views.profile, name="profile"),
    path('loggedIn/', views.loggedIn, name="loggedIn"),
    path('filter/', views.filter, name="filter"),
    path('login/',auth_views.LoginView.as_view(template_name="login/index.html"), name="login"),
    path('logout_view/', views.logout_view, name="logout_view"),
    path('like/', views.like, name="like"),
    # signup page

]
