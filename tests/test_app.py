import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json

from tests.base_tests import BaseTestCase
from models.user import User
from utils.extensions import db

class TestApp(BaseTestCase):
    
    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert b"Welsh Academy" in response.data
        assert b"Welsh Academy's API site." in response.data