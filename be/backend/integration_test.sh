#!/bin/sh
# Integration test script — run while Flask server is running on localhost:5000
set -e

BASE="http://localhost:5000/api"
TOKEN=$(grep APP_TOKEN "$(dirname "$0")/.env" | cut -d= -f2)
PASS=0
FAIL=0

check() {
    label="$1"
    expected="$2"
    actual="$3"
    if echo "$actual" | grep -q "$expected"; then
        echo "  PASS  $label"
        PASS=$((PASS + 1))
    else
        echo "  FAIL  $label"
        echo "        expected to contain: $expected"
        echo "        got: $actual"
        FAIL=$((FAIL + 1))
    fi
}

echo ""
echo "=== Health ==="
r=$(curl -s "$BASE/health")
echo "$r"
check "model_loaded=true" '"model_loaded":true' "$r"
check "status=success"    '"status":"success"'  "$r"

echo ""
echo "=== Auth ==="
r=$(curl -s "$BASE/jobs")
check "no-token → UNAUTHORIZED" "UNAUTHORIZED" "$r"

r=$(curl -s -H "Authorization: Bearer wrongtoken" "$BASE/jobs")
check "wrong-token → UNAUTHORIZED" "UNAUTHORIZED" "$r"

echo ""
echo "=== Jobs list ==="
r=$(curl -s -H "Authorization: Bearer $TOKEN" "$BASE/jobs")
echo "$r"
check "jobs array present" '"jobs":' "$r"
check "status=success"     '"status":"success"' "$r"

r=$(curl -s -H "Authorization: Bearer $TOKEN" "$BASE/jobs?industry=Finance")
check "industry filter Finance" '"industry":"Finance"' "$r"

r=$(curl -s -H "Authorization: Bearer $TOKEN" "$BASE/jobs?page=1&limit=1")
check "limit=1 returns one job" '"limit":1' "$r"

echo ""
echo "=== Job detail ==="
r=$(curl -s -H "Authorization: Bearer $TOKEN" "$BASE/jobs/IT00001")
echo "$r"
check "IT00001 title present"   '"title":'          "$r"
check "required_skills is array" '"required_skills":\[' "$r"

r=$(curl -s -H "Authorization: Bearer $TOKEN" "$BASE/jobs/jd-9999")
check "missing job → JOB_NOT_FOUND" "JOB_NOT_FOUND" "$r"

echo ""
echo "=== Match endpoint — validation ==="
r=$(curl -s -X POST -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{}' "$BASE/match")
check "missing job_id → INVALID_INPUT" "INVALID_INPUT" "$r"

r=$(curl -s -X POST -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"job_id":"jd-9999","candidate_id":"c1","candidate_name":"Alice","cv_text":"Python developer"}' \
    "$BASE/match")
check "bad job_id → JOB_NOT_FOUND" "JOB_NOT_FOUND" "$r"

r=$(curl -s -X POST -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"job_id":"IT00001","candidate_id":"c1","candidate_name":"Alice","cv_text":"   "}' \
    "$BASE/match")
check "whitespace cv_text → INVALID_INPUT" "INVALID_INPUT" "$r"

echo ""
echo "=== Match endpoint — full pipeline ==="
CV="Saya adalah software engineer dengan 3 tahun pengalaman. Bachelor of Computer Science. Menguasai Python, SQL, REST API, Git, dan Docker. Pengalaman membangun backend services dan integrasi database."
r=$(curl -s -X POST -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d "{\"job_id\":\"IT00001\",\"candidate_id\":\"c-test-01\",\"candidate_name\":\"Test Candidate\",\"cv_text\":\"$CV\"}" \
    "$BASE/match")
echo "$r"
check "status=success"           '"status":"success"'       "$r"
check "score_comparison present" '"score_comparison":'      "$r"
check "breakdown present"        '"breakdown":'             "$r"
check "grade present"            '"grade":'                 "$r"
check "language_detected"        '"language_detected":'     "$r"
check "processing_time_ms"       '"processing_time_ms":'    "$r"
check "semantic_score float"     '"semantic_score":'        "$r"
check "keyword_score float"      '"keyword_score":'         "$r"
check "improvement present"      '"improvement":'           "$r"
check "matched_skills present"   '"matched_skills":'        "$r"
check "missing_skills present"   '"missing_skills":'        "$r"
check "years_detected"           '"years_detected":'        "$r"

echo ""
echo "=== Match endpoint — no token ==="
r=$(curl -s -X POST -H "Content-Type: application/json" \
    -d '{"job_id":"IT00001","candidate_id":"c1","candidate_name":"A","cv_text":"test"}' \
    "$BASE/match")
check "no token → UNAUTHORIZED" "UNAUTHORIZED" "$r"

echo ""
echo "========================================"
echo "Results: $PASS passed, $FAIL failed"
echo "========================================"
[ "$FAIL" -eq 0 ]
