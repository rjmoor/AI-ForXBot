# tests/unit/test_data_population.py

import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch

from api.services.data_population_service import DataPopulationService


class TestDataPopulationService(unittest.TestCase):
    
    def setUp(self):
        self.population_service = DataPopulationService()

    @patch('api.services.data_population_service.OandaClient')  # Mock the OandaClient class
    @patch('api.services.data_population_service.MongoDBHandler')  # Mock MongoDBHandler
    def test_populate_historical_data(self, MockMongoDBHandler, MockOandaClient):
        """
        Test fetching and populating historical data for a specific forex pair.
        """
        # Mock the response from fetch_historical_data to return some candles
        mock_oanda_client_instance = MockOandaClient.return_value
        mock_oanda_client_instance.fetch_historical_data.return_value = [
            {
                "time": "2024-09-03T11:25:00.000000000Z",
                "volume": 100,
                "mid": {"o": 1.2, "h": 1.25, "l": 1.18, "c": 1.22}
            },
            {
                "time": "2024-09-03T11:26:00.000000000Z",
                "volume": 110,
                "mid": {"o": 1.22, "h": 1.26, "l": 1.19, "c": 1.24}
            }
        ]
        
        # Mock the MongoDBHandler bulk_insert method to avoid actual DB operations
        mock_mongo_handler_instance = MockMongoDBHandler.return_value
        mock_mongo_handler_instance.short_bulk_insert = MagicMock()
        
        # Call the populate_historical_data method
        data_population_service = DataPopulationService()
        data_population_service.populate_historical_data("EUR_USD", "M1", 500)
        
        # Check that bulk_insert was called (meaning data was inserted)
        mock_mongo_handler_instance.short_bulk_insert.assert_called_once()
        
        # Verify the inserted data
        args, kwargs = mock_mongo_handler_instance.short_bulk_insert.call_args
        self.assertGreater(len(args[0]), 0)  # args[0] is the list of documents that were inserted


if __name__ == "__main__":
    unittest.main()
