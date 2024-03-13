import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SbisContactsPage:

    def __init__(self, driver):
        self.driver = driver

    region_button = (By.CSS_SELECTOR, ".sbis_ru-Region-Chooser__text")
    region_dropdown = (By.XPATH, "//ul[@class='sbis_ru-Region-Panel__list-l']")
    desired_region = (By.XPATH, "//span[text()='41 Камчатский край']")
    selected_region = (By.XPATH, "//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")

    def open(self):
        self.driver.get("https://sbis.ru/contacts")

    def wait_for_page_to_load(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.region_button))

    def select_region(self):
        self.click_on_region()
        self.wait_for_region_dropdown_to_open()
        self.click_on_desired_region()
        self.wait_for_region_to_be_selected()

    def click_on_region(self):
        self.driver.find_element(*self.region_button).click()

    def wait_for_region_dropdown_to_open(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.region_dropdown))

    def click_on_desired_region(self):
        self.driver.find_element(*self.desired_region).click()

    def wait_for_region_to_be_selected(self):
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element(self.selected_region, "Камчатский край"))

    def assert_selected_region(self):
        assert self.driver.find_element(*self.selected_region).text == "Камчатский край"

    def assert_url_contains_region(self):
        assert "41-kamchatskij-kraj" in self.driver.current_url

    def assert_title_contains_region(self):
        assert "Камчатский край" in self.driver.title

    def get_region(self):
        return self.driver.find_element(*self.region_button).text

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment this line to run the test in headless mode
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.close()

def test_sbis_contacts_page(driver):
    page = SbisContactsPage(driver)
    page.open()
    page.wait_for_page_to_load()
    assert page.get_region() == "Ярославская обл."
    page.select_region()
    page.assert_selected_region()
    page.assert_url_contains_region()
    page.assert_title_contains_region()
