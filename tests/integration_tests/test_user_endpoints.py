def test_delete_user_success(testing_app, valid_user_id):
    response = testing_app.delete(f"/user/{valid_user_id}")
    assert response.status_code == 200


def test_delete_user_fail(testing_app, valid_user_id):
    response = testing_app.delete(f"/user/{valid_user_id}")
    assert response.status_code == 200

    second_response = testing_app.delete(f"/user/{valid_user_id}")
    assert second_response.status_code == 404
    assert second_response.json() == "User does not exist"


def test_delete_invalid_user_id_fails(testing_app, invalid_user_id):
    second_response = testing_app.delete(f"/user/{invalid_user_id}")
    assert second_response.status_code == 404
    assert second_response.json() == "User does not exist"


def test_put_user_returns_correct_results(testing_app, sample_full_user_profile):
    user_id = 1
    response = testing_app.put(
        f"/user/{user_id}", json=sample_full_user_profile.model_dump()
    )
    assert response.status_code == 200


def test_put_twice_user_returns_correct_results(testing_app, sample_full_user_profile):
    user_id = 1
    response = testing_app.put(
        f"/user/{user_id}", json=sample_full_user_profile.model_dump()
    )
    assert response.status_code == 200

    second_response = testing_app.put(
        f"/user/{user_id}", json=sample_full_user_profile.model_dump()
    )

    assert second_response.status_code == 200


def test_get_valid_user_returns_correct_result(testing_app, valid_user_id):
    response = testing_app.get(f"/user/{valid_user_id}")

    assert response.status_code == 200
    assert response.json()["long_bio"] == "This is my longer bio"


def test_rate_limit_works(testing_app, testing_rate_limit, valid_user_id):
    for i in range(testing_rate_limit * 2):
        response = testing_app.get(f"/user/{valid_user_id}")
        if "X-app-rate-limit" not in response.headers:
            assert response.status_code == 429
