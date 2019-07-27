import pytest  # noqa: F401; pylint: disable=unused-variable
import pixel_measure


@pytest.fixture
def _setup():
    # Put this in every function that requires a setup and teardown.
    Measurements = pixel_measure.Measurements
    Measurements.pos = [(10, 20), (10, 35)]
    Measurements.distances = [40.1, 10]
    yield Measurements
    # Teardown stuff here


def test_append(_setup):
    Measurements = _setup

    # Before "active"
    Measurements.append((50, 60))
    assert (Measurements.pos == [(10, 20), (10, 35)])

    # After "active"
    Measurements.is_active = True
    Measurements.append((50, 60))
    assert (Measurements.pos == [(10, 20), (10, 35), (50, 60)])


def test_compute_distance(_setup):
    Measurements = _setup
    Measurements.compute_distance()
    assert (Measurements.distances == [40.1, 10, 15])


def test_compute_ratio(_setup):
    Measurements = _setup
    ratio = Measurements.compute_ratio()
    assert (ratio == 4.01)

    Measurements.distances.append(20)
    ratio = Measurements.compute_ratio()
    assert (ratio == 1/2)
