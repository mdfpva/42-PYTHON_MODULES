#!/bin/bash
# =============================================================
#  Python Module 04 — Data Archivist (File I/O & Context Managers)
#  Deep tester — ex0 to ex3
#  Usage: bash tester_mod04.sh /path/to/student/repo
# =============================================================

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; MAGENTA='\033[0;35m'; BOLD='\033[1m'; RESET='\033[0m'
pass=0; fail=0; warn=0

ok()   { echo -e "  ${GREEN}[OK]${RESET}   $1"; pass=$((pass+1)); }
ko()   { echo -e "  ${RED}[KO]${RESET}   $1"; fail=$((fail+1)); }
wa()   { echo -e "  ${YELLOW}[!!]${RESET}   $1"; warn=$((warn+1)); }
hdr()  { echo -e "\n${BOLD}${CYAN}══════════════════════════════════════${RESET}\n${BOLD}${CYAN}  $1${RESET}\n${BOLD}${CYAN}══════════════════════════════════════${RESET}"; }
info() { echo -e "  ${MAGENTA}[>>]${RESET}   $1"; }

line_has()    { echo "$2" | grep -Fq  -- "$3" && ok "$1" || { ko "$1"; info "want (substring): $3"; }; }
line_exact()  { echo "$2" | grep -Fxq -- "$3" && ok "$1" || { ko "$1"; info "want (EXACT line): $3"; }; }
line_absent() { echo "$2" | grep -Fq  -- "$3" && ko "$1 (found forbidden: '$3')" || ok "$1"; }

REPO="${1:-$(pwd)}"
echo -e "${BOLD}${CYAN}\n╔══════════════════════════════════════╗\n║ Python Mod 04 — Data Archivist Tester ║\n╚══════════════════════════════════════╝${RESET}"
echo -e "Repo: ${BOLD}$REPO${RESET}"
python3 -m flake8 --version &>/dev/null || pip install flake8 --break-system-packages -q
python3 -m mypy --version   &>/dev/null || pip install mypy  --break-system-packages -q

run_py() { timeout 8 python3 "$@" 2>&1; }

check_flake8() { local b; b=$(python3 -m flake8 "$1" 2>&1); [ -z "$b" ] && ok "flake8 — no errors" || { ko "flake8 errors:"; echo "$b"|head -6|sed 's/^/      /'; }; }
check_mypy()   { local e; e=$(python3 -m mypy "$1" --ignore-missing-imports 2>&1|grep "error:"|head -5); [ -z "$e" ] && ok "mypy — no errors" || { ko "mypy errors:"; echo "$e"|sed 's/^/      /'; }; }
check_hints()  {
  local o; o=$(python3 -c "
import ast
t=ast.parse(open('$1').read()); miss=[]
for n in ast.walk(t):
    if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):
        if n.returns is None or not all(a.annotation is not None for a in n.args.args if a.arg not in ('self','cls')):
            miss.append(n.name)
print('MISSING:'+','.join(miss) if miss else 'OK')" 2>&1)
  echo "$o"|grep -q "^OK" && ok "type hints present" || ko "type hints: $o"; }

# 'with' rule: forbidden in ex0/ex1/ex2, required in ex3
check_no_with() { grep -qE "^[^#]*\bwith\b" "$1" && ko "uses 'with' — FORBIDDEN before ex3 (subject rule)" || ok "no 'with' statement (rule respected)"; }
check_uses_with() { grep -qE "^[^#]*\bwith\b" "$1" && ok "uses 'with' (required in ex3)" || ko "must use 'with' statement"; }
file_exists() { [ -f "$1" ] && ok "exists: $2" || ko "MISSING: $2"; }

EX0="$REPO/ex0/ft_ancient_text.py"; EX1="$REPO/ex1/ft_archive_creation.py"
EX2="$REPO/ex2/ft_stream_management.py"; EX3="$REPO/ex3/ft_vault_security.py"
FRAG=$'[FRAGMENT 001] Digital preservation protocols established 2087\n[FRAGMENT 002] Knowledge must survive the entropy wars\n[FRAGMENT 003] Every byte saved is a victory against oblivion'

