"""
Tests for yara_scanner.py
Run with: pytest tests/test_yara_scanner.py -v
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from yara_scanner import scan_file, scan_data, combine_results

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "..", "test_files")


def test_eicar_file_is_detected():
    path = os.path.join(TEST_FILES_DIR, "eicar_test.txt")
    if not os.path.exists(path):
        pytest.skip("eicar_test.txt not present - add it manually, see README")
    result = scan_file(path)
    assert result["matched"] is True
    assert any(r["rule"] == "EICAR_Test_File" for r in result["rules_matched"])


def test_clean_file_has_no_matches():
    path = os.path.join(TEST_FILES_DIR, "clean_sample.txt")
    result = scan_file(path)
    assert result["matched"] is False
    assert result["rules_matched"] == []


def test_ransomware_note_is_detected():
    part1 = "your files have been " + "encrypted"
    part2 = "README" + "_DECRYPT"
    content = part1 + ", see " + part2 + " for instructions"

    result = scan_data(content)
    assert result["matched"] is True
    matched_rules = [r["rule"] for r in result["rules_matched"]]
    assert "Ransomware_Note_Indicators" in matched_rules
    ransomware_hit = next(r for r in result["rules_matched"] if r["rule"] == "Ransomware_Note_Indicators")
    assert ransomware_hit["category"] == "ransomware"
    assert len(ransomware_hit["matched_strings"]) > 0


def test_webshell_php_is_detected():
    tag_open = "<" + "?php "
    call1 = "sys" + "tem" + "($_GET['cmd']); "
    call2 = "ev" + "al(" + "base64_" + "decode" + "($_POST['x'])); "
    tag_close = "?" + ">"
    content = tag_open + call1 + call2 + tag_close

    result = scan_data(content)
    assert result["matched"] is True
    matched_rules = [r["rule"] for r in result["rules_matched"]]
    assert "Webshell_PHP_Generic" in matched_rules


def test_combine_results_marks_suspicious_when_matched():
    fake_static_analysis = {"file_hash": {"sha256": "abc123"}, "metadata": {}}
    yara_result = {
        "file": "eicar_test.txt",
        "matched": True,
        "rules_matched": [{
            "rule": "EICAR_Test_File",
            "category": "test",
            "severity": "test",
            "description": "",
            "matched_strings": [],
        }],
    }
    combined = combine_results(fake_static_analysis, yara_result)
    assert combined["verdict"] == "suspicious"
    assert combined["static_analysis"] == fake_static_analysis


def test_combine_results_marks_clean_when_no_match():
    fake_static_analysis = {"file_hash": {"sha256": "def456"}, "metadata": {}}
    yara_result = {"file": "clean_sample.txt", "matched": False, "rules_matched": []}
    combined = combine_results(fake_static_analysis, yara_result)
    assert combined["verdict"] == "clean"