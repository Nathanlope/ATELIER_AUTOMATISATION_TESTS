import json
from tester.client import ApiClient

client = ApiClient("https://api.ipify.org", timeout=2, max_retries=1)


def test_status_200_json():
    r = client.get(params={"format": "json"})
    latency = r.get("latency_ms")
    if not r["ok"]:
        return {"name": "test_status_200_json", "status": "FAIL", "latency_ms": None, "details": r["error"]}
    ok = r["status_code"] == 200
    return {
        "name": "test_status_200_json",
        "status": "PASS" if ok else "FAIL",
        "latency_ms": latency,
        "details": None if ok else f"status={r['status_code']}",
    }


def test_content_type_json():
    r = client.get(params={"format": "json"})
    if not r["ok"]:
        return {"name": "test_content_type_json", "status": "FAIL", "latency_ms": None, "details": r["error"]}
    ct = r["headers"].get("Content-Type", "")
    ok = "application/json" in ct
    return {
        "name": "test_content_type_json",
        "status": "PASS" if ok else "FAIL",
        "latency_ms": r["latency_ms"],
        "details": None if ok else f"Content-Type={ct}",
    }


def test_schema_ip_field():
    r = client.get(params={"format": "json"})
    if not r["ok"]:
        return {"name": "test_schema_ip_field", "status": "FAIL", "latency_ms": None, "details": r["error"]}
    try:
        data = json.loads(r["text"])
        ok = "ip" in data and isinstance(data["ip"], str) and len(data["ip"]) > 0
        details = None if ok else "champ 'ip' manquant ou invalide"
    except ValueError:
        ok = False
        details = "réponse non JSON"
    return {"name": "test_schema_ip_field", "status": "PASS" if ok else "FAIL", "latency_ms": r["latency_ms"], "details": details}


def test_plain_text_default():
    r = client.get()  # sans format=json
    if not r["ok"]:
        return {"name": "test_plain_text_default", "status": "FAIL", "latency_ms": None, "details": r["error"]}
    ok = r["status_code"] == 200 and "." in r["text"]
    return {
        "name": "test_plain_text_default",
        "status": "PASS" if ok else "FAIL",
        "latency_ms": r["latency_ms"],
        "details": None if ok else f"réponse inattendue: {r['text'][:50]}",
    }


def test_invalid_endpoint_404():
    r = client.get(path="/invalidpath")
    if not r["ok"]:
        return {"name": "test_invalid_endpoint_404", "status": "FAIL", "latency_ms": None, "details": r["error"]}
    ok = r["status_code"] in (404, 400)
    return {
        "name": "test_invalid_endpoint_404",
        "status": "PASS" if ok else "FAIL",
        "latency_ms": r["latency_ms"],
        "details": None if ok else f"status={r['status_code']} attendu 404/400",
    }


ALL_TESTS = [
    test_status_200_json,
    test_content_type_json,
    test_schema_ip_field,
    test_plain_text_default,
    test_invalid_endpoint_404,
]
