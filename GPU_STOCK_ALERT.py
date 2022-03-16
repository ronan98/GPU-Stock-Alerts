from selenium import webdriver
from selenium.webdriver.common.by import By
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    email = os.getenv('USER_EMAIL')
    pw = os.getenv('USER_PASS')
    sms_gate = os.getenv('SMS_GATEWAY').split()
    url = "https://www.bestbuy.com/site/searchpage.jsp?id=pcat17071&qp=brand_facet%3DBrand~ASUS%5Ebrand_facet%3DBrand~EVGA%5Ebrand_facet%3DBrand~NVIDIA%5Econdition_facet%3DCondition~New%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%20Ti%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203070%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203070%20Ti&st=nvidia+rtx+gpu"
    PATH = "C:\Program Files (x86)\chromedriver.exe"

    while True:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('window-size=1,1')
        driver = webdriver.Chrome(executable_path= PATH, options = options)
        driver.set_window_position(-5000, 0)
        driver.get(url)

        time.sleep(10)

        items = driver.find_elements(By.CLASS_NAME, 'sku-item')
        for item in items:
            button = item.find_element(By.CLASS_NAME, 'sku-list-item-button')
            status = (button.find_element(By.TAG_NAME, 'button')).get_attribute('data-button-state')
            if status != "SOLD_OUT":
                title = '\n' + item.find_element(By.CLASS_NAME, 'sku-title').text
                price = '\n\n' + item.find_element(By.CLASS_NAME, 'sku-list-item-price').text
                href = '\n' + item.find_element(By.TAG_NAME, 'a').get_attribute('href')
                msg = title + price + href
                sendMail(msg, email, pw, sms_gate)
        
        driver.quit()
        print('sleeping...')
        time.sleep(10)

def sendMail(data, email, pas, sms_gate):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(email, pas)
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = ", ".join(sms_gate)
        msg['Subject'] = 'GPU STOCK ALERT'
        body = data
        msg.attach(MIMEText(body, 'plain'))

        sms = msg.as_string()
        server.sendmail(email, sms_gate, sms)
        server.quit()


    except smtplib.SMTPResponseException as e:
        error_code = e.smtp_code
        error_message = e.smtp_error
        print(error_code)
        print(error_message)
    
if __name__ == "__main__":
    main()
    
    