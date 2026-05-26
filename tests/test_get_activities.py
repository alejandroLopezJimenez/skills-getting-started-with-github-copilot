"""
Tests for the GET /activities endpoint.
Uses the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestGetActivities:
    """Test suite for retrieving activities."""

    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """
        GIVEN the API is running
        WHEN a GET request is made to /activities
        THEN all activities should be returned with correct data
        """
        # Arrange - Setup is handled by fixtures

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9  # 9 activities in the database
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_get_activities_contains_activity_structure(self, client, reset_activities):
        """
        GIVEN the API is running
        WHEN a GET request is made to /activities
        THEN each activity should have all required fields
        """
        # Arrange - Setup is handled by fixtures

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)

    def test_get_activities_shows_existing_participants(self, client, reset_activities):
        """
        GIVEN activities with existing participants
        WHEN a GET request is made to /activities
        THEN the participants list should show enrolled students
        """
        # Arrange - Setup is handled by fixtures

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in data["Chess Club"]["participants"]
        assert "emma@mergington.edu" in data["Programming Class"]["participants"]
