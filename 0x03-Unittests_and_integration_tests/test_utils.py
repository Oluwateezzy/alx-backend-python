#!/usr/bin/env python3

from typing import Any, Dict, Mapping, Sequence
import unittest
from unittest.mock import Mock, patch
from utils import access_nested_map, get_json
from parameterized import parameterized

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence, expected: Any) -> None:
        """Test access_nested_map with various inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence, expected_msg: str) -> None:
        """Test access_nested_map raises KeyError with correct message for invalid paths."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_msg)


class TestGetJson(unittest.TestCase):
    """Test class for utils.get_json function.
    Tests that the function makes correct HTTP requests and returns expected JSON.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: Dict) -> None:
        """Test get_json returns the expected payload from mocked requests.
        
        Args:
            test_url: The URL to test with
            test_payload: The expected JSON payload
        """
        # Create a mock response object
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        
        # Patch requests.get to return our mock response
        with patch('requests.get', return_value=mock_response) as mock_get:
            # Call the function
            result = get_json(test_url)
            
            # Assert the mock was called exactly once with test_url
            mock_get.assert_called_once_with(test_url)
            
            # Assert the result matches test_payload
            self.assertEqual(result, test_payload)