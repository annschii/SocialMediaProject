import unittest
import json
import os
from io import BytesIO
from flask import Flask
from flask.testing import FlaskClient
from SWEG_SocialMediaProject.app import app
from SWEG_SocialMediaProject import social_media_db


# In your unit test code
DATABASE_URL = os.environ.get("DATABASE_URL_TEST", "postgresql://postgres:postgres@db_test:5433/test_database")


class TestApp(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app: Flask = app
        self.client: FlaskClient = app.test_client()

    def test_list_posts(self):
        # Test the GET /posts endpoint
        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        # Add more assertions based on the expected behavior of the /posts endpoint

    def test_upload_image(self):
        # Simulate file upload
        sample_image_path = "DSC_0411.JPG"  # Update with your image path
        with open(sample_image_path, "rb") as image_file:
            response = self.client.post('/images', data={'file': (image_file, 'sample_image.jpg')})

        # Check the response status code
        self.assertEqual(response.status_code, 201)

        # Optionally, check the response data for image URL or other details
        data = json.loads(response.data)
        self.assertIn('image_url', data)

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
