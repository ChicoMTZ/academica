from .base import FunctionalTest


credentials = {'username': 'operator', 'password': '123', 'first_name': 'Test_user', 'last_name': 'Last_Name_User',
               'email': 'test_user@gmail.com'}


url_server = 'http://localhost:8000/'


class UserTest(FunctionalTest):
    #Test para probar la creacion de usuario sin permisos
    def test_create_user_without_Admin_permision(self):
        self.create_user_without_permision(**credentials)

    #Test para logear usuarios sin permison
    def test_login_user_without_Admin_permision(self):
        self.login_user_without_permision('operator', 123)

    def test_anonymus_can_nav(self):
        self.anonymus_can_nav()

    def test_user_can_nav(self):
        self.user_can_nav()


