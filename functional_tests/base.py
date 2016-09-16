# encoding: utf-8
from matricula.models import Period, Category, Course, Student, Group
from datetime import timedelta
from django.utils import timezone as datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from selenium.webdriver.firefox.webdriver import WebDriver
import sys
from django.test import Client
from django.core.urlresolvers import reverse
User = get_user_model()


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return

        super(FunctionalTest, cls).setUpClass()
        cls.server_url = cls.live_server_url
        cls.selenium = WebDriver()
        cls.selenium.maximize_window()
        cls.selenium.implicitly_wait(5)

        cls.period_present = Period.objects.create(
                    name="Test present",
                    start_date=datetime.now(),
                    finish_date=datetime.now() + timedelta(days=1),
                    )

        cls.period_past = Period.objects.create(
                    name="Test past",
                    start_date=datetime.now() + timedelta(days=-360),
                    finish_date=datetime.now() + timedelta(days=-2),
                    )
        cls.period_future = Period.objects.create(
                    name="Test future",
                    start_date=datetime.now() + timedelta(days=1),
                    finish_date=datetime.now() + timedelta(days=2),
                    )
        cls.categorias = [
                Category.objects.create(name="Cat 1", description="Description 1"),
                Category.objects.create(name="Cat 2", description="Description 2"),
                Category.objects.create(name="Cat 3", description="Description 3")
                          ]

        cls.courses = [
            Course.objects.create(category=cls.categorias[0],
                                   name="Course 1",
                                   content="Contenido del Curso I"),
            Course.objects.create(category=cls.categorias[1],
                                   name="Course 2",
                                   content="Contenido del Curso II"),
            Course.objects.create(category=cls.categorias[0],
                                   name="Course 3",
                                   content="Contenido del Curso III"),
            Course.objects.create(category=cls.categorias[2],
                                   name="Course 4",
                                   content="Contenido del Curso IV"),
                        ]
        cls.groups = [
            Group.objects.create(
                        period=cls.period_present,
                        course=cls.courses[0],
                        name="G 01",
                        schedule="N/D",
                        pre_enroll_start=datetime.now(),
                        pre_enroll_finish=datetime.now() + timedelta(days=1),
                        enroll_start=datetime.now(),
                        enroll_finish=datetime.now() + timedelta(days=1),
                        cost=10.0, maximum=10),

            Group.objects.create(
                        period=cls.period_past,
                        course=cls.courses[0],
                        name="G 02",
                        schedule="N/D",
                        pre_enroll_start=datetime.now(),
                        pre_enroll_finish=datetime.now() + timedelta(days=1),
                        enroll_start=datetime.now(),
                        enroll_finish=datetime.now() + timedelta(days=1),

                        cost=10.0, maximum=10),
            Group.objects.create(
                        period=cls.period_present,
                        course=cls.courses[1],
                        name="G 03",
                        schedule="N/D",
                        pre_enroll_start=datetime.now() + timedelta(days=-2),
                        pre_enroll_finish=datetime.now() + timedelta(days=-1),
                        enroll_start=datetime.now(),
                        enroll_finish=datetime.now() + timedelta(days=1),
                        cost=10.0, maximum=10),

                       ]

        cls.users = [
                      Student.objects.create_user(username='Admin',
                                                  email='jacob@…',
                                                  password='chicomtz'),
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

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(FunctionalTest, cls).tearDownClass()

    def create_user_without_permision(self, **credentials):
        user = User.objects.create_user(**credentials)

    def login_user_without_permision(self, username, password):
        self.selenium.get('http://localhost:8000/')

        btn_signin = self.get_signin_button()
        self.assertTrue(btn_signin.is_displayed())
        btn_signin.click()
        input_user = self.selenium.find_element_by_name('username')
        input_user.send_keys(username)
        input_pass = self.selenium.find_element_by_name('password')
        input_pass.send_keys(password)
        btn_login = self.selenium.find_element_by_name('Login')
        btn_login.click()

    def anonymus_can_nav(self):
        self.selenium.get('%s' % self.server_url)
        menu_list = self.selenium.find_element_by_id('menu')
        self.assertTrue(menu_list)
        self.selenium.find_element_by_css_selector('ul li a')
        table = self.selenium.find_element_by_class_name('table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any('Groups' in row.text for row in rows)
        )
        self.selenium.find_element_by_name('Curso').click()
        self.selenium.find_element_by_class_name('navbar-brand').click()
        self.selenium.find_element_by_name('Read').click()

    def user_can_nav(self):
        self.login_user_without_permision('Admin', 'chicomtz')
        table = self.selenium.find_element_by_id('menu')
        testo = table.find_elements_by_tag_name('li')

        self.assertTrue(
            any('Cursos' in row.text for row in testo)
        )

    def get_signin_button(self):
        return self.selenium.find_element_by_name('Sign in')

    def get_sigup_button(self):
        return self.selenium.find_element_by_name('Sign up')
