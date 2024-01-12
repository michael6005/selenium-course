import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from config.settings import BASE_DIR
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


@pytest.fixture
def root_url():
    return f'file:///{BASE_DIR / "store-template" / "index.html"}'


def _switch_to_another_handler(browser, original_page_handler):
    for window_handle in browser.window_handles:
        if window_handle != original_page_handler:
            browser.switch_to.window(window_handle)
            break


def test_bs(browser, root_url):
    browser.get(root_url)
    browser.maximize_window()
    browser.find_element(By.ID, 'start-purchase-link').click()

    bs = BeautifulSoup(browser.page_source, 'html.parser')
    rows = bs.find_all('div', attrs={'class': 'card-body'})

    products = []
    for row in rows:
        title = row.find('h4').text
        products.append(title)

    with open('products.txt', 'w') as file:
        file.write('\n'.join(products))


def test_interaction_with_tabs_or_windows(browser, root_url):
    actions = webdriver.ActionChains(browser)
    browser.get(root_url)
    browser.maximize_window()

    original_page_handler = browser.current_window_handle

    login_page_link = browser.find_element(By.LINK_TEXT, 'Войти')
    actions.key_down(Keys.CONTROL).click(login_page_link).key_up(Keys.CONTROL).perform()
    _switch_to_another_handler(browser, original_page_handler)
    login_title = browser.title
    assert login_title == 'Store - Авторизация'

    browser.close()
    browser.switch_to.window(original_page_handler)

    time.sleep(5)
    catalog_page = browser.find_element(By.XPATH, '/html/body/nav/div/div/ul/li[1]/a')
    actions.key_down(Keys.CONTROL).click(catalog_page).key_up(Keys.CONTROL).perform()
    _switch_to_another_handler(browser, original_page_handler)
    catalog_title = browser.title
    assert catalog_title == 'Store - Каталог'

    browser.close()
    browser.switch_to.window(original_page_handler)
    time.sleep(5)
    main_title = browser.title
    assert main_title == 'Store'


def test_interaction(browser, root_url):
    browser.get(root_url)
    browser.maximize_window()

    browser.find_element(By.ID, 'navbarDropdown').click()
    browser.find_element(By.LINK_TEXT, 'Профиль').click()
    browser.find_element(By.LINK_TEXT, 'Оформить заказ').click()
    first_name = browser.find_element(By.ID, 'firstName')
    first_name.send_keys('Michael')

    last_name = browser.find_element(By.ID, 'lastName')
    last_name.send_keys('Korol')

    assert first_name.get_attribute('value') == 'Michael'
    assert last_name.get_attribute('value') == 'Korol'

    remember_data = browser.find_element(By.ID, 'rememberData')
    remember_data.click()
    assert remember_data.is_selected()

    remember_data.click()
    assert remember_data.is_selected() is False


def test_find_by_css_selectors(headless_chrome, root_url):
    headless_chrome.get(root_url)
    headless_chrome.maximize_window()

    headless_chrome.find_element(By.ID, 'start-purchase-link').click()
    el1 = headless_chrome.find_element(By.CSS_SELECTOR, 'a[aria-disabled="true"]')
    el2 = headless_chrome.find_element(By.CSS_SELECTOR, '#navbarDropdown')
    el_list = [el1, el2]

    assert all(el is not None for el in el_list)


def test_add_to_cart_and_remove(browser, root_url):
    browser.get(root_url)
    browser.maximize_window()

    browser.find_element(By.ID, 'start-purchase-link').click()

    cart_title = browser.find_element(By.CLASS_NAME, 'card-title').text

    card_footer = browser.find_element(By.CLASS_NAME, 'card-footer')
    card_footer.find_element(By.TAG_NAME, 'button').click()

    browser.find_element(By.ID, 'navbarDropdown').click()
    browser.find_element(By.LINK_TEXT, 'Профиль').click()

    added_item_title = browser.find_element(By.CLASS_NAME, 'card-title').text

    assert cart_title == added_item_title
    WebDriverWait(browser, timeout=5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="trash"]/i')))
    browser.find_element(By.ID, 'trash').click()
    message = browser.find_element(By.TAG_NAME, 'h3').text
    assert message == 'Нет добавленных товаров'


def test_titles_are_correct(browser, root_url):
    browser.maximize_window()
    browser.get(root_url)
    main_title = browser.find_element(By.CLASS_NAME, 'navbar-brand')
    assert main_title.text == 'Store'
    purchase_link = browser.find_element(By.ID, 'start-purchase-link')
    purchase_link.click()
    product_title = browser.find_element(By.ID, 'product-title')
    assert product_title.text == 'Store'
