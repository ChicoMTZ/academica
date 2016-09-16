from .base import FunctionalTest
credentials = {'username': 'jacob', 'password': 'password', 'first_name': 'Test_user', 'last_name': 'Last_Name_User',
               'email': 'test_user@gmail.com'}


class UserTest(FunctionalTest):

    def test_create_user_without_Admin_permision(self):
        self.create_user_without_permision(**credentials)

    def test_login_user_without_Admin_permision(self):
        self.login_user_without_permision('Admin', 'chicomtz')

    def test_anonymus_can_nav(self):
        self.anonymus_can_nav()

    def test_user_can_nav(self):
        self.create_user_without_permision(**credentials)
        self.user_can_nav()


