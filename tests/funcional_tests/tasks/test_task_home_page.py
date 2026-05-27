from selenium.webdriver.common.by import By

from .base import TaskBaseFunctionalTest


class TaskHomePageFunctionalTest(TaskBaseFunctionalTest):
    def test_task_home_page_return_welcome_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, "body")

        self.assertIn(
            "Organize suas tarefas de forma eficiente\ne produtiva.", body.text
        )

    def test_nav_menu_not_shows_if_user_is_not_authenticated(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.CLASS_NAME, "navbar")

        self.assertNotIn("Logout", body.text)
