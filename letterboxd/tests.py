from django.test import TestCase
from .models import CustomUser, Review


class ReviewModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.user = CustomUser.objects.create(
			first_name = "Test", 
			last_name = "case", 
			email = "lala@gmail.com",
			username = "testcase",
			password = "password",

			)
		cls.review = Review.objects.create(
			user = cls.user,
			review_body = "this is a body"
			)

	def test_successful_review(self):
		self.asserEqual(self.review.user, self.user)
		self.asserEqual(self.review.review_body, "this is a body" )

	