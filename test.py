import pytest  # noqa: F401; pylint: disable=unused-variable
import pixel_measure


def setup(request):
    # Put this in every function that requires a setup and teardown.
    Measurements = pixel_measure.Measurements
    Measurements.pos = [(10, 20), (30, 40)]
    Measurements.distances = [40.1, 10]
    yield Measurements
    # Teardown stuff here


def test_append(setup):
    Measurements = setup
    Measurements.append((50, 60))
    assert (Measurements.pos == [(10, 20), (30, 40), (50, 60)])


def test_compute_distance(setup):
    Measurements = setup
    Measurements.append((30, 45))
    Measurements.compute_distance()
    assert (Measurements.distances == [40.1, 10, 15])
