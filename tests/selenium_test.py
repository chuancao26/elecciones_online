from selenium.webdriver.common.by import By
import time

REGISTER_URL = "http://localhost:4321/register"
LOGIN_URL = "http://localhost:4321/login"
DATE_OF_BIRTH = "10/09/2000"
HOME_URL = "http://localhost:4321/home"

class TestRegisterPage:
    def test_invalid_register(self, driver):
        driver.get(REGISTER_URL)

        driver.find_element(By.ID, "name").send_keys("Crishtian")
        driver.find_element(By.ID, "paternalName").send_keys("Jose")
        driver.find_element(By.ID, "maternalName").send_keys("Maria")
        driver.find_element(By.ID, "date-of-birth").send_keys(DATE_OF_BIRTH)
        driver.find_element(By.ID, "user").send_keys("cdho2jjjjj")
        driver.find_element(By.ID, "email").send_keys("asdqwewqeq12@gmail.com")
        driver.find_element(By.ID, "password").send_keys("123456")

        driver.find_element(By.ID, "form-register").submit()
        time.sleep(2)
        current_url = driver.current_url
        assert current_url == REGISTER_URL

    def test_duplicated_elector(self, driver):
        driver.get(REGISTER_URL)

        driver.find_element(By.ID, "name").send_keys("Crishtian")
        driver.find_element(By.ID, "paternalName").send_keys("Jose")
        driver.find_element(By.ID, "maternalName").send_keys("Maria")
        driver.find_element(By.ID, "date-of-birth").send_keys("10/09/2000")
        driver.find_element(By.ID, "user").send_keys("juanco")
        driver.find_element(By.ID, "email").send_keys("juanco@gmail.com")
        driver.find_element(By.ID, "password").send_keys("123456")

        driver.find_element(By.ID, "form-register").submit()
        current_url = driver.current_url
        assert current_url == REGISTER_URL
    def test_incorrect_email(self, driver):
        driver.get(REGISTER_URL)

        driver.find_element(By.ID, "name").send_keys("Crishtian")
        driver.find_element(By.ID, "paternalName").send_keys("Jose")
        driver.find_element(By.ID, "maternalName").send_keys("Maria")
        driver.find_element(By.ID, "date-of-birth").send_keys(DATE_OF_BIRTH)
        driver.find_element(By.ID, "user").send_keys("juanco")
        driver.find_element(By.ID, "email").send_keys("juancmail.com")
        driver.find_element(By.ID, "password").send_keys("123456")

        driver.find_element(By.ID, "form-register").submit()
        current_url = driver.current_url
        assert current_url ==REGISTER_URL

class TestLoginPage:
    def test_correct_elector(self, driver):
        driver.get(LOGIN_URL)

        driver.find_element(By.ID, "user").send_keys("juanco")
        driver.find_element(By.ID, "password").send_keys("123456")

        driver.find_element(By.CSS_SELECTOR, "button.relative.inline-flex.items-center").click()
        time.sleep(1)
        current_url = driver.current_url
        assert current_url == HOME_URL

    def test_incorrect_elector(self, driver):
        driver.get(LOGIN_URL)

        driver.find_element(By.ID, "user").send_keys("juanco11")
        driver.find_element(By.ID, "password").send_keys("123456")

        driver.find_element(By.CSS_SELECTOR, "button.relative.inline-flex.items-center").click()
        current_url = driver.current_url
        assert current_url == LOGIN_URL
