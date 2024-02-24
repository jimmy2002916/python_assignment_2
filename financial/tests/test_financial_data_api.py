import unittest
from financial.api.app import app


class FinancialDataAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_financial_data_no_params(self):
        response = self.app.get('/financial_data')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json)
        self.assertIn('pagination', response.json)

    def test_get_financial_data_with_start_date_only(self):
        response = self.app.get('/financial_data?start_date=2020-01-01')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json)

    def test_get_financial_data_with_end_date_only(self):
        response = self.app.get('/financial_data?end_date=2020-12-31')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json)

    def test_get_financial_data_with_symbol_only(self):
        response = self.app.get('/financial_data?symbol=IBM')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json)

    def test_get_financial_data_with_all_params(self):
        response = self.app.get('/financial_data?start_date=2020-01-01&end_date=2020-12-31&symbol=IBM')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json)

    def test_pagination_limit(self):
        # Define the page and limit you want to test
        test_page = 1
        test_limit = 2  # For example, you want to test if the limit of 2 is expected

        # Make a GET request to the API endpoint with the page and limit
        response = self.app.get(f'/financial_data?page={test_page}&limit={test_limit}')

        # Check if the status code is 200
        self.assertEqual(response.status_code, 200)

        # Load the response data
        data = response.json
        print("data", data)

        # Check if the 'data' field in the response has the correct number of items
        self.assertEqual(len(data['data']), test_limit)

        # Check if the 'pagination' field has the correct 'limit'
        self.assertEqual(data['pagination']['limit'], test_limit)


if __name__ == '__main__':
    unittest.main()
