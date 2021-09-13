from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
import uuid
import datetime
import json
from main.models import User, Notify, Food, Review, Reply, Image, Coupon, Status, Bill, Item

class IndexViewTest(TestCase):
    def setUp(self):
        test_food1 = Food.objects.create(name='Pizza', description='Test food1 description', price=50.0)
        test_food2 = Food.objects.create(name='Sushi', description='Test food2 description', price=100.0)
        test_food3 = Food.objects.create(name='Taco', description='Test food3 description', price=40.0)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_lists_all_foods(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('foods' in response.context)
        self.assertEqual(len(response.context['foods']), 3)
    
    def test_view_search_food(self):
        response = self.client.get(reverse('search'), data={'query': 'sushi pizza'})
        self.assertTrue('keyword' in response.context)
        self.assertTrue('foods' in response.context)
        self.assertEqual(len(response.context['foods']), 2)

class FoodDetailViewTest(TestCase):
    def setUp(self):
        self.test_food = Food.objects.create(name='Test food name', description='Test food description', price=100.0)
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/en-us/food/{self.test_food.pk}/details/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('food-details', kwargs={'id': self.test_food.pk}))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('food-details', kwargs={'id': self.test_food.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foods/details.html')

class RegisterViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/en-us/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
    
    def test_redirect_to_login_on_account_register_success(self):
        response = self.client.post(reverse('register'), data={
            'username': 'test',
            'email': 'test@gmail.com',
            'password1': '1X<ISRUkw+tuK',
            'password2': '1X<ISRUkw+tuK'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

class ReviewFoodViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test', email='test@gmail.com')
        self.test_user.set_password('1X<ISRUkw+tuK')
        self.test_user.save()
        self.test_food = Food.objects.create(name='Test food name', description='Test food description', price=100.0)
    
    def test_review_and_redirect_if_not_logged_in(self):
        response = self.client.post(reverse('review', kwargs={'id': self.test_food.pk}), data={'rating': 5, 'comment': 'Test comment'})
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_review_and_success(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('review', kwargs={'id': self.test_food.pk}), data={'rating': 5, 'comment': 'Test comment'})
        self.assertEqual(response.status_code, 200)

class ReplyCommentViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test', email='test@gmail.com')
        self.test_user.set_password('1X<ISRUkw+tuK')
        self.test_user.save()
        self.test_food = Food.objects.create(name='Test food name', description='Test food description', price=100.0)
        self.test_review = Review.objects.create(rating=5.0, comment='Test comment', user=self.test_user, food=self.test_food)
    
    def test_reply_and_redirect_if_not_logged_in(self):
        response = self.client.post(reverse('reply', kwargs={'food_id': self.test_food.pk, 'review_id': self.test_review.pk}), data={'content': 'Test reply'})
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_reply_and_success(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('reply', kwargs={'food_id': self.test_food.pk, 'review_id': self.test_review.pk}), data={'content': 'Test reply'})
        self.assertEqual(response.status_code, 200)

class DeleteReviewViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test', email='test@gmail.com')
        self.test_user.set_password('1X<ISRUkw+tuK')
        self.test_user.save()
        self.test_food = Food.objects.create(name='Test food name', description='Test food description', price=100.0)
        self.test_review = Review.objects.create(rating=5.0, comment='Test comment', user=self.test_user, food=self.test_food)
    
    def test_delete_review_and_redirect_if_not_logged_in(self):
        response = self.client.delete(reverse('delete-review', kwargs={'id': self.test_review.pk}))
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_delete_review_and_success(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.delete(reverse('delete-review', kwargs={'id': self.test_review.pk}))
        self.assertEqual(response.status_code, 200)

class DeleteReplyViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test', email='test@gmail.com')
        self.test_user.set_password('1X<ISRUkw+tuK')
        self.test_user.save()
        self.test_food = Food.objects.create(name='Test food name', description='Test food description', price=100.0)
        self.test_review = Review.objects.create(rating=5.0, comment='Test comment', user=self.test_user, food=self.test_food)
        self.test_reply = Reply.objects.create(content='Test reply', user=self.test_user, parent=self.test_review)
    
    def test_delete_reply_and_redirect_if_not_logged_in(self):
        response = self.client.delete(reverse('delete-reply', kwargs={'id': self.test_reply.pk}))
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_delete_reply_and_success(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.delete(reverse('delete-reply', kwargs={'id': self.test_reply.pk}))
        self.assertEqual(response.status_code, 200)

class CartViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test', email='test@gmail.com')
        self.test_user.set_password('1X<ISRUkw+tuK')
        self.test_user.save()
        self.test_status, notExist = Status.objects.get_or_create(name='cart')
        self.test_bill, notExist = Bill.objects.get_or_create(user=self.test_user, status=self.test_status)
    
    def test_view_cart_and_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('cart'))
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.get('/en-us/cart/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('cart' in response.context)
        self.assertEqual(response.context['cart'].id, self.test_bill.id)
        self.assertTemplateUsed(response, 'cart/cart.html')

class AddToCartViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test', email='test@gmail.com')
        self.test_user.set_password('1X<ISRUkw+tuK')
        self.test_user.save()
        self.test_food = Food.objects.create(name='Test food name', description='Test food description', price=100.0)
        self.test_status, notExist = Status.objects.get_or_create(name='cart')
        self.test_bill, notExist = Bill.objects.get_or_create(user=self.test_user, status=self.test_status)
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.post(reverse('add-to-cart'), data={'id': self.test_food.id})
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_add_to_cart_and_success(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('add-to-cart'), data={'id': self.test_food.id})
        self.assertEqual(response.status_code, 200)

class RemoveFromCartViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test', email='test@gmail.com')
        self.test_user.set_password('1X<ISRUkw+tuK')
        self.test_user.save()
        self.test_food = Food.objects.create(name='Test food name', description='Test food description', price=100.0)
        self.test_status, notExist = Status.objects.get_or_create(name='cart')
        self.test_bill, notExist = Bill.objects.get_or_create(user=self.test_user, status=self.test_status)
        self.test_item = Item.objects.create(food=self.test_food, bill=self.test_bill, quantity=1, unit_price=self.test_food.price)
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.post(reverse('remove-from-cart', kwargs={'id': self.test_item.pk}))
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_remove_from_cart_and_success(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('remove-from-cart', kwargs={'id': self.test_item.pk}))
        self.assertEqual(response.status_code, 200)

class ProfileViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test', email='test@gmail.com')
        self.test_user.set_password('1X<ISRUkw+tuK')
        self.test_user.save()
    
    def test_view_profile_and_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('profile'))
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.get('/en-us/profile/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

class CheckoutCartViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test', email='test@gmail.com')
        self.test_user.set_password('1X<ISRUkw+tuK')
        self.test_user.save()
        self.test_food = Food.objects.create(name='Test food name', description='Test food description', price=100.0)
        self.test_status, notExist = Status.objects.get_or_create(name='cart')
        self.test_bill, notExist = Bill.objects.get_or_create(user=self.test_user, status=self.test_status)
        self.test_item = Item.objects.create(food=self.test_food, bill=self.test_bill, quantity=1, unit_price=self.test_food.price)
        self.checkoutip = {}
        self.checkoutip[self.test_food.id] = self.test_item.quantity
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.post(reverse('checkout'))
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_checkout_and_success(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('checkout'), data={'checkoutip': json.dumps(self.checkoutip, separators=(',', ':'))})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/checkout.html')

class HandleCheckoutViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test', email='test@gmail.com')
        self.test_user.set_password('1X<ISRUkw+tuK')
        self.test_user.save()
        self.test_food = Food.objects.create(name='Test food name', description='Test food description', price=100.0)
        self.test_status1, notExist = Status.objects.get_or_create(name='cart')
        self.test_status2, notExist = Status.objects.get_or_create(name='processing')
        self.test_bill, notExist = Bill.objects.get_or_create(user=self.test_user, status=self.test_status1)
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.post(reverse('handle-checkout'), data={
            'fprice': 100.0,
            'inputName': 'Repicient',
            'inputPhoneNo': '123456789',
            'inputAddress': '123 Main Street',
            'inputCity': 'Hanoi',
            'inputCountry': 'Vietnam',
            'inputZip': '1111',
            'inputShipNote': 'Test bill shipping note',
        })
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_handle_checkout_and_success(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('handle-checkout'), data={
            'fprice': 100.0,
            'inputName': 'Repicient',
            'inputPhoneNo': '123456789',
            'inputAddress': '123 Main Street',
            'inputCity': 'Hanoi',
            'inputCountry': 'Vietnam',
            'inputZip': '1111',
            'inputShipNote': 'Test bill shipping note',
        })
        self.assertEqual(response.status_code, 200)

class CancelOrderViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test', email='test@gmail.com')
        self.test_user.set_password('1X<ISRUkw+tuK')
        self.test_user.save()
        self.test_food = Food.objects.create(name='Test food name', description='Test food description', price=100.0)
        self.test_status, notExist = Status.objects.get_or_create(name='processing')
        self.test_bill, notExist = Bill.objects.get_or_create(user=self.test_user, status=self.test_status)
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.post(reverse('cancel-order'), data={'uuid': self.test_bill.id})
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_cancel_order_and_success(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('cancel-order'), data={'uuid': self.test_bill.id})
        self.assertEqual(response.status_code, 200)

class WishListViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test', email='test@gmail.com')
        self.test_user.set_password('1X<ISRUkw+tuK')
        self.test_user.save()
        self.test_food = Food.objects.create(name='Test food name', description='Test food description', price=100.0)
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.post(reverse('wishlist'))
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_view_wishlist_success_and_use_correct_template(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/wishlist.html')

class AddToWishListViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test', email='test@gmail.com')
        self.test_user.set_password('1X<ISRUkw+tuK')
        self.test_user.save()
        self.test_food = Food.objects.create(name='Test food name', description='Test food description', price=100.0)
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.post(reverse('add-to-wishlist'), data={'food_id': self.test_food.pk})
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_add_to_wishlist_and_success(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('add-to-wishlist'), data={'food_id': self.test_food.pk})
        self.assertEqual(response.status_code, 200)

class RemoveFromWishListViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='test', email='test@gmail.com')
        self.test_user.set_password('1X<ISRUkw+tuK')
        self.test_user.save()
        self.test_food = Food.objects.create(name='Test food name', description='Test food description', price=100.0)
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.post(reverse('remove-from-wishlist', kwargs={'id': self.test_food.pk}))
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_remove_from_wishlist_and_success(self):
        login = self.client.login(email=self.test_user.email, password='1X<ISRUkw+tuK')
        response = self.client.delete(reverse('remove-from-wishlist', kwargs={'id': self.test_food.pk}))
        self.assertEqual(response.status_code, 200)
