from src.balls_bins import expected_empty_bins


def test_expected_empty_bins():
    assert abs(expected_empty_bins(0, 10) - 10) < 1e-9  # no balls -> all empty
    val = expected_empty_bins(10, 10)
    assert 0 <= val <= 10
