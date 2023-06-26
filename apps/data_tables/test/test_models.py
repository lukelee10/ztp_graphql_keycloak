import base64
import logging
import os
import os.path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.data_tables.models import DataContent

logging.basicConfig(level=logging.INFO)

PROJ_PATH = os.getcwd()
TEXT_DATA = ["first string", "second string"]
BOOL_TEST_DATA = [False, True]
FLOAT_DATA = [float(21.89), float(88.90)]
IMAGE_PATH = "./media/images/"
TEST_IMG_PATH = "{}/apps/data_tables/test/img/test.png".format(PROJ_PATH)


class TextDataCase(TestCase):
    """test the text data types"""

    def setUp(self):
        """create the data"""
        for item in TEXT_DATA:
            DataContent.objects.create(text_data=item)

    def test_validate_data(self):
        """validation checks"""
        results = DataContent.objects.values_list("text_data", flat=True)
        self.assertIsNotNone(results)
        self.assertEquals(len(results), 2)
        for value in results:
            self.assertTrue(value in TEXT_DATA)


class BoolDataCase(TestCase):
    """boolean type test case"""

    def setUp(self):
        for boolean in BOOL_TEST_DATA:
            DataContent.objects.create(bool_data=boolean)

    def test_validate_data(self):
        results = DataContent.objects.values_list("bool_data", flat=True)
        self.assertEquals(len(results), 2)
        for res in results:
            self.assertTrue(res in BOOL_TEST_DATA)


class FloatDataCase(TestCase):
    """boolean=3 type test case"""

    def setUp(self):
        for num in FLOAT_DATA:
            DataContent.objects.create(float_data=num)

    def test_validate_data(self):
        results = DataContent.objects.values_list("float_data", flat=True)
        self.assertEquals(len(results), 2)
        for res in results:
            self.assertTrue(res in FLOAT_DATA)