# The tester is self-sufficient: it creates the support file it needs
# in each exercise directory, so it never depends on files that may be
# missing from the student's repo.
ensure_fragment() {
  local d="$1"
  [ -d "$d" ] || return 0
  if [ ! -f "$d/ancient_fragment.txt" ]; then
    printf '%s\n' "$FRAG" > "$d/ancient_fragment.txt"
    touch "$d/.frag_made"
  fi
}
ensure_fragment "$REPO/ex0"; ensure_fragment "$REPO/ex1"
ensure_fragment "$REPO/ex2"; ensure_fragment "$REPO/ex3"

# ═══════════════════════════════════════════════════════════
hdr "FILES"
file_exists "$EX0" "ex0/ft_ancient_text.py"
file_exists "$EX1" "ex1/ft_archive_creation.py"
file_exists "$EX2" "ex2/ft_stream_management.py"
file_exists "$EX3" "ex3/ft_vault_security.py"

# ═══════════════════════════════════════════════════════════
hdr "EX0 — ft_ancient_text.py (read & cat)"
if [ -f "$EX0" ]; then
  D=$(dirname "$EX0"); B=$(basename "$EX0")
  check_flake8 "$EX0"; check_mypy "$EX0"; check_hints "$EX0"; check_no_with "$EX0"
  grep -q "import sys" "$EX0" && ok "imports sys" || ko "must import sys"
  grep -qE "\.close\(\)" "$EX0" && ok "calls .close() explicitly" || wa "no explicit .close() — file may stay open without 'with'"

  O=$(cd "$D" && run_py "$B")
  line_has "no args: usage" "$O" "Usage: ft_ancient_text.py <file>"
  O=$(cd "$D" && run_py "$B" foo)
  line_has "header" "$O" "=== Cyber Archives Recovery ==="
  line_has "accessing foo" "$O" "Accessing file 'foo'"
  line_has "nonexistent: errno 2" "$O" "Error opening file 'foo': [Errno 2] No such file or directory: 'foo'"
  O=$(cd "$D" && run_py "$B" ancient_fragment.txt)
  line_has "valid: accessing" "$O" "Accessing file 'ancient_fragment.txt'"
  line_has "valid: fragment 001" "$O" "[FRAGMENT 001] Digital preservation protocols established 2087"
  line_has "valid: closed footer" "$O" "File 'ancient_fragment.txt' closed."
  # exact body: '---' must hug the content (no blank lines like the subject)
  EXACT0=$'=== Cyber Archives Recovery ===\nAccessing file \'ancient_fragment.txt\'\n---\n[FRAGMENT 001] Digital preservation protocols established 2087\n[FRAGMENT 002] Knowledge must survive the entropy wars\n[FRAGMENT 003] Every byte saved is a victory against oblivion\n---\nFile \'ancient_fragment.txt\' closed.'
  [ "$O" = "$EXACT0" ] && ok "valid: EXACT layout (no extra blank lines)" || { ko "valid: layout differs from subject"; diff <(printf '%s' "$EXACT0") <(printf '%s' "$O")|sed 's/^/      /'; }
  # empty file must not crash
  echo -n "" > "$D/.empty_test.txt"; OE=$(cd "$D" && run_py "$B" .empty_test.txt); rm -f "$D/.empty_test.txt"
  echo "$OE"|grep -qi "Traceback" && ko "empty file crashes" || ok "empty file: no crash"
fi

