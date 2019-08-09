# Web Programming Project Final - A Matching Django Web App

A matching site built with Django.

### Homepage

[![django-matching-web-app](http://img.youtube.com/vi/AwrsrltusaA/0.jpg)](http://www.youtube.com/watch?v=AwrsrltusaA "Web Project Video")
>See YoutTube Video for demo. 

> On the homepage, the user is presented with the current weather conditions for their location. The user is also able to enter any time during the day along with a value for how long they would like to run, and the app would then present a forecast for that time period. 

1. Users	can	create	an	account	on	the	site	and	login.	
2. The	user’s	proFile	should	contain	(at	least):	proFile	image,	email,	gender,	date	of	birth,	
and	a	list	of	hobbies.	
3. The	overall	list	of	hobbies	should	be	deFined	in	advance	by	the	application	developer,	
so	the	users	of	the	site	can	only	select	one	or	more	hobbies	from	the	given	list.	(i.e.	on	
your	DB	you	should	have	a	table	for	User	and	another	for	Hobby,	with	a	many-to-many	
relationship	between	them)			
4. Users	should	then	see	a	list	of	other	users	who	have	the	most	similar	set	of	hobbies,	
i.e.	for	each	two	users	you	should	count	how	many	hobbies	in	common	they	have,	and	
then	list	those	users	in	descending	order	(users	with	most	common	hobbies	First).		
5. From	the	list	above	users	should	be	able	to	Filter	by	gender	and/or	age,	e.g.	only	
females	with	ages	between	30	and	50.	Searching	and	Filtering	should	be	done	using	
Ajax	and	jQuery.	
6. Frontend	should	use	Bootstrap,	and	be	responsive.	
7. Apart	from	the	basic	features	above,	you	should	implement	at	least	one	extra	feature.	
Feel	free	to	include	any	extra	feature	you	can	think	of.	Here	are	two	examples	of	
possible	extra	features:	
a) Users	are	able	to	request	to	connect	with	another	user.	The	other	user	would	then	
need	to	approve	the	request.	
b) Users	are	able	to	“like”	other	users	—	and	users	receive	alerts	or	emails	when	
someone	likes	them.	


## Installation

```sh
git clone https://github.com/Yaseen121/WebProgrammingProjectFinal.git
cd WebProject
python manage.py runserver
```

## Disclaimer

 - For secuirty purposes, details in the settings.py file have been removed, these will need to be replaced to run the web application. This includes the host for the database and the Gmail that the server uses to send notifications. 
 
 
# Group Project Contributors:
 -  [Yaseen Sultan](https://github.com/Yaseen121)
 -  [Aasif Khan](https://github.com/Blazero100)
 -  [Marios Hadjigeorgiou](https://github.com/marios50)
 -  [Maksym Sokolenko](https://github.com/MaksymSok)
 
    
