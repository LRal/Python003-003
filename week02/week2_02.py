import time
from selenium import webdriver

try:
    browser = webdriver.Edge()
    browser.get('https://shimo.im')
    time.sleep(1)

    LoginURL = browser.find_element_by_xpath(
        '//*[@class="login-button btn_hover_style_8"]')
    LoginURL.click()
    time.sleep(1)

    InputUsername = browser.find_element_by_xpath('//*[@name="mobileOrEmail"]')
    InputPassword = browser.find_element_by_xpath('//*[@name="password"]')
    InputUsername.send_keys('username')
    InputPassword.send_keys('password')

    LoginButton = browser.find_element_by_xpath(
        '//*[@class="sm-button submit sc-1n784rm-0 bcuuIb"]')
    LoginButton.click()

    cookies = browser.get_cookies()
    print(cookies)

except Exception as error:
    print('error')
finally:
    browser.close()
