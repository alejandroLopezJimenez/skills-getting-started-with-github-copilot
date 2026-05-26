"""
Tests for the POST /activities/{activity_name}/signup endpoint.
Uses the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestSignupForActivity:
    """Test suite for signing up students for activities."""

    def test_signup_new_participant_success(self, client, reset_activities):
        """
        GIVEN an activity exists and a student is not yet registered
        WHEN the student signs up for the activity
        THEN the signup should succeed and return a success message
        """
        # Arrange
        activity_name = "Basketball Team"
        email = "new.student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant_to_activity(self, client, reset_activities):
        """
        GIVEN an activity with no participants
        WHEN a student signs up
        THEN the student should appear in the activity's participants list
        """
        # Arrange
        activity_name = "Swimming Club"
        email = "swimmer@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        activities_response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = activities_response.json()
        assert email in data[activity_name]["participants"]

    def test_signup_duplicate_registration_fails(self, client, reset_activities):
        """
        GIVEN a student is already registered for an activity
        WHEN the student attempts to sign up again
        THEN the signup should fail with a 400 error
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_nonexistent_activity_fails(self, client, reset_activities):
        """
        GIVEN an activity does not exist
        WHEN a student attempts to sign up
        THEN the signup should fail with a 404 error
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    def test_signup_multiple_different_students_success(self, client, reset_activities):
        """
        GIVEN an activity exists
        WHEN multiple different students sign up
        THEN all should be added to the participants list
        """
        # Arrange
        activity_name = "Art Studio"
        emails = ["artist1@mergington.edu", "artist2@mergington.edu", "artist3@mergington.edu"]

        # Act
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # Assert
        activities_response = client.get("/activities")
        data = activities_response.json()
        for email in emails:
            assert email in data[activity_name]["participants"]
        assert len(data[activity_name]["participants"]) == 3
