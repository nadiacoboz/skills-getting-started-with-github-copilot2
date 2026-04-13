"""
Tests for the Mergington High School Activities API.
Using the AAA (Arrange-Act-Assert) pattern for clarity.
"""


def test_get_activities(client):
    """Test fetching all activities returns correct data"""
    # Arrange
    expected_activity_count = 9
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(data) == expected_activity_count
    for activity_name in expected_activities:
        assert activity_name in data


def test_get_activity_details(client):
    """Test that activity details are returned correctly"""
    # Arrange
    activity_name = "Chess Club"
    expected_description = "Learn strategies and compete in chess tournaments"
    expected_schedule = "Fridays, 3:30 PM - 5:00 PM"
    expected_max_participants = 12
    expected_participant_count = 2
    
    # Act
    response = client.get("/activities")
    data = response.json()
    activity = data[activity_name]
    
    # Assert
    assert activity["description"] == expected_description
    assert activity["schedule"] == expected_schedule
    assert activity["max_participants"] == expected_max_participants
    assert len(activity["participants"]) == expected_participant_count


def test_signup_for_activity_success(client):
    """Test successfully signing up a student for an activity"""
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    initial_response = client.get("/activities")
    initial_participant_count = len(initial_response.json()[activity_name]["participants"])
    
    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={new_email}")
    verification_response = client.get("/activities")
    final_participants = verification_response.json()[activity_name]["participants"]
    
    # Assert
    assert signup_response.status_code == 200
    assert f"Signed up {new_email}" in signup_response.json()["message"]
    assert new_email in final_participants
    assert len(final_participants) == initial_participant_count + 1


def test_unregister_from_activity_success(client):
    """Test successfully unregistering a student from an activity"""
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"
    initial_response = client.get("/activities")
    initial_participant_count = len(initial_response.json()[activity_name]["participants"])
    
    # Act
    unregister_response = client.post(
        f"/activities/{activity_name}/unregister?email={email_to_remove}"
    )
    verification_response = client.get("/activities")
    final_participants = verification_response.json()[activity_name]["participants"]
    
    # Assert
    assert unregister_response.status_code == 200
    assert f"Unregistered {email_to_remove}" in unregister_response.json()["message"]
    assert email_to_remove not in final_participants
    assert len(final_participants) == initial_participant_count - 1


def test_signup_nonexistent_activity_returns_404(client):
    """Test signing up for a non-existent activity returns 404"""
    # Arrange
    nonexistent_activity = "Fake Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{nonexistent_activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_nonexistent_activity_returns_404(client):
    """Test unregistering from a non-existent activity returns 404"""
    # Arrange
    nonexistent_activity = "Fake Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{nonexistent_activity}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_already_registered_returns_400(client):
    """Test that a student cannot sign up twice for the same activity"""
    # Arrange
    activity_name = "Chess Club"
    # michael@mergington.edu is already registered for Chess Club
    already_registered_email = "michael@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={already_registered_email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_not_registered_returns_400(client):
    """Test that unregistering a non-registered student returns 400"""
    # Arrange
    activity_name = "Chess Club"
    unregistered_email = "notregistered@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister?email={unregistered_email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]
