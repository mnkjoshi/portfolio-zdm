import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

os.environ['TESTING'] = 'true'

from app import app,mydb,TimelinePost

class AppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up headless Chrome for testing
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        # Close Chrome driver after all tests
        cls.driver.quit()

    def setUp(self):
        self.client = app.test_client()
        mydb.create_tables([TimelinePost])

    def tearDown(self):
        mydb.drop_tables([TimelinePost])
    
    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        # Check Page Title
        assert "<title>MLH Fellow</title>" in html
        # Check profile picture
        assert '<img src="./static/img/zidanni.jpg" alt="Profile Picture" />' in html
        # Check Name
        assert "<h1>Zidanni Clerigo</h1>" in html
        # Check Sections
        assert "<h2>About Me</h2>" in html
        assert "<h2>Places I Have Visited</h2>" in html
        assert "<h2>Experience</h2>" in html
        assert "<h2>Education</h2>" in html
    
    def test_timeline(self):
        # Assert GET timeline posts returns an empty list
        all_posts_response = self.client.get("/api/timeline_post")
        self._assert_get_posts_response(all_posts_response, 0)

        first_mock_post = {"name": "Jane Doe", "email": "jane@example.com", "content": "Hello, my name is Jane!"}
        second_mock_post = {"name": "John Doe", "email": "john@example.com", "content": "Hello, my name is John!"}

        # Assert posts are successfully added to the database
        first_new_post_response = self.client.post("/api/timeline_post", data=first_mock_post)
        self._assert_new_post_response(first_new_post_response, first_mock_post)
        second_new_post_response = self.client.post("/api/timeline_post", data=second_mock_post)
        self._assert_new_post_response(second_new_post_response, second_mock_post)

        # Assert GET timeline posts is consistent after adding new posts
        all_posts_response = self.client.get("/api/timeline_post")
        self._assert_get_posts_response(all_posts_response, 2, second_mock_post)

        # Assert timeline page endpoint works as expected
        timeline_html_response = self.client.get("/timeline")
        assert timeline_html_response.status_code == 200

        self.driver.get("http://localhost:5000/timeline")
        timeline_form = self._find("timeline-form")
        submit_button = self._find("form-submit")
        first_post_element = self._find(first_mock_post["email"])
        second_post_element = self._find(second_mock_post["email"])

        # Assert posts are rendered in the client side
        self.assertIsNotNone(first_post_element)
        self.assertIsNotNone(second_post_element)
        # Assert form and submit button exist
        self.assertIsNotNone(timeline_form)
        self.assertIsNotNone(submit_button)
    
    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data= {"email": "john@example.com", "content": "Hello, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data= {"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
    
    def _assert_get_posts_response(self, get_posts_response, expected_length, latest_post=None):
        assert get_posts_response.status_code == 200
        assert get_posts_response.is_json
        json = get_posts_response.get_json()
        assert "timeline_posts" in json
        # Assert the number of posts is equal to the expected length
        assert len(json["timeline_posts"]) == expected_length
        # Assert Posts are sorted in descending order
        if expected_length > 0:
            assert json["timeline_posts"][0]["name"] == latest_post["name"]
            assert json["timeline_posts"][0]["email"] == latest_post["email"]
            assert json["timeline_posts"][0]["content"] == latest_post["content"]
    
    def _assert_new_post_response(self, new_post_response, original_post):
        assert new_post_response.status_code == 200
        assert new_post_response.is_json
        new_post_json = new_post_response.get_json()
        # Assert the values of new post are consistent with new post added to database
        assert original_post["name"] == new_post_json["name"]
        assert original_post["email"] == new_post_json["email"]
        assert original_post["content"] == new_post_json["content"]
    
    def _find(self, val):
        # Find HTML element with a specified data-test-id
        return self.driver.find_element(by=By.CSS_SELECTOR, value=f'[data-test-id="{val}"]')