from django.test import TestCase
from django.core.exceptions import ValidationError
import datetime
import uuid
from main.models import User, Notify, Food, Review, Reply, Image, Coupon, Status, Bill, Item

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user_id = User.objects.create(
            email='test@gmail.com',
            phone_number='123456789',
            address='123 Main Street',
            city='Hanoi',
            country='Vietnam',
            zip_code='1111',
            first_name='Big',
            last_name='Bob'
        ).pk

    def test_first_name_label(self):
        test_user = User.objects.get(id=self.user_id)
        field_label = test_user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        test_user = User.objects.get(id=self.user_id)
        field_label = test_user._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_object_name_is_last_name_comma_first_name(self):
        test_user = User.objects.get(id=self.user_id)
        expected_object_name = f'{test_user.last_name} {test_user.first_name}' 
        self.assertEqual(str(test_user), expected_object_name)
    
    def test_email_max_length_and_unique(self):
        test_user = User.objects.get(id=self.user_id)
        max_length = test_user._meta.get_field('email').max_length
        unique = test_user._meta.get_field('email').unique
        self.assertEqual(max_length, 255)
        self.assertEqual(unique, True)
    
    def test_phone_number_max_length(self):
        test_user = User.objects.get(id=self.user_id)
        max_length = test_user._meta.get_field('phone_number').max_length
        self.assertEqual(max_length, 12)
    
    def test_address_max_length(self):
        test_user = User.objects.get(id=self.user_id)
        max_length = test_user._meta.get_field('address').max_length
        self.assertEqual(max_length, 255)
    
    def test_city_max_length(self):
        test_user = User.objects.get(id=self.user_id)
        max_length = test_user._meta.get_field('city').max_length
        self.assertEqual(max_length, 100)
    
    def test_country_max_length(self):
        test_user = User.objects.get(id=self.user_id)
        max_length = test_user._meta.get_field('country').max_length
        self.assertEqual(max_length, 100)
    
    def test_zip_code_max_length(self):
        test_user = User.objects.get(id=self.user_id)
        max_length = test_user._meta.get_field('zip_code').max_length
        self.assertEqual(max_length, 100)
        
class NotifyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.notify_id = Notify.objects.create(message='Test notify message').pk
    
    def test_is_active_default_value(self):
        test_notify = Notify.objects.get(id=self.notify_id)
        self.assertEqual(test_notify.is_active, True)

class FoodModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.food_id = Food.objects.create(
            name='Test food name',
            description='Test food description',
            price=100.0
        ).pk
    
    def test_food_name_max_length(self):
        test_food = Food.objects.get(id=self.food_id)
        max_length = test_food._meta.get_field('name').max_length
        self.assertEqual(max_length, 45)
    
    def test_order_count_default_value(self):
        test_food = Food.objects.get(id=self.food_id)
        self.assertEqual(test_food.order_count, 0)
    
    def test_object_name_is_food_name(self):
        test_food = Food.objects.get(id=self.food_id)
        self.assertEqual(str(test_food), test_food.name)
    
        
class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(email='test@gmail.com', username='testuser', password='1X<ISRUkw+tuK')
        test_food = Food.objects.create(name='test food', price=100.0)
        cls.review_id = Review.objects.create(comment='Test comment', rating=6, user=test_user, food=test_food).pk
    
    def test_rating_is_valid(self):
        with self.assertRaises(ValidationError):
            test_review = Review.objects.get(id=self.review_id)
            test_review.full_clean()
    
class ReplyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(email='test@gmail.com', username='testuser', password='1X<ISRUkw+tuK')
        test_food = Food.objects.create(name='test food', price=100.0)
        test_review = Review.objects.create(comment='Test comment', rating=6, user=test_user, food=test_food)
        cls.reply_id = Reply.objects.create(user=test_user, parent=test_review, content='Test reply content').pk
    
    def test_content_is_succesfully_generated(self):
        test_reply = Reply.objects.get(id=self.reply_id)
        self.assertEqual(test_reply.content, 'Test reply content')
        
class ImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_food = Food.objects.create(name='test food', price=100.0)
        cls.image_id = Image.objects.create(food=test_food, url='/static/img/default.jpeg').pk
    
    def test_url_max_length(self):
        test_image = Image.objects.get(id=self.image_id)
        max_length = test_image._meta.get_field('url').max_length
        self.assertEqual(max_length, 255)
    
    def test_object_name_return_image_url(self):
        test_image = Image.objects.get(id=self.image_id)
        self.assertEqual(str(test_image), test_image.url)
        
class CouponModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.coupon_id = Coupon.objects.create(code='SALE50K', value=50.0, start=datetime.date.today()).pk
    
    def test_code_max_length(self):
        test_coupon = Coupon.objects.get(id=self.coupon_id)
        max_length = test_coupon._meta.get_field('code').max_length
        self.assertEqual(max_length, 50)
    
    def test_coupon_is_active(self):
        test_coupon = Coupon.objects.get(id=self.coupon_id)
        self.assertEqual(test_coupon.is_active, True)
    
    def test_object_name_is_code(self):
        test_coupon = Coupon.objects.get(id=self.coupon_id)
        self.assertEqual(str(test_coupon), test_coupon.code)
        
class StatusModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.status_id = Status.objects.create(name='processing', description='Order succesfully but not paid yet').pk
    
    def test_status_max_length(self):
        test_status = Status.objects.get(id=self.status_id)
        max_length = test_status._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)
    
    def test_description_max_length(self):
        test_status = Status.objects.get(id=self.status_id)
        max_length = test_status._meta.get_field('description').max_length
        self.assertEqual(max_length, 255)
    
    def test_object_name_is_code(self):
        test_status = Status.objects.get(id=self.status_id)
        self.assertEqual(str(test_status), test_status.name)
        
class BillModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(email='test@gmail.com', username='testuser', password='1X<ISRUkw+tuK')
        test_coupon = Coupon.objects.create(code='SALE50K', value=50.0, start=datetime.date.today())
        test_status = Status.objects.create(name='processing', description='Order succesfully but not paid yet')
        cls.bill_id = Bill.objects.create(
            total=200.0,
            recipient='Test bill recipient',
            phone_number='123456789',
            address='123 Main Street',
            city='Hanoi',
            country='Vietnam',
            zip_code='1111',
            shipping_note='Test bill shipping note',
            user=test_user,
            coupon=test_coupon,
            status=test_status
        ).pk
    
    def test_recipient_max_length(self):
        test_bill = Bill.objects.get(id=self.bill_id)
        max_length = test_bill._meta.get_field('recipient').max_length
        self.assertEqual(max_length, 50)
    
    def test_phone_number_max_length(self):
        test_bill = Bill.objects.get(id=self.bill_id)
        max_length = test_bill._meta.get_field('phone_number').max_length
        self.assertEqual(max_length, 12)
    
    def test_address_max_length(self):
        test_bill = Bill.objects.get(id=self.bill_id)
        max_length = test_bill._meta.get_field('address').max_length
        self.assertEqual(max_length, 255)
    
    def test_city_max_length(self):
        test_bill = Bill.objects.get(id=self.bill_id)
        max_length = test_bill._meta.get_field('city').max_length
        self.assertEqual(max_length, 100)
    
    def test_country_max_length(self):
        test_bill = Bill.objects.get(id=self.bill_id)
        max_length = test_bill._meta.get_field('country').max_length
        self.assertEqual(max_length, 100)
    
    def test_zip_code_max_length(self):
        test_bill = Bill.objects.get(id=self.bill_id)
        max_length = test_bill._meta.get_field('zip_code').max_length
        self.assertEqual(max_length, 100)
    
    def test_delivery_charges_is_default_to_zero(self):
        test_bill = Bill.objects.get(id=self.bill_id)
        self.assertEqual(test_bill.delivery_charges, 0)
    
    def test_object_name_is_bill_id(self):
        test_bill = Bill.objects.get(id=self.bill_id)
        self.assertEqual(str(test_bill), str(test_bill.id))

class ItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(email='test@gmail.com', username='testuser', password='1X<ISRUkw+tuK')
        test_food1 = Food.objects.create(name='test food 1', price=100.0)
        test_food2 = Food.objects.create(name='test food 2', price=50.0)
        test_bill = Bill.objects.create(recipient='Test bill recipient', phone_number='123456789', address='123 Main Street', user=test_user)
        test_item1 = Item.objects.create(unit_price=100.0, quantity=2, food=test_food1, bill=test_bill)
        test_item2 = Item.objects.create(unit_price=50.0, quantity=3, food=test_food2, bill=test_bill)
        test_bill.total = test_item1.unit_price * test_item1.quantity + test_item2.unit_price * test_item2.quantity
        test_bill.save()
        cls.test_item1_id = test_item1.pk
        cls.test_item2_id = test_item2.pk
        cls.test_bill_id = test_bill.pk
    
    def test_bill_total_is_saved(self):
        test_item1 = Item.objects.get(id=self.test_item1_id)
        test_item2 = Item.objects.get(id=self.test_item2_id)
        test_bill = Bill.objects.get(id=self.test_bill_id)
        expected_bill_total = test_item1.unit_price * test_item1.quantity + test_item2.unit_price * test_item2.quantity
        self.assertEqual(test_bill.total, expected_bill_total)
