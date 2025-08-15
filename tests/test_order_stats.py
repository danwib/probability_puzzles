from src.order_stats import expected_kth_uniform, expected_max_uniform


def test_uniform_order_stats():
    assert abs(expected_max_uniform(1) - 0.5) < 1e-9
    assert abs(expected_max_uniform(2) - 2 / 3) < 1e-9
    assert abs(expected_kth_uniform(10, 1) - 1 / 11) < 1e-9
    assert abs(expected_kth_uniform(10, 10) - 10 / 11) < 1e-9
