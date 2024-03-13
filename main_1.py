import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

# Базовый класс для всех страниц
class PageObject:

    def __init__(self, driver):
        self.driver = driver

    # Перейти на страницу "Контакты"
    def go_to_contacts_page(self):
        self.driver.get("https://sbis.ru/")
        self.find_element((By.LINK_TEXT, "Контакты")).click()

    # Найти элемент на странице
    def find_element(self, locator):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )

# Страница "Контакты"
class ContactsPage(PageObject):

    # Перейти на страницу Tensor
    def go_to_tensor(self):
        tensor_banner = self.find_element((By.CSS_SELECTOR, "a[href='https://tensor.ru/']"))
        tensor_banner.click()
        self.driver.switch_to.window(self.driver.window_handles[1])

# Страница "О компании"
class AboutPage(PageObject):

    # Открыть страницу "О компании"
    def open_about_page(self):
        strength_in_people = self.find_element((By.XPATH, "//*[contains(text(), 'Сила в людях')]"))
        self.driver.execute_script("arguments[0].scrollIntoView();", strength_in_people)
        learn_more = self.find_element((By.XPATH, "//a[@href='/about']"))
        learn_more.click()

# Страница "Работа"
class WorkPage(PageObject):

    # Проверить размеры фотографий на странице "Работа"
    def check_photo_sizes(self):
        work = self.find_element((By.XPATH, "//h2[text()='Работаем']"))
        self.driver.execute_script("arguments[0].scrollIntoView();", work)
        photos = work.find_elements(By.TAG_NAME, "img")

        for photo in photos:
            assert photo.get_attribute("height") == photos[0].get_attribute("height")
            assert photo.get_attribute("width") == photos[0].get_attribute("width")

# Фикстура для инициализации и завершения работы драйвера браузера
@pytest.fixture(scope="class")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# Тестовый класс
class TestTensorWebsite:

    # Тест для проверки сайта Tensor
    def test_tensor_website(self, driver):
        contacts_page = ContactsPage(driver)
        contacts_page.go_to_contacts_page()
        contacts_page.go_to_tensor()

        about_page = AboutPage(driver)
        about_page.open_about_page()

        work_page = WorkPage(driver)
        work_page.check_photo_sizes()
