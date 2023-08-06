from unittest import mock
import pytest
from collect_framework_test.src.check_letters.main import count_unique_chars, count_unique_chars2
from collect_framework_test.src.check_letters.__main__ import main


@pytest.mark.parametrize("text, expected_result", [
        ("abbbccdf", 3),
        ("abcddd eefffgh", 6),
        ("a1111bcd efg!h", 10),
        ("", 0),
        ("hello world", 6),
        ("aaaaaaa", 0)
    ])
def test_count_unique_chars(text, expected_result):
    cache = {}
    assert count_unique_chars(text, cache) == expected_result

@pytest.mark.parametrize("text, expected_result", [
        ("abbbccdf", 3),
        ("abcddd eefffgh", 6),
        ("a1111bcd efg!h", 10),
        ("", 0),
        ("hello world", 6),
        ("aaaaaaa", 0)
    ])
def test_count_unique_chars2(text, expected_result):
    assert count_unique_chars2(text) == expected_result

def test_count_unique_chars_from_string(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--string", "abcddd eefffgh"])
    with mock.patch("builtins.open", mock.mock_open(read_data="abcddd eefffgh")) as mock_file:
        cache = {}
        count_unique_chars_mock = mock.Mock()
        monkeypatch.setattr("collect_framework_test.src.check_letters.__main__.count_unique_chars", count_unique_chars_mock)
        count_unique_chars2_mock = mock.Mock()
        monkeypatch.setattr("collect_framework_test.src.check_letters.__main__.count_unique_chars2", count_unique_chars2_mock)
        main()
    assert count_unique_chars_mock.called == True
    count_unique_chars_mock.assert_called_with("abcddd eefffgh", cache)
    assert mock_file.called == False
    assert count_unique_chars2_mock.called == True
    assert count_unique_chars2_mock.call_args[0][0] == "abcddd eefffgh"

def test_count_unique_chars_from_file(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "--file", "test_file.txt"])
    with mock.patch("builtins.open", mock.mock_open(read_data="abcddd eefffgh")) as mock_file:
        count_unique_chars_mock = mock.Mock()
        monkeypatch.setattr("collect_framework_test.src.check_letters.__main__.count_unique_chars", count_unique_chars_mock)
        count_unique_chars2_mock = mock.Mock()
        monkeypatch.setattr("collect_framework_test.src.check_letters.__main__.count_unique_chars2", count_unique_chars2_mock)
        main()
    assert mock_file.called == True
    assert count_unique_chars_mock.called == True
    count_unique_chars_mock.assert_called_with("abcddd eefffgh", {})
    assert count_unique_chars2_mock.called == True
    assert count_unique_chars2_mock.call_args[0][0] == "abcddd eefffgh"