from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from datetime import datetime


# Account details
username = "dummy@gmail.com"
password = "80\X#qE&gt;2_?"


date_ids = ["an2", "an3", "an4", "an5", "an6", "an7", "an1"]
weekday = datetime.now().weekday()
date_id_today = date_ids[weekday+1]


selection_name = "Peter Blummen"
selection_element_xpath = '//h5[text()="' + selection_name + '"]//parent::button'

print("selection_element_xpath:", selection_element_xpath)
# exit()

opts = Options()
opts.add_argument("start-maximized")
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36")

driver = webdriver.Chrome(options=opts)
# driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36", "platform":"Linux"})
driver.get("https://clients.mindbodyonline.com/consumermyinfo?studioid=5720459&tg=&vt=&lvl=&stype=&view=&trn=0&page=&catid=&prodid=&date=6%2f20%2f2021&classid=0&prodGroupId=&sSU=&optForwardingLink=&qParam=&justloggedin=&nLgIn=&pMode=0&loc=1")

wait = WebDriverWait(driver, 30)

sign_in_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "myInfoSignInButton")))
assert "Sign In" in sign_in_button.get_attribute("value")
sign_in_button.send_keys(Keys.ENTER)


print("sign_in_button: ", sign_in_button)

username_element = wait.until(EC.element_to_be_clickable((By.ID, 'username')))
password_element = wait.until(EC.element_to_be_clickable((By.ID, 'password')))
button_element = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'button')))


username_element.clear()
username_element.send_keys(username)

password_element.clear()
password_element.send_keys(password)

button_element.send_keys(Keys.ENTER)

selection_element = wait.until(EC.presence_of_element_located((By.XPATH, selection_element_xpath)))
print("selection_element:", selection_element)

selection_element.click()

wait.until(EC.presence_of_element_located((By.XPATH, '//a[@id="tabA7"]'))).click()

day_elem = wait.until(EC.presence_of_element_located((By.ID, date_id_today)))
assert str(datetime.now().day) in day_elem.text

try:
    register_button_elem = wait.until(EC.presence_of_element_located((By.XPATH, '//td[@id="{}"]/parent::tr/following-sibling::tr[3]/td[2]/input[@name="but7"]'.format(date_id_today))))
    print("register_button_elem:", register_button_elem)
    print("Hooray Regisrations open.")
    register_button_elem.click()

    try:
        action_button = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="SubmitEnroll2" and @class="actionButton"]')))
        print("action_button:", action_button)
        action_button.click()
        print("It happened. Booked the ticket.")
    except TimeoutException:
        main_text = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="mainTextBig"]/span/b')))
        assert "The class/event that you are trying to reserve is full." in main_text.text
        print("The class/event that you are trying to reserve is full.")
except TimeoutException:
    try:
        already_registered_elem = wait.until(EC.presence_of_element_located((By.XPATH, '//td[@id="{}"]/parent::tr/following-sibling::tr[3]/td[2]/a/strong/span'.format(date_id_today))))
        print("already_registered_elem:", already_registered_elem)
        assert "Registered!" in already_registered_elem.text
        print("Already Registered!")
    except AssertionError:
        raise AssertionError("Nothing here.")
    except TimeoutException:
        print("Something's badly wrong.")

# driver.get("https://clients.mindbodyonline.com/classic/mainclass?studioid=5720459&tg=&vt=&lvl=&stype=-7&view=day&trn=0&page=&catid=&prodid=&date=6%2f20%2f2021&classid=0&prodGroupId=&sSU=&optForwardingLink=&qParam=&justloggedin=&nLgIn=&pMode=0&loc=1")

driver.close()