# ═══════════════════════════════════════════════════════════
hdr "EX1 — ft_archive_creation.py (transform + save)"
if [ -f "$EX1" ]; then
  D=$(dirname "$EX1"); B=$(basename "$EX1")
  check_flake8 "$EX1"; check_mypy "$EX1"; check_hints "$EX1"; check_no_with "$EX1"
  grep -qE "\binput\(" "$EX1" && ok "uses input() for prompt" || wa "no input() — ex1 expects input() (ex2 replaces it)"

  O=$(cd "$D" && printf "\n" | run_py "$B" ancient_fragment.txt)
  line_has "header preservation" "$O" "=== Cyber Archives Recovery & Preservation ==="
  line_has "transform header" "$O" "Transform data:"
  line_has "line 1 has #" "$O" "[FRAGMENT 001] Digital preservation protocols established 2087#"
  line_has "line 3 has #" "$O" "[FRAGMENT 003] Every byte saved is a victory against oblivion#"
  echo "$O" | grep -qx "#" && ko "transform has a stray '#' line (each line must end with #, no extra)" || ok "no stray '#' line in transform"
  line_has "empty input: not saving" "$O" "Not saving data."

  TMP="$D/.tester_out.txt"; rm -f "$TMP"
  O=$(cd "$D" && printf "%s\n" ".tester_out.txt" | run_py "$B" ancient_fragment.txt)
  line_has "save: saving msg" "$O" "Saving data to"
  if [ -f "$TMP" ]; then
    ok "save: file created"
    grep -q "2087#$" "$TMP" && ok "saved content: # appended per line" || ko "saved file missing # markers"
    [ "$(tail -1 "$TMP")" = "[FRAGMENT 003] Every byte saved is a victory against oblivion#" ] \
      && ok "saved file: last line is oblivion# (no stray # line)" \
      || ko "saved file: wrong last line (stray '#'?): $(tail -1 "$TMP")"
  else ko "save: file NOT created"; fi
  rm -f "$TMP"
fi

# ═══════════════════════════════════════════════════════════
hdr "EX2 — ft_stream_management.py (stdin/stdout/stderr)"
if [ -f "$EX2" ]; then
  D=$(dirname "$EX2"); B=$(basename "$EX2")
  check_flake8 "$EX2"; check_mypy "$EX2"; check_hints "$EX2"; check_no_with "$EX2"
  grep -qE "\binput\(" "$EX2" && ko "uses input() — FORBIDDEN in ex2 (must use sys.stdin)" || ok "no input() (uses sys.stdin)"
  grep -q "sys.stdin"  "$EX2" && ok "uses sys.stdin"  || ko "must read via sys.stdin"
  grep -q "sys.stderr" "$EX2" && ok "uses sys.stderr" || ko "errors must go to sys.stderr"

  # error must go to STDERR only (disappears when 2>/dev/null)
  ERR_BOTH=$(cd "$D" && printf "\n" | run_py "$B" foo 2>&1)
  ERR_OUT=$(cd "$D" && printf "\n" | python3 "$B" foo 2>/dev/null)
  echo "$ERR_BOTH"|grep -q "\[STDERR\] Error opening file 'foo'" && ok "[STDERR] prefix on read error" || ko "missing [STDERR] prefix"
  echo "$ERR_OUT"|grep -q "Error opening file 'foo'" && ko "error leaks to STDOUT (must be stderr only)" || ok "error NOT on stdout (stderr only)"

  # write error → stderr + 'Data not saved.'
  O=$(cd "$D" && printf "/nonexistent_dir_xyz/f.txt\n" | run_py "$B" ancient_fragment.txt 2>&1)
  line_has "write error: [STDERR]" "$O" "[STDERR] Error opening file"
  line_has "write error: not saved" "$O" "Data not saved."
fi

