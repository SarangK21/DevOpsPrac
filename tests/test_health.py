from health_monitor import check_status


def test_status_is_ok():

    result = check_status(50, 80)

    assert result == "OK"


def test_status_is_warning():

    result = check_status(90, 80)

    assert result == "WARNING"
