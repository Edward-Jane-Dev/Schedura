from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime, timedelta
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Event, Resource, ResourceCategory, EventType
from django.utils import timezone
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

# Create your tests here.

class HomePageSeleniumTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        cls.browser = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_homepage_button_redirects_to_schedule(self):
        self.browser.get(self.live_server_url + '/')
        button = self.browser.find_element(By.LINK_TEXT, 'Go to Schedule')
        button.click()
        time.sleep(1)  # Wait for navigation
        self.assertIn('/schedule/', self.browser.current_url)

class SchedulerAPITests(APITestCase):
    def setUp(self):
        self.category = ResourceCategory.objects.create(name='Room', description='A room') # type: ignore
        self.resource = Resource.objects.create(name='Conference Room', description='A big room', category=self.category) # type: ignore
        self.event_type = EventType.objects.create(name='Meeting', description='A meeting', block_resource=False) # type: ignore

    def test_create_resource_category(self):
        url = reverse('resourcecategory-list')
        data = {'name': 'Projector', 'description': 'A projector'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(ResourceCategory.objects.filter(name='Projector').exists()) # type: ignore

    def test_create_resource(self):
        url = reverse('resource-list')
        data = {'name': 'Whiteboard', 'description': 'A whiteboard', 'category': self.category.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201) # type: ignore
        self.assertTrue(Resource.objects.filter(name='Whiteboard').exists()) # type: ignore

    def test_create_event_type(self):
        url = reverse('eventtype-list')
        data = {'name': 'Workshop', 'description': 'A workshop', 'block_resource': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201) # type: ignore
        self.assertTrue(EventType.objects.filter(name='Workshop').exists()) # type: ignore

    def test_create_event(self):
        url = reverse('event-list')
        start = timezone.now()
        end = start + timezone.timedelta(hours=1)
        data = {
            'name': 'Team Sync',
            'description': 'Daily sync',
            'resource': self.resource.id,
            'event_type': self.event_type.id,
            'start_time': start.isoformat(),
            'end_time': end.isoformat(),
            'is_recurring': False,
            'recurrence_rule': '',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201) # type: ignore
        self.assertTrue(Event.objects.filter(name='Team Sync').exists()) # type: ignore

class SchedulerSeleniumUITests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.set_capability('goog:loggingPrefs', {"browser":"ALL"})
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        cls.browser = webdriver.Chrome(options=chrome_options)
        cls.browser.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def open_schedule_page(self):
        self.browser.get(self.live_server_url + '/schedule/')

    def test_add_resource_category_via_ui(self):
        self.open_schedule_page()
        add_event_btn = self.browser.find_element(By.CSS_SELECTOR, '[data-bs-target="#addEventModal"]')
        add_event_btn.click()
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#addEventModal.show'))
        )
        time.sleep(1)
        # Open Add Resource modal
        add_resource_category_btn = self.browser.find_element(By.CSS_SELECTOR, '[data-bs-target="#addResourceModal"]')
        add_resource_category_btn.click()
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#addResourceModal.show'))
        )
        
        time.sleep(1)
        # Open Add Resource Category modal from within Resource modal
        add_category_btn = self.browser.find_element(By.CSS_SELECTOR, '[data-bs-target="#addResourceCategoryModal"]')
        add_category_btn.click()
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#addResourceCategoryModal.show'))
        )
        
        time.sleep(1)
        self.browser.find_element(By.ID, 'resource-category-name').send_keys('UI Category')
        self.browser.find_element(By.ID, 'resource-category-description').send_keys('Created via UI')
        self.browser.find_element(By.ID, 'add-resource-category-form').submit()
        
        # Wait for modal to close
        WebDriverWait(self.browser, 5).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, '#addResourceCategoryModal.show'))
        )
        
        # Reopen Add Event modal
        add_event_btn = self.browser.find_element(By.CSS_SELECTOR, '[data-bs-target="#addEventModal"]')
        add_event_btn.click()
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#addEventModal.show'))
        )
        # Reopen Add Resource modal and check dropdown
        add_resource_btn = self.browser.find_element(By.CSS_SELECTOR, '[data-bs-target="#addResourceModal"]')
        add_resource_btn.click()
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#addResourceModal.show'))
        )
        dropdown = self.browser.find_element(By.ID, 'resource-category-modal')
        options = [o.text for o in dropdown.find_elements(By.TAG_NAME, 'option')]
        assert 'UI Category' in options

    def test_add_resource_via_ui(self):
        ResourceCategory.objects.create(name='Room', description='A room') # type: ignore
        self.open_schedule_page()
        add_event_btn = self.browser.find_element(By.CSS_SELECTOR, '[data-bs-target="#addEventModal"]')
        add_event_btn.click()
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#addEventModal.show'))
        )
        time.sleep(0.5)
        # Open Add Resource modal
        add_resource_btn = self.browser.find_element(By.CSS_SELECTOR, '[data-bs-target="#addResourceModal"]')
        add_resource_btn.click()
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#addResourceModal.show'))
        )
        time.sleep(0.5)
        self.browser.find_element(By.ID, 'resource-name').send_keys('UI Resource')
        self.browser.find_element(By.ID, 'resource-description').send_keys('Created via UI')
        dropdown = self.browser.find_element(By.ID, 'resource-category-modal')
        options = [o.text for o in dropdown.find_elements(By.TAG_NAME, 'option')]
        # print(options)
        dropdown.find_elements(By.TAG_NAME, 'option')[1].click()
        self.browser.find_element(By.ID, 'add-resource-form').submit()
        WebDriverWait(self.browser, 5).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, '#addResourceModal.show'))
        )
        time.sleep(0.5)
        # Reopen Add Event modal
        add_event_btn = self.browser.find_element(By.CSS_SELECTOR, '[data-bs-target="#addEventModal"]')
        add_event_btn.click()
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#addEventModal.show'))
        )
        time.sleep(0.5)
        # Open Add Event Type modal and add an event type (if not already present)
        add_event_type_btn = self.browser.find_element(By.CSS_SELECTOR, '[data-bs-target="#addEventTypeModal"]')
        add_event_type_btn.click()
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#addEventTypeModal.show'))
        )
        time.sleep(0.5)
        self.browser.find_element(By.ID, 'event-type-name').send_keys('UI EventType')
        self.browser.find_element(By.ID, 'event-type-description').send_keys('Created via UI')
        self.browser.find_element(By.ID, 'add-event-type-form').submit()
        WebDriverWait(self.browser, 5).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, '#addEventTypeModal.show'))
        )
        time.sleep(0.5)
        # Now open Add Event modal and check resource dropdown
        add_event_btn = self.browser.find_element(By.CSS_SELECTOR, '[data-bs-target="#addEventModal"]')
        add_event_btn.click()
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#addEventModal.show'))
        )
        time.sleep(0.5)
        event_resource_dropdown = self.browser.find_element(By.ID, 'event-resource')
        options = [o.text for o in event_resource_dropdown.find_elements(By.TAG_NAME, 'option')]
        assert 'UI Resource' in options

    def test_add_event_type_via_ui(self):
        self.open_schedule_page()

        category = ResourceCategory.objects.create(name='Room', description='A room') # type: ignore
        Resource.objects.create(name='Conference Room', description='A big room', category=category) # type: ignore

        add_event_btn = self.browser.find_element(By.CSS_SELECTOR, '[data-bs-target="#addEventModal"]')
        add_event_btn.click()
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#addEventModal.show'))
        )
        time.sleep(0.5)

        add_event_type_btn = self.browser.find_element(By.CSS_SELECTOR, '[data-bs-target="#addEventTypeModal"]')
        add_event_type_btn.click()
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#addEventTypeModal.show'))
        )
        time.sleep(0.5)
        self.browser.find_element(By.ID, 'event-type-name').send_keys('UI EventType')
        self.browser.find_element(By.ID, 'event-type-description').send_keys('Created via UI')
        self.browser.find_element(By.ID, 'add-event-type-form').submit()
        WebDriverWait(self.browser, 5).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, '#addEventTypeModal.show'))
        )
        time.sleep(0.5)
        # Open Add Event modal and check event type dropdown
        add_event_btn = self.browser.find_element(By.CSS_SELECTOR, '[data-bs-target="#addEventModal"]')
        add_event_btn.click()
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#addEventModal.show'))
        )
        time.sleep(0.5)
        event_type_dropdown = self.browser.find_element(By.ID, 'event-type')
        options = [o.text for o in event_type_dropdown.find_elements(By.TAG_NAME, 'option')]
        assert 'UI EventType' in options

    def test_add_event_via_ui(self):
        category = ResourceCategory.objects.create(name='Room', description='A room') # type: ignore
        Resource.objects.create(name='Conference Room', description='A big room', category=category) # type: ignore
        EventType.objects.create(name='Meeting', description='A meeting', block_resource=False) # type: ignore
        for event_type in EventType.objects.all():
            print(event_type)
        assert(EventType.objects.filter(name='Meeting').exists())

        self.open_schedule_page()

        add_event_btn = self.browser.find_element(By.CSS_SELECTOR, '[data-bs-target="#addEventModal"]')
        add_event_btn.click()
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#addEventModal.show'))
        )
        time.sleep(0.5)
        options = [o.text for o in self.browser.find_element(By.ID, 'event-resource').find_elements(By.TAG_NAME, 'option')]
        print(options)
        options = [o.text for o in self.browser.find_element(By.ID, 'event-type').find_elements(By.TAG_NAME, 'option')]
        print(options)
        self.browser.find_element(By.ID, 'event-name').send_keys('UI Event')
        self.browser.find_element(By.ID, 'event-description').send_keys('Created via UI')
        self.browser.find_element(By.ID, 'event-resource').find_elements(By.TAG_NAME, 'option')[1].click()
        self.browser.find_element(By.ID, 'event-type').find_elements(By.TAG_NAME, 'option')[1].click()
        now = datetime.now().replace(microsecond=0, second=0)
        start = now
        end = now + timedelta(hours=1)
        self.browser.find_element(By.ID, 'event-start').send_keys(start.day)
        self.browser.find_element(By.ID, 'event-start').send_keys(start.month)
        self.browser.find_element(By.ID, 'event-start').send_keys(start.year)
        self.browser.find_element(By.ID, 'event-start').send_keys(Keys.TAB)
        self.browser.find_element(By.ID, 'event-start').send_keys("00")
        self.browser.find_element(By.ID, 'event-start').send_keys("00")
        
        self.browser.find_element(By.ID, 'event-end').send_keys(end.day)
        self.browser.find_element(By.ID, 'event-end').send_keys(end.month)
        self.browser.find_element(By.ID, 'event-end').send_keys(end.year)
        self.browser.find_element(By.ID, 'event-end').send_keys(Keys.TAB)
        self.browser.find_element(By.ID, 'event-end').send_keys("23")
        self.browser.find_element(By.ID, 'event-end').send_keys("59")
        self.browser.find_element(By.ID, 'add-event-form').submit()
        WebDriverWait(self.browser, 5).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, '#addEventModal.show'))
        )
        time.sleep(2)

        # logs = self.browser.get_log("browser")

        # print(logs)
        # Check if the event appears on the calendar (look for badge)
        assert(Event.objects.filter(name='UI Event').exists())
        # badges = self.browser.find_elements(By.CLASS_NAME, 'badge')
        # assert any('UI Event' in b.text for b in badges)
