import re

from release_notes.tests.conftest import version

version_expected_values = {
    "None": "0.0.1",
    "major": "1.0.0",
    "minor": "0.1.0",
    "patch": "0.0.1",
}


def test_current_version():
    current_version = version.current_version
    assert isinstance(current_version, str)
    assert re.match(r"\d*.\d*.\d*", str(version))


def test_increment_version():
    current_version = "0.0.0"
    for version_type, expected_value in version_expected_values.items():
        new_version = version.increment_version(current_version, version_type)
        assert isinstance(new_version, str)
        assert re.match(r"\d*.\d*.\d*", str(new_version))
        assert new_version == expected_value
