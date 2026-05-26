"""
Tests for the POST /activities/{activity_name}/unregister endpoint.
Uses the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering students from activities."""

    def test_unregister_existing_participant_success(self, client, reset_activities):
        """
        GIVEN a student is registered for an activity
        WHEN the student unregisters
        THEN the unregistration should succeed and return a success message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_removes_participant_from_activity(self, client, reset_activities):
        """
        GIVEN a student is registered for an activity
        WHEN the student unregisters
        THEN the student should no longer appear in the activity's participants list
        """
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"  # Already registered

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        activities_response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = activities_response.json()
        assert email not in data[activity_name]["participants"]

    def test_unregister_nonexistent_participant_fails(self, client, reset_activities):
        """
        GIVEN a student is not registered for an activity
        WHEN the student attempts to unregister
        THEN the unregistration should fail with a 400 error
        """
        # Arrange
        activity_name = "Chess Club"
        email = "unregistered@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "not registered" in data["detail"]

    def test_unregister_nonexistent_activity_fails(self, client, reset_activities):
        """
        GIVEN an activity does not exist
        WHEN a student attempts to unregister
        THEN the unregistration should fail with a 404 error
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    def test_unregister_then_signup_again_success(self, client, reset_activities):
        """
        GIVEN a student has unregistered from an activity
        WHEN the student signs up again
        THEN the signup should succeed
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"

        # Act - First unregister
        unregister_response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        assert unregister_response.status_code == 200

        # Act - Then signup again
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert signup_response.status_code == 200
        activities_response = client.get("/activities")
        data = activities_response.json()
        assert email in data[activity_name]["participants"]

    def test_unregister_decreases_participant_count(self, client, reset_activities):
        """
        GIVEN an activity with multiple participants
        WHEN one participant unregisters
        THEN the participant count should decrease by one
        """
        # Arrange
        activity_name = "Chess Club"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        email = "michael@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity_name]["participants"])

        # Assert
        assert response.status_code == 200
        assert final_count == initial_count - 1
