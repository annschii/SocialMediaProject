import unittest
import json
from SWEG_SocialMediaProject.app import app
from SWEG_SocialMediaProject.social_media_db import social_media_db


# In your unit test code
DATABASE_URL_TEST = os.environ.get("DATABASE_URL_TEST", "postgresql://postgres:postgres@db_test:5432/test_database")


class TestApp(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()

    def test_list_posts(self):
        # Test the GET /posts endpoint
        response = self.app.get('/posts')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        # Add more assertions based on the expected behavior of the /posts endpoint

    def test_create_new_post(self):
        # Test the POST /posts endpoint for creating a new post
        sample_data = {"title": "Test Post", "content": "This is a test post."}
        response = self.app.post('/posts', json=sample_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("id", data)
        # Add more assertions based on the expected behavior of creating a new post

    def test_get_post_detail(self):
        # Test the GET /posts/<int:post_id> endpoint
        # Assuming there is a post with ID 1
        response = self.app.get('/posts/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        # Add more assertions based on the expected behavior of getting a post by ID

    # Add more test methods for other endpoints as needed

if __name__ == '__main__':
    unittest.main()
