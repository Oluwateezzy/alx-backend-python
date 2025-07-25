#!/usr/bin/env python3
"""Test module for utils functions.
Contains tests for access_nested_map, get_json, and memoize functions.
"""
from typing import Any, Dict, Mapping, Sequence
import unittest
from unittest.mock import Mock, patch
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """Test class for utils.access_nested_map function."""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self, nested_map: Mapping,
        path: Sequence, expected: Any
    ) -> None:
        """Test access_nested_map with various inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Mapping,
        path: Sequence,
        expected_msg: str
    ) -> None:
        """Test access_nested_map raises KeyError with correct message."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_msg)


class TestGetJson(unittest.TestCase):
    """Test class for utils.get_json function."""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
        self,
        test_url: str,
        test_payload: Dict
    ) -> None:
        """Test get_json returns expected payload from mocked requests."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        with patch('requests.get', return_value=mock_response) as mock_get:
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test class for utils.memoize decorator."""
    def test_memoize(self) -> None:
        """Test that memoize decorator caches method results properly."""
        class TestClass:
            """Test class with methods to be memoized."""
            def a_method(self) -> int:
                """Method that will be mocked and memoized."""
                return 42

            @memoize
            def a_property(self) -> int:
                """Property that memoizes the result of a_method."""
                return self.a_method()

        test_instance = TestClass()

        with patch.object(
            TestClass,
            'a_method',
            return_value=42
        ) as mock_method:
            result1 = test_instance.a_property
            result2 = test_instance.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
