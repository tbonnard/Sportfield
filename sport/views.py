from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import json
from operator import attrgetter
from datetime import datetime



from .forms import ClubForm, FieldForm
from .models import User, Club, Category, Field, Booking, Schedule


# Create your views here.


def error(request):
    return render(request,'sport/error.html')



def index(request):
    """Index page listing all the categories (sport) for user/non user

    Args:
        request: user request - calling url index

    Returns:
        render : index template
        categories: list of all categories
    """
    categories = Category.objects.all()
    if request.user.is_authenticated:
        return render(request, 'sport/index.html', {'categories': categories})
    return render(request, 'sport/index.html', {'categories': categories, 'message':'login'})


def login_view(request):
    # to avoid logged in user can access the page
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "sport/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "sport/login.html")



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    # to avoid logged in user can access the page
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        pro = request.POST.get("pro", False)
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirm_password"]
        if (password != confirmation) :
            return render(request, "sport/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            if pro == 'on':
                user = User.objects.create_user(username, email, password, admin_pro = True)
            else:
                user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "sport/register.html", {
                "message": "Email address already taken."
            })
        except ValueError:
            return render(request, "sport/register.html", {
                "message": "You must enter correct data"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "sport/register.html")


def profile(request):
    return HttpResponseRedirect(reverse("index"))

def profile_id(request, profile_id):
    """Profile page listing user details + booking infos + clubs.
    Validation on user id is performed to make sure the user exists and request.user can see the page

    Args:
        request: user request - calling profile_id url
        profile_id [int: id of the user]: id of the user

    Returns:
        render: profile_id template
        user: all details of the user
        bookings: list of bookings of the user (if any)
        clubs: info about the club the user owns (if any) 
    """
    try:
        User.objects.get(pk=profile_id)
    except:
        return HttpResponseRedirect(reverse("index"))
    if request.user.is_authenticated:
        booking = Booking.objects.filter(user=request.user)
        #sort by booking date - most recent at the top
        bookings = sorted(booking, key = attrgetter('date_book'))[::-1]
        return render(request, "sport/profile.html", {"user":request.user, 'bookings':bookings, 'clubs': Club.objects.filter(owner_club=request.user)})
    return HttpResponseRedirect(reverse("index"))



def create_club(request):
    """create_club view allowing the user to create a new club, if authentified

    Args:
        request: user request - calling create_club url

    Returns:
        form: Render a form to create a club
        Create the club (if valid)
        Redirect to field page (refer to views.club_id) if valid
        If problem, render back the form on the page
    """
    if request.user.is_authenticated:
        form = ClubForm(initial={'owner_club':request.user})
        if request.method == "POST":
            form = ClubForm(request.POST)
            if form.is_valid():
                club = form.cleaned_data['club'].title()
                address =  form.cleaned_data['address']
                address_number =  form.cleaned_data['address_number']
                city =  form.cleaned_data['city']
                zip_code =  form.cleaned_data['zip_code']
                country =  form.cleaned_data['country']
                image_url =  form.cleaned_data['image_url']
                new_club = Club.objects.create(club=club, address=address, address_number=address_number, city=city, zip_code=zip_code, country=country, image_url=image_url, owner_club=request.user)
                new_club.save()              
                return redirect("club_id", new_club.pk)
            return render(request, "sport/create_club.html", {'form': form})
        return render(request, "sport/create_club.html", {'form': form})
    return HttpResponseRedirect(reverse("index"))



def field_display(request, club_id):
    """function to create the initial form to create a field

    Args:
        request  user request - calling that function
        club_id [int: id of the club ]: id of the club 

    Returns:
        field_form: objects of the list matching the query
    """
    try:
        Club.objects.get(pk=club_id)
    except:
        return HttpResponseRedirect(reverse("index"))
    club =  Club.objects.get(pk=club_id)
    field_form = FieldForm(initial={'club': club, 'address': club.address, 'address_number': club.address_number, 'country': club.country, 'zip_code': club.zip_code, 'city':club.city})
    return field_form



def booking_list_club(request,club_id):
    """function to provide a list of bookings for a club_id

    Args:
        request  user request - calling that function
        club_id [int: id of the club ]: id of the club 

    Returns:
        bookings: objects of the list matching the query, booking, sorted by most recent booking date at the top
    """
    try:
        Club.objects.get(pk=club_id)
    except:
        return HttpResponseRedirect(reverse("index"))
    fields = Field.objects.filter(club=club_id)
    booking = Booking.objects.all()
    list_bookings = [i for i in booking if i.field in fields ]  
    #sort by booking date - most recent at the top
    bookings = sorted(list_bookings, key = attrgetter('date_book'))[::-1]
    return bookings



def club_id(request, club_id):
    """club page of the user containing all infos about the clubs, the fields of the club and the booking details about the fields of the club.
    Validation on club id is performed to make sure the club exists

    Args:
        request: user request - calling club_id url
        club_id [int: id of the club ]: id of the club 

    Returns:
        Render the page to view details of the club, fields, booking
        field_form: Render a form to create a field (refer to views.create_field). Form is pre-populated as for some, user can not edit them.
        club: render club details (if any)
        fields: render fields details of the club (if any)
        bookings: render details about the bookings for the fields of the club (if any)
    """
    try:
        Club.objects.get(pk=club_id)
    except:
        return HttpResponseRedirect(reverse("index"))
    if request.user.is_authenticated and Club.objects.get(pk=club_id).owner_club == request.user:
        fields = Field.objects.filter(club=club_id)
        club = Club.objects.get(pk=club_id)
        address = club.address
        address_number = club.address_number
        country = club.country
        zip_code = club.zip_code
        city = club.city
        return render(request, "sport/club.html", {'club': club, 'field_form': field_display(request,club_id), 'fields': fields, 'bookings':booking_list_club(request,club_id)})
    return HttpResponseRedirect(reverse("index"))


#Without JS fetch
def create_field(request, club_id):
    """Function allowing to create a new field for a club.
    Validation on club id is performed to make sure the club exists.
    FYI: Request made by JS call for now that calls that function.

    Args:
        request: user request - calling create_field url
        club_id [int: id of the club ]: id of the club

    Returns:
        redirect to the field page, page on which the user can add a new schedule to the field (refer to views.field_view)
        club = club details of the user
        fields = fields info of the club of the user
        field_form = form 
    """
    try:
        Club.objects.get(pk=club_id)
    except:
        return HttpResponseRedirect(reverse("index"))
    if request.user.is_authenticated:
        if Club.objects.get(pk=club_id).owner_club == request.user:
            fields = Field.objects.filter(club=club_id)
            club = Club.objects.get(pk=club_id)
            form = FieldForm()
            if request.method == "POST":
                form = FieldForm(request.POST)
                if form.is_valid():
                    name =  form.cleaned_data['field_name'].title()
                    category =  form.cleaned_data['category']
                    price = form.cleaned_data['price']
                    address =  form.cleaned_data['address']
                    address_number =  form.cleaned_data['address_number']
                    city =  form.cleaned_data['city']
                    zip_code =  form.cleaned_data['zip_code']
                    country =  form.cleaned_data['country']
                    full_name = f"{name} - {club}"
                    new_field = Field(field_name = full_name, club = club, category=category, address_number=address_number, address=address, zip_code=zip_code, country=country, city=city, price=price)
                    new_field.save()    
                    return HttpResponseRedirect(reverse("field_view", args=[new_field.id]))
                return render(request, "sport/club.html", {'club': club, 'fields': fields, 'field_form': form})
            return HttpResponseRedirect(reverse("club_id", args=[club_id]))
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("index"))



