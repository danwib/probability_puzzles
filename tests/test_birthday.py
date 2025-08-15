from src.birthday import prob_shared_birthday


def test_small_groups():
    assert abs(prob_shared_birthday(1)) == 0.0
    assert prob_shared_birthday(23) > 0.5  # classic result ~0.507


def test_bounds():
    assert prob_shared_birthday(400, days=365) == 1.0
