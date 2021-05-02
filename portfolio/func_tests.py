from selenium import webdriver

PROTOCOL = 'http'
DOMAIN = 'localhost'
PORT = '8000'

browser = webdriver.Firefox()
browser.get(f'{PROTOCOL}://{DOMAIN}:{PORT}')

assert 'success' in browser.title