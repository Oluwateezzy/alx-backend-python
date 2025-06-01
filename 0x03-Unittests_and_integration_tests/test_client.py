#!/usr/bin/env python3
"""Test module for client.GithubOrgClient class."""
from typing import Dict
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
        """
        Test that _public_repos_url returns the correct URL from org payload.
        """
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

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: unittest.mock.Mock) -> None:
        """Test that public_repos returns the correct list of repos."""

        test_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]
        test_repos_url = "https://api.github.com/orgs/testorg/repos"

        mock_get_json.return_value = test_repos_payload

        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_repos_url

            client = GithubOrgClient("testorg")

            repos = client.public_repos()

            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_repos)

            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_repos_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(
        self,
        repo: Dict,
        license_key: str,
        expected: bool
    ) -> None:
        """
        Test that has_license correctly identifies license matches.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
