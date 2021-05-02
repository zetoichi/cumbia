from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
    
    def test_can_see_homepage(self):
        # User heads to site to check out Cumbia Photographers work
        self.browser.get('http://localhost:8000')

        # She sees that 'Cumbia' is the homepage title
        self.assertIn('Cumbia', self.browser.title)
        self.fail('FINISH THE TEST!')

        # She can see the Cumbia logo at the center of the page

        # She can see all the available photographer's listed

        # She can see a list of informational links:
        # * 'nosotros'
        # * 'instagram'
        # * 'contacto'

        # She can hover over each photographer's name and see 
        # * a photo by that photographer in the center of the page
        # * the photographer's name in a detailed view
        # * photo caption

        # She can click on each photographer's name and go to 
        # that photographer's detail page

        # She can click on each of the links and be directed to 
        # the corresponding page

if __name__ == '__main__':
    unittest.main(warnings='ignore')