# ═══════════════════════════════════════════════════════════
hdr "EX3 — ft_vault_security.py (with / context manager)"
if [ -f "$EX3" ]; then
  D=$(dirname "$EX3"); B=$(basename "$EX3")
  check_flake8 "$EX3"; check_mypy "$EX3"; check_hints "$EX3"; check_uses_with "$EX3"
  grep -qE "def secure_archive\b" "$EX3" && ok "function named secure_archive()" \
    || { grep -qE "def secure_archives\b" "$EX3" && ko "function is 'secure_archives' — subject/output say 'secure_archive' (singular)" || ko "missing secure_archive()"; }

  # signature: file_name + optional action + optional content
  sig=$(python3 -c "
import ast
t=ast.parse(open('$EX3').read())
for n in ast.walk(t):
    if isinstance(n,ast.FunctionDef) and n.name.startswith('secure_archive'):
        d=len(n.args.defaults); a=[x.arg for x in n.args.args]
        print('ARGS',len(a),'DEFAULTS',d); break" 2>&1)
  echo "$sig"|grep -q "ARGS 3" && ok "3 params (file_name, action, content)" || wa "signature: $sig (expected file_name + 2 optional)"
  echo "$sig"|grep -q "DEFAULTS 2" && ok "2 optional params (defaults)" || wa "optional params: $sig"

  # return type tuple[bool, str]
  ret=$(python3 -c "
import importlib.util
spec=importlib.util.spec_from_file_location('m','$EX3'); m=importlib.util.module_from_spec(spec)
fn=None
try:
    spec.loader.exec_module(m)
except SystemExit: pass
fn=getattr(m,'secure_archive',None) or getattr(m,'secure_archives',None)
r=fn('/not/existing/file') if fn else None
print('RET', type(r).__name__, len(r) if isinstance(r,tuple) else '-', type(r[0]).__name__ if r else '-', type(r[1]).__name__ if r else '-')" 2>&1)
  echo "$ret"|grep -q "RET tuple 2 bool str" && ok "returns tuple[bool, str]" || ko "return type wrong: $ret (want tuple[bool,str])"

  O=$(cd "$D" && run_py "$B")
  line_has "header" "$O" "=== Cyber Archives Security ==="
  line_has "read nonexistent label" "$O" "Using 'secure_archive' to read from a nonexistent file:"
  line_has "read inaccessible label" "$O" "Using 'secure_archive' to read from an inaccessible file:"
  line_has "read regular label" "$O" "Using 'secure_archive' to read from a regular file:"
  line_has "write label" "$O" "Using 'secure_archive' to write previous content to a new file:"
  # tuple format must be (False, "...") not "False, ..."
  echo "$O"|grep -qE "^\(False, " && ok "False case printed as tuple (False, ...)" || ko "False case not printed as a tuple — subject shows (False, \"...\")"
  echo "$O"|grep -qE "^\(True, " && ok "True case printed as tuple (True, ...)" || ko "True case not printed as a tuple"
  line_has "write success content" "$O" "Content successfully written to file"
fi

# ═══════════════════════════════════════════════════════════
hdr "GENERAL"
PY=$(python3 --version 2>&1|grep -oE "[0-9]+\.[0-9]+"); MIN=$(echo "$PY"|cut -d. -f2)
[ "${MIN:-0}" -ge 10 ] && ok "Python $PY >= 3.10" || ko "Python $PY < 3.10"

# cleanup: remove only the support files THIS tester created
cleanup_fragment() { [ -f "$1/.frag_made" ] && rm -f "$1/ancient_fragment.txt" "$1/.frag_made"; }
cleanup_fragment "$REPO/ex0"; cleanup_fragment "$REPO/ex1"
cleanup_fragment "$REPO/ex2"; cleanup_fragment "$REPO/ex3"
rm -f "$REPO/ex3/new_file" "$REPO/ex1/.tester_out.txt" "$REPO/ex2/.tester_out.txt"
find "$REPO" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null

hdr "SUMMARY"
echo -e "\n  Total: $((pass+fail))    ${GREEN}Passed: $pass${RESET}"
[ "$fail" -gt 0 ] && echo -e "  ${RED}Failed: $fail${RESET}" || echo "  Failed: 0"
[ "$warn" -gt 0 ] && echo -e "  ${YELLOW}Warnings: $warn${RESET}"
echo ""
[ "$fail" -eq 0 ] && echo -e "${BOLD}${GREEN}  ✓ All tests passed!${RESET}\n" || echo -e "${BOLD}${RED}  ✗ Some tests failed — see above${RESET}\n"
