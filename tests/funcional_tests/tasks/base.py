from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from utils.browser import make_browser


class TaskBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = make_browser()
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()
