# encoding: utf-8
from django.test import RequestFactory
from matricula.models import Period, Category, Course, Student, Group
from datetime import timedelta
from django.utils import timezone as datetime
from django.core.urlresolvers import resolve
from matricula.views import index
from django.contrib.auth import get_user_model
from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import TestCase
import time
User = get_user_model()
url_server = 'http://localhost:8000/'


#En este archivo creo todas las funciones base de todos los test, los demas test heredaran todos de
# este con el con el fin de obtener tambien sus metodos.

class FunctionalTest(TestCase):

    def setUp(self):

        self.browser = WebDriver()
        #Maximizo la ventana pork si no esta maximizada no se le presenta al usuario la opcion de logearse
        self.browser.set_window_size(1024,760)
        self.browser.implicitly_wait(3)

        self.factory = RequestFactory()
        #Prueba la creacion de distintos objetos en la BD y los mantiene en todas las pruebas que haga
        self.period_present = Period.objects.create(
                    name="Test present",
                    start_date=datetime.now(),
                    finish_date=datetime.now() + timedelta(days=1),
                    )

        self.period_past = Period.objects.create(
                    name="Test past",
                    start_date=datetime.now() + timedelta(days=-360),
                    finish_date=datetime.now() + timedelta(days=-2),
                    )
        self.period_future = Period.objects.create(
                    name="Test future",
                    start_date=datetime.now() + timedelta(days=1),
                    finish_date=datetime.now() + timedelta(days=2),
                    )
        self.categorias = [
                Category.objects.create(name="Cat 1", description="Description 1"),
                Category.objects.create(name="Cat 2", description="Description 2"),
                Category.objects.create(name="Cat 3", description="Description 3") 
                          ]

        self.courses = [
            Course.objects.create(category=self.categorias[0],
                                   name="Course 1",
                                   content=""),
            Course.objects.create(category=self.categorias[1],
                                   name="Course 2",
                                   content=""),
            Course.objects.create(category=self.categorias[0],
                                   name="Course 3",
                                   content=""),
            Course.objects.create(category=self.categorias[2],
                                   name="Course 4",
                                   content=""),
                        ]
        self.groups = [
            Group.objects.create(
                        period=self.period_present,
                        course=self.courses[0],
                        name="G 01",
                        schedule="N/D",
                        pre_enroll_start=datetime.now(),
                        pre_enroll_finish=datetime.now() + timedelta(days=1),
                        enroll_start=datetime.now(),
                        enroll_finish=datetime.now() + timedelta(days=1),
                        cost=10.0, maximum=10),
            Group.objects.create(
                        period=self.period_past,
                        course=self.courses[0],
                        name="G 02",
                        schedule="N/D",
                        pre_enroll_start=datetime.now(),
                        pre_enroll_finish=datetime.now() + timedelta(days=1),
                        enroll_start=datetime.now(),
                        enroll_finish=datetime.now() + timedelta(days=1),
                        cost=10.0, maximum=10),
            Group.objects.create(
                        period=self.period_present,
                        course=self.courses[1],
                        name="G 03",
                        schedule="N/D",
                        pre_enroll_start=datetime.now() + timedelta(days=-2),
                        pre_enroll_finish=datetime.now() + timedelta(days=-1),
                        enroll_start=datetime.now(),
                        enroll_finish=datetime.now() + timedelta(days=1),
                        cost=10.0, maximum=10),

                       ]

        self.users = [
                      Student.objects.create_user(username='jacob',
                                                  email='jacob@…',
                                                  password='password'),
                      Student.objects.create_user(username='jacob1',
                                                  email='jacob1@…',
                                                  password='password'),
                      Student.objects.create_user(username='jacob2',
                                                  email='jacob2@…',
                                                  password='password'),
                      Student.objects.create_user(username='jacob3',
                                                  email='jacob3@…',
                                                 password='password'),
                      ]

        self.assertTrue(self.client.get('matricula/course'))

    #Funcion que crea un usuario

    def create_user_without_permision(self, **credentials):
        user = User.objects.create_user(**credentials)



    #Funcion que logea un usuario

    def login_user_without_permision(self, username, password):
        self.browser.get(url_server)

        btn_signin = self.get_signin_button()
        self.assertTrue(btn_signin.is_displayed())
        btn_signin.click()
        input_user = self.browser.find_element_by_name('username')
        input_user.send_keys(username)
        input_pass = self.browser.find_element_by_name('password')
        input_pass.send_keys(password)
        btn_login = self.browser.find_element_by_name('Login')
        btn_login.click()

    def user_can_nav(self):
        self.browser.get(url_server)
        menu_list = self.browser.find_element_by_id('menu')
        self.assertTrue(menu_list)
        self.browser.find_element_by_css_selector('ul li a')
        table = self.browser.find_element_by_class_name('table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any('Groups' in row.text for row in rows)
        )
        

    #Funcion que obtiene el boton de login

    def get_signin_button(self):
        return self.browser.find_element_by_name('Sign in')

    #Funcion que obtiene el boton de sign up

    def get_sigup_button(self):
        return self.browser.find_element_by_name('Sign up')

    def tearDown(self):
        self.browser.quit()
