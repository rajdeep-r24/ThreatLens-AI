"""
ThreatLens-AI - YARA & Signature Detection Engine
Member: Vamshi
Branch: feat/yara-signature-engine
"""

import os
import yara

RULES_PATH = os.path.join(os.path.dirname(__file__), "yara_rules", "custom_rules.yar")


def load_rules(rules_path: str = RULES_PATH):
    return yara.compile(filepath=rules_path)


def scan_file(target_path: str, rules_path: str = RULES_PATH) -> dict:
    rules = load_rules(rules_path)
    matches = rules.match(target_path)

    rules_matched = []
    for m in matches:
        matched_strings = []
        for string_match in m.strings:
            if hasattr(string_match, "instances"):
                identifier = string_match.identifier
                for instance in string_match.instances:
                    matched_data = instance.matched_data
                    try:
                        value = matched_data.decode("utf-8", errors="replace")
                    except Exception:
                        value = repr(matched_data)
                    matched_strings.append({
                        "identifier": identifier,
                        "offset": instance.offset,
                        "value": value,
                    })
            else:
                offset, identifier, matched_data = string_match
                try:
                    value = matched_data.decode("utf-8", errors="replace")
                except Exception:
                    value = repr(matched_data)
                matched_strings.append({
                    "identifier": identifier,
                    "offset": offset,
                    "value": value,
                })

        rules_matched.append({
            "rule": m.rule,
            "category": m.meta.get("category", "uncategorized"),
            "severity": m.meta.get("severity", "unknown"),
            "description": m.meta.get("description", ""),
            "matched_strings": matched_strings,
        })

    return {
        "file": os.path.basename(target_path),
        "matched": len(rules_matched) > 0,
        "rules_matched": rules_matched,
    }
def scan_data(data: str, rules_path: str = RULES_PATH) -> dict:
    """
    Scan raw text/bytes directly in memory, without writing to disk.
    Used in tests to avoid antivirus interference with temp files
    containing signature-like strings.
    """
    rules = load_rules(rules_path)
    if isinstance(data, str):
        data = data.encode("utf-8")
    matches = rules.match(data=data)

    rules_matched = []
    for m in matches:
        matched_strings = []
        for string_match in m.strings:
            if hasattr(string_match, "instances"):
                identifier = string_match.identifier
                for instance in string_match.instances:
                    matched_data = instance.matched_data
                    try:
                        value = matched_data.decode("utf-8", errors="replace")
                    except Exception:
                        value = repr(matched_data)
                    matched_strings.append({
                        "identifier": identifier,
                        "offset": instance.offset,
                        "value": value,
                    })
            else:
                offset, identifier, matched_data = string_match
                try:
                    value = matched_data.decode("utf-8", errors="replace")
                except Exception:
                    value = repr(matched_data)
                matched_strings.append({
                    "identifier": identifier,
                    "offset": offset,
                    "value": value,
                })

        rules_matched.append({
            "rule": m.rule,
            "category": m.meta.get("category", "uncategorized"),
            "severity": m.meta.get("severity", "unknown"),
            "description": m.meta.get("description", ""),
            "matched_strings": matched_strings,
        })

    return {
        "file": "in-memory",
        "matched": len(rules_matched) > 0,
        "rules_matched": rules_matched,
    }

def save_result_to_db(yara_result: dict, file_id, db_session=None):
    from models import YARAResult

    saved_rows = []
    for match in yara_result.get("rules_matched", []):
        row = YARAResult(
            file_id=file_id,
            rule_name=match["rule"],
            category=match["category"],
            severity=match["severity"],
            description=match["description"],
            matched_strings=str(match["matched_strings"]),
        )
        if db_session:
            db_session.add(row)
        saved_rows.append(row)

    if db_session:
        db_session.commit()

    return saved_rows


def combine_results(static_analysis_result: dict, yara_result: dict) -> dict:
    return {
        "file": yara_result.get("file"),
        "static_analysis": static_analysis_result,
        "yara": {
            "matched": yara_result.get("matched", False),
            "rules_matched": yara_result.get("rules_matched", []),
        },
        "verdict": "suspicious" if yara_result.get("matched") else "clean",
    }


if __name__ == "__main__":
    test_dir = os.path.join(os.path.dirname(__file__), "test_files")

    for filename in ["eicar_test.txt", "clean_sample.txt"]:
        path = os.path.join(test_dir, filename)
        if not os.path.exists(path):
            print(f"\nSkipping {filename} (not present)")
            continue
        result = scan_file(path)
        print(f"\nScanning: {filename}")
        print(result)