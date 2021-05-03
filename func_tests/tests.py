import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()
    
    def test_user_can_see_index(self):
        # User heads to site to check out Cumbia Photographers work
        self.browser.get(self.live_server_url)

        # She sees that 'Cumbia' is the index title
        self.assertIn('Cumbia', self.browser.title)

        # She can see the Cumbia logo at the center of the page
        logo_img = self.browser.find_element(By.ID, 'brand-center-img')
        logo_img_src = logo_img.get_attribute('src')
        self.assertIn('cumbia-logo-negro.png', logo_img_src)

        # She can see links to all the available photographer's listed
        # nav = self.browser.find_element(By.ID, 'main-nav')
        # links = nav.find_elements_by_class_name('ph-link')
        # self.assertTrue(len(list(links)) > 0)           # TO-DO missing link test

        # She can see a list of informational links:
        # * 'nosotros'
        # * 'instagram'
        # * 'contacto'
        self.fail('FINISH THE TEST!')

        # She can hover over each photographer's name and see 
        # * a photo by that photographer in the center of the page
        # * the photographer's name in a detailed view
        # * photo caption

        # She can click on each photographer's name and go to 
        # that photographer's detail page

        # She can click on each of the links and be directed to 
        # the corresponding page