#!/usr/bin/env python3
"""Test module for client.GithubOrgClient class."""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(
        self,
        org_name: str,
        mock_get_json: unittest.mock.Mock
    ) -> None:
        """Test that GithubOrgClient.org returns correct value.
        
        Args:
            org_name: The organization name to test
            mock_get_json: Mock for get_json function
        """
        # Set up test data
        test_payload = {
            "name": org_name,
            "repos_url": f"https://repos/{org_name}"
        }
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)

        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        self.assertEqual(result, test_payload)

        result2 = client.org
        self.assertEqual(result2, test_payload)
        mock_get_json.assert_called_once()
    
    def test_public_repos_url(self) -> None:
        """Test that _public_repos_url returns the correct URL from org payload."""
        test_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }
        
        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("testorg")
            result = client._public_repos_url
            self.assertEqual(result, test_payload["repos_url"])