#JS call
def booking(request):
    """Function allowing to create a new booking record
    JS fetch API
 
    Args:
        request: user request - calling create_field url

    Returns:
        Return a json response: "OK" if booking created
    """
    if request.user.is_authenticated:
        if request.method =="POST":
            data = json.loads(request.body)
            field_json = data.get("field")
            date = data.get("date")
            time = data.get("time")
            try:
                field = Field.objects.get(pk=field_json)
            except:
                return JsonResponse({"Field": "Field not found."}, status=404)
            time_field = [i.schedule_time_field for i in Booking.objects.filter(field=field, date_book=date) if str(i.schedule_time_field) == str(time)]
            if len(time_field) == 0:
                new_booking = Booking(field = field, user=request.user, date_book=date, schedule_time_field=time)
                new_booking.save()
                return JsonResponse({"message": 'OK'}, status=201)
            return JsonResponse({"error": "schedule not available anymore"}, status=400)
        return JsonResponse({"error": "POST request required."}, status=400)
    return HttpResponseRedirect(reverse("error"))
        

#JS call
def get_fields(request, category_id, date):
    """Function allowing to see the available fields based on the category and the date
    JS get call

    Args:
        request: user request - calling create_field url
        category_id [int: id of the category ]: id of the category the user wants to look for
        date [date : YYYY-MM-DD]: date of the field booked

    Returns:
        return a list of fields (objects - serialized json) matching the query: if schedule available for the date
    """
    try:
        category = Category.objects.get(pk=category_id)
    except :
        return HttpResponseRedirect(reverse("error"))
    if request.method == "GET":
        fields = Field.objects.filter(category=category)
        booking = Booking.objects.all()
        list_fields = [i for i in fields if len(Booking.objects.filter(field=i, date_book=date)) < Schedule.objects.filter(field=i).count() ]
        return JsonResponse([field.serialize() for field in list_fields], safe=False)
    else:
        return HttpResponseRedirect(reverse("error"))




