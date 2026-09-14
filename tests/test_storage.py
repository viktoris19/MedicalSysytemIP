import os
import tempfile
from storage import load_data, save_data


def test_load_data_file_not_found():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "not_exists.json")
        data = load_data(filename, {"default": True})
        assert data == {"default": True}


def test_save_and_load_data():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")
        test_data = {"key": "value", "number": 42}

        assert save_data(filename, test_data) is True
        assert os.path.exists(filename)

        loaded_data = load_data(filename)
        assert loaded_data == test_data


def test_load_data_corrupted():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "corrupted.json")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("this is not valid json {")

        data = load_data(filename, {"default": True})
        assert data == {"default": True}


def test_load_data_returns_dict():
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = os.path.join(tmpdir, "test.json")

        test_data = {"key": "value"}
        save_data(filename, test_data)

        loaded = load_data(filename)
        assert isinstance(loaded, dict)
        assert loaded["key"] == "value"
