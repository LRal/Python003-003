import time
from selenium import webdriver

# 进入登录页面 - 输入账号密码 - 登录
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
        '//*[text()="立即登录"]')
    LoginButton.click()

except Exception as error:
    print('error')
finally:
    Browser.close()