#JS call
def get_schedule(request,field_id, date):
    """Function allowing to see the available schedule based on the field and the date
    JS get call

    Args:
        request ([type]): [description]
        field_id [int: id of the field ]: id of the field to display data about the field and allow owner to see available schedules
        date [date : YYYY-MM-DD]: date of the field booked

    Returns:
        return a list of schedule (objects - serialized json) matching the query: if schedule available for the date
    """
    try:
        field = Field.objects.get(pk=field_id)
    except:
        return HttpResponseRedirect(reverse("error"))
    if request.method == "GET":
        schedule_field = [i.schedule_time_field for i in Booking.objects.filter(field=field, date_book=date)]
        schedules = [i for i in Schedule.objects.filter(field=field) if i.schedule_time not in schedule_field]
        return JsonResponse([schedule.serialize() for schedule in schedules], safe=False)
    else:
        return HttpResponseRedirect(reverse("error"))


def field_view(request, field_id):
    """Render the field view and allow a club owner to add a new schedule to the field

    Args:
        request: user request - calling field url
        field_id [int: id of the field ]: id of the field to display data about the field and allow owner to add a schedule

    Returns:
        redirect to the field page, page on which the user can see field schedule and create a schedule for the field
        schedule: all the current schedules for that field
    """
    try:
        field = Field.objects.get(pk=field_id)
    except:
        return HttpResponseRedirect(reverse("error"))
    #only club's owner can access the field
    if request.user == field.club.owner_club:
        schedule = Schedule.objects.filter(field=field)
        if request.method == "POST":
            time = f"{request.POST['time']}:00"
            time_ob = datetime.strptime(time, '%H:%M:%S').time
            time_validation = [i.schedule_time for i in schedule if i.schedule_time.strftime("%H:%M:%S") == time]
            if len(time_validation) == 0 :
                new_schedule = Schedule(field=field, schedule_time=time)
                new_schedule.save()
            return render(request,'sport/field.html', {'field':field, 'schedule':Schedule.objects.filter(field=field)})
        return render(request,'sport/field.html', {'field':field, 'schedule':schedule})
    return HttpResponseRedirect(reverse("index"))

