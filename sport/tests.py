from django.test import TestCase
from .models import User, Club, Category, Field, Booking, Schedule


# Create your tests here.
class TestCaseSport(TestCase):
    def setUp(self):
        #create user test
        u1 = User.objects.create(username = 'testcaseautoPro', email = 'testcaseauto@test.com', password='Testcaseauto123!', admin_pro = True)
        u2 = User.objects.create(username = 'testcaseauto', email = 'testcaseautoPro@test.com', password='testcaseautoPro123!', admin_pro = False)

        #create club
        c1 = Club.objects.create(club='club_1', address='Test Street', address_number='1', city = "Montreal", zip_code='H1AH1A', country='CA', image_url='https://images.pexels.com/photos/1619860/pexels-photo-1619860.jpeg?auto=compress&cs=tinysrgb&dpr=3&h=150&w=150', owner_club= u1)
        c2 = Club.objects.create(club='club_2', address='Test Street', address_number='1', city = "Montreal", zip_code='H1AH1A', country='CA', image_url='https://images.pexels.com/photos/1619860/pexels-photo-1619860.jpeg?auto=compress&cs=tinysrgb&dpr=3&h=150&w=150', owner_club= u2)

        #create category
        cat1 = Category.objects.create(category='Tennis',image_url='https://images.pexels.com/photos/1619860/pexels-photo-1619860.jpeg?auto=compress&cs=tinysrgb&dpr=3&h=150&w=150')
        cat2 = Category.objects.create(category='Golf',image_url='https://images.pexels.com/photos/114972/pexels-photo-114972.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=150&w=150')

        #create fields
        f1 = Field.objects.create(field_name="field_1", club = c1, category=cat1, price=15, address='Test Street Field', address_number='1', city = "Montreal", zip_code='H1AH1A', country='CA')
        f2 = Field.objects.create(field_name="field_2", club = c1, category=cat2, price=15, address='Test Street Field', address_number='2', city = "Montreal", zip_code='H1AH1A', country='CA')
        f3 = Field.objects.create(field_name="field_3", club = c1, category=cat1, price=15, address='Test Street Field', address_number='3', city = "Montreal", zip_code='H1AH1A', country='CA')
        f4 = Field.objects.create(field_name="field_4", club = c1, category=cat1, price=15, address='Test Street Field', address_number='4', city = "Montreal", zip_code='H1AH1A', country='CA')

        #create schdules
        s1 = Schedule.objects.create(field=f1, schedule_time='10:00:00')

        s2 = Schedule.objects.create(field=f2, schedule_time='11:00:00')
        s3 = Schedule.objects.create(field=f2, schedule_time='13:00:00')
        s4 = Schedule.objects.create(field=f2, schedule_time='09:00:00')
        s5 = Schedule.objects.create(field=f2, schedule_time='15:00:00')
        s6 = Schedule.objects.create(field=f2, schedule_time='16:00:00')

        s7 = Schedule.objects.create(field=f3, schedule_time='09:00:00')
        s8 = Schedule.objects.create(field=f4, schedule_time='09:00:00')
        s9 = Schedule.objects.create(field=f4, schedule_time='17:00:00')


        #create bookings
        b1 = Booking.objects.create(field=f1, user=u2, date_book='2021-01-01')
        b2 = Booking.objects.create(field=f2, user=u1, date_book='2021-01-01')
        b4 = Booking.objects.create(field=f3, user=u1, date_book='2021-01-01')

        b3 = Booking.objects.create(field=f1, user=u1, date_book='2021-02-01')
        
        b5 = Booking.objects.create(field=f2, user=u1, date_book='2021-05-01')
        b6 = Booking.objects.create(field=f1, user=u2, date_book='2021-05-01')
        b7 = Booking.objects.create(field=f3, user=u2, date_book='2021-05-01')
        b8 = Booking.objects.create(field=f4, user=u1, date_book='2021-05-01')


    #validate the count of bookings
    def test_booking_count(self):
        booking = Booking.objects.all()
        self.assertEqual(booking.count(), 8)

    #validate the count of fields with a specific cat
    def test_fields_cat_count(self):
        fields = Field.objects.filter(category=Category.objects.get(category='Tennis'))
        self.assertEqual(fields.count(), 3)

    #validate the count of bookings for a specific user
    def test_booking_count_2(self):
        booking = Booking.objects.filter(user=User.objects.get(username='testcaseauto'))
        self.assertEqual(booking.count(), 3)

    #validate the number of field with a schedule number >1
    def test_schedule_field(self):
        fields = Field.objects.all()
        fields_sched = [i for i in fields if Schedule.objects.filter(field=i).count() >1]
        self.assertEqual(len(fields_sched), 2)

    #validate that only available fields (based on schedule per day) are returned    
    def test_validation_booking(self):
        self.assertEqual(Booking.validation_booking(self,"2021-01-01"), [Field.objects.get(field_name='field_2'), Field.objects.get(field_name='field_4')])

    def test_validation_booking_2(self):
        list_fields_check = Booking.validation_booking(self,"2021-10-01")
        self.assertEqual(len(list_fields_check), 4)

    def test_validation_booking_3(self):
        list_fields_check = Booking.validation_booking(self,"2021-05-01")
        self.assertEqual(len(list_fields_check), 2)

    #validate only a pro can be a club owner
    def test_valid_owner_club(self):
        c = Club.objects.get(club=Club.objects.get(club='club_1'))
        self.assertTrue(c.is_owner_valid())

    #validate only a pro can be a club owner
    def test_invalid_owner_club_2(self):
        c = Club.objects.get(club=Club.objects.get(club='club_2'))
        self.assertFalse(c.is_owner_valid())
