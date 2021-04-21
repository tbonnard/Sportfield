# Sportfield


Final Project of the [Harvard - CS50’s Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2020/ "CS50 - Web Programming with Python and JavaScript")
</br>
The goal of the project was to design and implement a dynamic website with Django and JavaScript.
</br>
The platform is just a project, but not a realistic platform on which you can trully book a field.
</br></br>
Details [About the course](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript "About CS50 - Web Programming with Python and JavaScript")
</br></br>
### Languages of the platform
python 3.7
</br>Django framework
</br>javascript <i>(data fetch / Data calls / DOM)</i>
</br>HTML
</br>CSS / Bootstrap
</br>

### Demo of the plaform
[Live demo](http://sportfield.pythonanywhere.com)
</br></br>

## About the platform</br>
<p>This platform is a web platform allowing users to book sport fields.
</br></br>In order to do so, the platform groups two types of users:
</br>- Club owner: user that can create a new club and add new fields to that club, and book fields
<i>Depending on the page this pro user is, the color is different, to differentiate when the user is interacting for himself (booking, user info) or for the club (create a club, add a field, manage the field's schedules)</i>
</br>- Standard user: user that can book fields (but can not create clubs, fields).
</p>
</br>


### Global flow of the club owner:</br>
<p>
The user must create an account. While creating an account (register page), he must specify he is a "pro" user (pro for professional). 
The fact to select "pro" allows the user to create clubs and fields.
Once the user is created as a "pro", he can create a new club (name, address, image of the club).
Once a club has been created, the user can add fields to that club. A field can not be created without a club.
To create a field, the user must enter a name, a type of sport (there are default categories coming from a model) a price per hour for the field and, if the address of the field is different than the one from the club (the parent), the user can enter another address.
Once a field has been created, the user can add "schedules" to the field, meaning, timeslots of when the field can be booked by a user.
At least one schedule for the field must be created in order to be visible and available to book.
If for the date, there is no available schedules, the field is not listed.
If there are some bookings for a field related to the club, the booking details are displayed on the club page.
</p>

### Global flow of the standard user:</br>
<p>On the index page, user (logged in or not) can search for a sport (categories, coming from a model). 
Then, user must select a date for which he wants to book a field.
Once the date has been selected, a list of available fields (based on the date, on the sport) is displayed.
When the user selects a field, the available (only available ones) schedules are displayed to this user. 
In order to book a field though, the user must be logged in.
If the user is not logged in, the platform ask him to create a new account, or to login.
For a login user, he can book the field (based on the date, the sport and the schedule) and if that field is still available (server validation as well), the booking is created.
From the profile page, the user can then see all the details of the booking (price, time, date, field, address).
</p>

