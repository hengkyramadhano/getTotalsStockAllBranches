import unittest
class TestMyFunction(unittest.TestCase):
    def setUp(self):
        self.test_list = [1, 2, 3, 4, 5]
        print("setUp")
        sku = "OMHALNWH"
        self.hit_api(sku)

    def test_length_of_list(self):
        self.assertEqual(len(self.test_list), 5)
        print("test")
        
    def tearDown(self):
        del self.test_list
        print("tearDown")

    def hit_api(self, sku2):
        print(f"hit_api {sku2}")