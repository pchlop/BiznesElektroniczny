from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def add_product_to_cart(category, product, amount):
    category = '//a[contains(@href,"id_category=' + category + '")]'
    product = '//a[contains(@href,"id_product=' + product + '")]'
    browser.find_element_by_xpath(category).click()
    browser.find_element_by_xpath(product).click()
    browser.find_element_by_id("quantity_wanted").clear()
    browser.find_element_by_id("quantity_wanted").send_keys(amount)
    browser.find_element_by_class_name("add-to-cart").click()
    time.sleep(2)
    browser.get('https://192.168.1.116/prestashop')

def delete_first_product_from_cart():
    browser.find_element_by_class_name("cart-preview").click()
    browser.find_element_by_class_name("remove-from-cart").click()

browser = webdriver.Chrome(r'F:\Projekty\Python\Biznes-selenium\chromedriver.exe')
browser.get('https://192.168.1.116/prestashop')
browser.find_element_by_id("details-button").click()
browser.find_element_by_id("proceed-link").click()

add_product_to_cart('12', '22', '7')
add_product_to_cart('11', '26', '1')
delete_first_product_from_cart()
time.sleep(1)
browser.find_element_by_xpath('//a[contains(@href,"order")]').click()

firstname = "testn"
lastname = "tests"
email = "abcww2dwewwww@gmail.com"
password = "qaz123WSX"
birthday = "1970-05-31"

browser.find_element_by_name("id_gender").click()
browser.find_element_by_name("firstname").send_keys(firstname)
browser.find_element_by_name("lastname").send_keys(lastname)
browser.find_element_by_name("email").send_keys(email)
browser.find_element_by_name("password").send_keys(password)
browser.find_element_by_name("birthday").send_keys(birthday)
browser.find_element_by_name("psgdpr").click()
browser.find_element_by_name("continue").click()

address1 = "Kolorowa 3"
postcode = "11-111"
city = "Warszawa"

browser.find_element_by_name("address1").send_keys(address1)
browser.find_element_by_name("postcode").send_keys(postcode)
browser.find_element_by_name("city").send_keys(city)
browser.find_element_by_name("confirm-addresses").click()

browser.find_element_by_id("delivery_option_3").click()
browser.find_element_by_name("confirmDeliveryOption").click()
browser.find_element_by_id("payment-option-1").click()
browser.find_element_by_id("conditions_to_approve[terms-and-conditions]").click()
time.sleep(1)
browser.find_elements_by_class_name("center-block")[1].click()

browser.find_elements_by_class_name("hidden-sm-down")[2].click()
browser.find_element_by_id("history-link").click()