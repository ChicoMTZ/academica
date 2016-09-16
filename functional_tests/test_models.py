from .util_test import ModelTestHelper
from matricula.models import Period, Category, Course, Student, Group
from django.utils import timezone as datetime
from datetime import timedelta


class MimicModelTest(ModelTestHelper):
    model = Period

    def setUp(self):
        # Mimics require a window
        pass

    def test_saving_and_retrieving_mimic(self):
        periodo_present = {'name': 'Test present', 'start_date': datetime.now(), 'finish_date':datetime.now() + timedelta(days=1)}
        periodo_past = {'name': 'Test past','start_date': datetime.now() + timedelta(days=-360), 'finish_date': datetime.now() + timedelta(days=-2)}

        self.check_saving_and_retrieving_objects(obj1_dict=periodo_present, obj2_dict=periodo_past)