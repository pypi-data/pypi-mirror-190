import os

from service_driver.project_generator import start_project
from service_driver.__main__ import absolute_import

class TestProjectGenerator:
    def test_start_project(self):
        start_project('new_project')
        assert os.path.isdir(os.path.join('new_project', "api_object"))
        assert os.path.isdir(os.path.join('new_project', "testcase"))
