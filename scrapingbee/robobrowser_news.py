from robobrowser import RoboBrowser
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Initializing RoboBrowser")
browser = RoboBrowser(parser='html.parser')

logging.info("Opening the login page")
browser.open('https://news.ycombinator.com/login')

logging.info("Getting the login form by action name")
signin_form = browser.get_form(action='login')

logging.info("Filling out the form with username and password")
signin_form['acct'].value = 'your_username'
signin_form['password'].value = 'your_password'

logging.info("Submiting the form")
browser.submit_form(signin_form)

if browser.find(id='logout'):
    print('Successfully logged in')
else:
    print('Login failed')