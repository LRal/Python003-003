import time
from selenium import webdriver

try:
    Browser = webdriver.Edge()
    Browser.get('https://shimo.im')
    time.sleep(1)

    LoginURL = Browser.find_element_by_xpath(
        '//*[@class="login-button btn_hover_style_8"]')
    LoginURL.click()
    time.sleep(1)

    InputUsername = Browser.find_element_by_xpath('//*[@name="mobileOrEmail"]')
    InputPassword = Browser.find_element_by_xpath('//*[@name="password"]')
    InputUsername.send_keys('username')
    InputPassword.send_keys('password')

    LoginButton = Browser.find_element_by_xpath(
        '//*[@class="sm-button submit sc-1n784rm-0 bcuuIb"]')
    LoginButton.click()

except Exception as error:
    print('error')
finally:
    Browser.close()
