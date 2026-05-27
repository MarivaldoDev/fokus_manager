from django.urls import resolve, reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .base import AuthorsBaseFuncionalTest


class AuthorsLoginFormFunctionalTest(AuthorsBaseFuncionalTest):
    def test_show_message_error_if_form_is_not_valid(self):
        self.browser.get(self.live_server_url + "/authors/login/")

        user = self.browser.find_element(By.ID, "id_username")
        password = self.browser.find_element(By.ID, "id_password")

        user.send_keys("invalid_user")
        password.send_keys("12345")
        password.send_keys(Keys.ENTER)

        message_erro = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert"))
        )

        self.assertIn(
            "Por favor, entre com um usuário e senha corretos. Note que ambos os campos diferenciam maiúsculas e minúsculas.",
            message_erro.text,
        )

    def test_load_tasks_if_login_form_is_valid(self):
        self.browser.get(self.live_server_url + "/authors/login/")

        user = self.browser.find_element(By.ID, "id_username")
        password = self.browser.find_element(By.ID, "id_password")

        user.send_keys("mariva")
        password.send_keys("1234")
        password.send_keys(Keys.ENTER)

        response = resolve(reverse("tasks:tasks"))

        self.assertEqual(response.url_name, "tasks")
