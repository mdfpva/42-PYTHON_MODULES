#!/bin/bash
# ================================================================
#  The Codex — Python Import Mysteries | Automated Tester v1.0
#  Run from the project root (same dir as ft_alembic_0.py).
#  Usage: bash tester_codex.sh
# ================================================================

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; DIM='\033[2m'; NC='\033[0m'

PASS=0; FAIL=0

# ── helpers ─────────────────────────────────────────────────────

banner() {
    echo -e "\n${CYAN}${BOLD}── $1 ─────────────────────────────────────────────${NC}"
}

ok() {
    echo -e "  ${GREEN}[OK]${NC} $1"
    PASS=$((PASS + 1))
}

ko() {
    echo -e "  ${RED}[KO]${NC} $1"
    [ -n "$2" ] && echo -e "       ${DIM}↳ $2${NC}"
    FAIL=$((FAIL + 1))
}

info() {
    echo -e "  ${YELLOW}[··]${NC} ${DIM}$1${NC}"
}

chk_file() { [ -f "$1" ] && ok "file: $1"  || ko "file: $1"  "NOT FOUND"; }
chk_dir()  { [ -d "$1" ] && ok "dir:  $1/" || ko "dir:  $1/" "NOT FOUND"; }

# Run a script, capture stdout+stderr, check for fixed string
run_has() {
    local label="$1" needle="$2" script="$3"
    local out; out=$(python3 "$script" 2>&1)
    if printf '%s\n' "$out" | grep -qF "$needle"; then
        ok "$label"
    else
        ko "$label" "substring not found: ›${needle}‹"
        printf '%s\n' "$out" | head -6 | sed 's/^/         /'
    fi
}

# Run inline Python, check output for fixed string
py_has() {
    local label="$1" needle="$2" code="$3"
    local out; out=$(python3 -c "$code" 2>&1)
    if printf '%s\n' "$out" | grep -qF "$needle"; then
        ok "$label"
    else
        ko "$label" "substring not found: ›${needle}‹"
        printf '%s\n' "$out" | head -3 | sed 's/^/         /'
    fi
}

run_ok() {
    python3 "$1" >/dev/null 2>&1 \
        && ok  "$2 — exits 0" \
        || ko  "$2 — exits 0" "non-zero exit code"
}

run_fail() {
    python3 "$1" >/dev/null 2>&1 \
        && ko  "$2 — crashes (expected)" "script exited 0; should crash" \
        || ok  "$2 — crashes (expected)"
}

# Grep a file for an extended-regex pattern
file_has() {
    grep -qE "$2" "$3" 2>/dev/null \
        && ok "$1" \
        || ko "$1" "pattern not found: $2"
}

# ── preflight ────────────────────────────────────────────────────

command -v python3 >/dev/null 2>&1 || { echo -e "${RED}ERROR: python3 not found.${NC}"; exit 1; }

echo -e "${CYAN}${BOLD}"
echo "  ╔═══════════════════════════════════════════════════╗"
echo "  ║   The Codex — Python Import Mysteries  Tester    ║"
echo "  ║                      v1.0                        ║"
echo "  ╚═══════════════════════════════════════════════════╝"
echo -e "${NC}  ${DIM}Python : $(python3 --version 2>&1)${NC}"
echo -e   "  ${DIM}Dir    : $(pwd)${NC}"

# ================================================================
# 1 · FILE STRUCTURE
# ================================================================
banner "1 · File Structure"

chk_dir  alchemy
chk_file alchemy/__init__.py
chk_file alchemy/elements.py
chk_file alchemy/potions.py
chk_dir  alchemy/grimoire
chk_file alchemy/grimoire/__init__.py
chk_file alchemy/grimoire/light_spellbook.py
chk_file alchemy/grimoire/light_validator.py
chk_file alchemy/grimoire/dark_spellbook.py
chk_file alchemy/grimoire/dark_validator.py
chk_dir  alchemy/transmutation
chk_file alchemy/transmutation/__init__.py
chk_file alchemy/transmutation/recipes.py
chk_file elements.py
for n in 0 1 2 3 4 5; do chk_file "ft_alembic_$n.py";      done
for n in 0 1;          do chk_file "ft_distillation_$n.py"; done
for n in 0 1;          do chk_file "ft_kaboom_$n.py";       done
for n in 0 1 2;        do chk_file "ft_transmutation_$n.py"; done

# ================================================================
# 2 · MODULE CONTENT
# ================================================================
banner "2 · Module Content"

file_has "elements.py       → def create_fire"               "def create_fire"                       elements.py
file_has "elements.py       → def create_water"              "def create_water"                      elements.py
file_has "alchemy/elements  → def create_earth"              "def create_earth"                      alchemy/elements.py
file_has "alchemy/elements  → def create_air"                "def create_air"                        alchemy/elements.py
file_has "alchemy/potions   → def healing_potion"            "def healing_potion"                    alchemy/potions.py
file_has "alchemy/potions   → def strength_potion"           "def strength_potion"                   alchemy/potions.py
file_has "recipes.py        → def lead_to_gold"              "def lead_to_gold"                      alchemy/transmutation/recipes.py
file_has "recipes.py        → has absolute import"           "^(import alchemy|from alchemy)"        alchemy/transmutation/recipes.py
file_has "recipes.py        → has relative import"           "^from \."                              alchemy/transmutation/recipes.py
file_has "alchemy/__init__  → exposes create_air"            "create_air"                            alchemy/__init__.py
file_has "alchemy/__init__  → exposes heal alias"            "heal"                                  alchemy/__init__.py
file_has "light_spellbook   → allowed_ingredients fn"        "def light_spell_allowed_ingredients"   alchemy/grimoire/light_spellbook.py
file_has "light_spellbook   → light_spell_record fn"         "def light_spell_record"                alchemy/grimoire/light_spellbook.py
file_has "light_validator   → validate_ingredients fn"       "def validate_ingredients"              alchemy/grimoire/light_validator.py
file_has "dark_spellbook    → dark_spell_record fn"          "def dark_spell_record"                 alchemy/grimoire/dark_spellbook.py
file_has "dark_validator    → validate_ingredients fn"       "def validate_ingredients"              alchemy/grimoire/dark_validator.py
file_has "dark_spellbook    → imports dark_validator"        "dark_validator"                        alchemy/grimoire/dark_spellbook.py
file_has "dark_validator    → imports dark_spellbook"        "dark_spellbook"                        alchemy/grimoire/dark_validator.py

# Verify alchemy module interface directly
py_has "alchemy module → create_air accessible" \
    "Air element created" \
    "import alchemy; print(alchemy.create_air())"

py_has "alchemy module → create_earth NOT exposed (AttributeError)" \
    "AttributeError" \
    "import alchemy
try:
    alchemy.create_earth()
except AttributeError as e:
    print('AttributeError:', e)"

# Verify heal alias works through alchemy module
py_has "alchemy module → heal() alias works" \
    "Healing potion" \
    "import alchemy; print(alchemy.heal())"

# ================================================================
# 3 · PART I — THE ALEMBIC
# ================================================================
banner "3 · Part I: The Alembic"

# ── ft_alembic_0 — import elements ──
echo -e "  ${DIM}ft_alembic_0  (import elements)${NC}"
run_has "[alembic_0] header"         "=== Alembic 0 ==="     ft_alembic_0.py
run_has "[alembic_0] Fire created"   "Fire element created"  ft_alembic_0.py
file_has "[alembic_0] import style"  "^import elements( |$)" ft_alembic_0.py
run_ok   ft_alembic_0.py            "[alembic_0]"

# ── ft_alembic_1 — from elements import ──
echo -e "  ${DIM}ft_alembic_1  (from elements import)${NC}"
run_has "[alembic_1] header"         "=== Alembic 1 ==="       ft_alembic_1.py
run_has "[alembic_1] Water created"  "Water element created"   ft_alembic_1.py
file_has "[alembic_1] import style"  "^from elements import"   ft_alembic_1.py
run_ok   ft_alembic_1.py            "[alembic_1]"

# ── ft_alembic_2 — import alchemy.elements ──
echo -e "  ${DIM}ft_alembic_2  (import alchemy.elements)${NC}"
run_has "[alembic_2] header"         "=== Alembic 2 ==="          ft_alembic_2.py
run_has "[alembic_2] Earth created"  "Earth element created"      ft_alembic_2.py
file_has "[alembic_2] import style"  "^import alchemy\.elements"  ft_alembic_2.py
run_ok   ft_alembic_2.py            "[alembic_2]"

# ── ft_alembic_3 — from alchemy.elements import ──
echo -e "  ${DIM}ft_alembic_3  (from alchemy.elements import)${NC}"
run_has "[alembic_3] header"         "=== Alembic 3 ==="               ft_alembic_3.py
run_has "[alembic_3] Air created"    "Air element created"             ft_alembic_3.py
file_has "[alembic_3] import style"  "^from alchemy\.elements import"  ft_alembic_3.py
run_ok   ft_alembic_3.py            "[alembic_3]"

# ── ft_alembic_4 — import alchemy (create_earth hidden, partial crash) ──
echo -e "  ${DIM}ft_alembic_4  (import alchemy — create_earth hidden, intentional crash)${NC}"
run_has "[alembic_4] header"         "=== Alembic 4 ==="    ft_alembic_4.py
run_has "[alembic_4] Air created"    "Air element created"  ft_alembic_4.py
run_has "[alembic_4] AttributeError" "AttributeError"       ft_alembic_4.py
file_has "[alembic_4] import style"  "^import alchemy( |$)" ft_alembic_4.py
info "alembic_4: exit code not tested — catching exception is optional (§IV.1)"

# ── ft_alembic_5 — from alchemy import ──
echo -e "  ${DIM}ft_alembic_5  (from alchemy import)${NC}"
run_has "[alembic_5] header"         "=== Alembic 5 ==="    ft_alembic_5.py
run_has "[alembic_5] Air created"    "Air element created"  ft_alembic_5.py
file_has "[alembic_5] import style"  "^from alchemy import" ft_alembic_5.py
run_ok   ft_alembic_5.py            "[alembic_5]"

# ================================================================
# 4 · PART II — DISTILLATION
# ================================================================
banner "4 · Part II: Distillation"

SP="Strength potion brewed with 'Fire element created' and 'Water element created'"
HP="Healing potion brewed with 'Earth element created' and 'Air element created'"

# ── ft_distillation_0 — from alchemy.potions import ──
echo -e "  ${DIM}ft_distillation_0  (from alchemy.potions import)${NC}"
run_has "[dist_0] header"            "=== Distillation 0 ===" ft_distillation_0.py
run_has "[dist_0] strength_potion"   "$SP"                    ft_distillation_0.py
run_has "[dist_0] healing_potion"    "$HP"                    ft_distillation_0.py
file_has "[dist_0] import style"     "^from alchemy\.potions import" ft_distillation_0.py
run_ok   ft_distillation_0.py       "[dist_0]"

# ── ft_distillation_1 — import alchemy (via heal alias) ──
echo -e "  ${DIM}ft_distillation_1  (import alchemy, heal alias)${NC}"
run_has "[dist_1] header"            "=== Distillation 1 ===" ft_distillation_1.py
run_has "[dist_1] strength_potion"   "$SP"                    ft_distillation_1.py
run_has "[dist_1] heal alias"        "$HP"                    ft_distillation_1.py
file_has "[dist_1] import style"     "^import alchemy( |$)"  ft_distillation_1.py
run_ok   ft_distillation_1.py       "[dist_1]"

# ================================================================
# 5 · PART III — TRANSMUTATION
# ================================================================
banner "5 · Part III: The Great Transmutation"

GOLD="Recipe transmuting Lead to Gold: brew 'Air element created' and 'Strength potion brewed with 'Fire element created' and 'Water element created'' mixed with 'Fire element created'"

# ── ft_transmutation_0 — import alchemy.transmutation.recipes ──
echo -e "  ${DIM}ft_transmutation_0  (import alchemy.transmutation.recipes directly)${NC}"
run_has "[trans_0] header"     "=== Transmutation 0 ===" ft_transmutation_0.py
run_has "[trans_0] lead→gold"  "$GOLD"                   ft_transmutation_0.py
file_has "[trans_0] import"    "^import alchemy\.transmutation\.recipes" ft_transmutation_0.py
run_ok   ft_transmutation_0.py "[trans_0]"

# ── ft_transmutation_1 — import alchemy.transmutation ──
echo -e "  ${DIM}ft_transmutation_1  (import alchemy.transmutation module)${NC}"
run_has "[trans_1] header"     "=== Transmutation 1 ===" ft_transmutation_1.py
run_has "[trans_1] lead→gold"  "$GOLD"                   ft_transmutation_1.py
file_has "[trans_1] import"    "^import alchemy\.transmutation( |$)" ft_transmutation_1.py
run_ok   ft_transmutation_1.py "[trans_1]"

# ── ft_transmutation_2 — import alchemy only ──
echo -e "  ${DIM}ft_transmutation_2  (import alchemy only)${NC}"
run_has "[trans_2] header"     "=== Transmutation 2 ===" ft_transmutation_2.py
run_has "[trans_2] lead→gold"  "$GOLD"                   ft_transmutation_2.py
file_has "[trans_2] import"    "^import alchemy( |$)"    ft_transmutation_2.py
run_ok   ft_transmutation_2.py "[trans_2]"

# ================================================================
# 6 · PART IV — AVOID THE EXPLOSION
# ================================================================
banner "6 · Part IV: Avoid the Explosion"

# ── ft_kaboom_0 — light magic, no circular dep ──
echo -e "  ${DIM}ft_kaboom_0  (light magic — no circular dependency)${NC}"
run_has "[kaboom_0] header"          "=== Kaboom 0 ===" ft_kaboom_0.py
run_has "[kaboom_0] Spell recorded"  "Spell recorded"   ft_kaboom_0.py
run_has "[kaboom_0] VALID"           "VALID"            ft_kaboom_0.py
run_ok   ft_kaboom_0.py             "[kaboom_0] no circular dependency crash"

# ── ft_kaboom_1 — dark magic, must explode ──
echo -e "  ${DIM}ft_kaboom_1  (dark magic — circular import BOOM)${NC}"
run_has "[kaboom_1] header"          "=== Kaboom 1 ===" ft_kaboom_1.py
run_has "[kaboom_1] ImportError"     "ImportError"      ft_kaboom_1.py
run_has "[kaboom_1] circular import" "circular import"  ft_kaboom_1.py
info "kaboom_1: exit code not tested — catching exception is optional (§IV.4)"

# ================================================================
# 7 · FLAKE8
# ================================================================
banner "7 · Flake8 Style"

if ! command -v flake8 >/dev/null 2>&1; then
    info "flake8 not installed — skipping (pip install flake8)"
else
    ALL_CLEAN=true
    while IFS= read -r -d '' f; do
        res=$(flake8 --max-line-length=100 "$f" 2>&1)
        if [ -z "$res" ]; then
            ok "flake8 clean: $f"
        else
            ko "flake8: $f"
            printf '%s\n' "$res" | head -3 | sed 's/^/         /'
            ALL_CLEAN=false
        fi
    done < <(find . -maxdepth 4 -name "*.py" ! -path "*/__pycache__/*" -print0 | sort -z)
fi

# ================================================================
# 8 · MYPY
# ================================================================
banner "8 · Mypy Type Annotations"

if ! command -v mypy >/dev/null 2>&1; then
    info "mypy not installed — skipping (pip install mypy)"
else
    res=$(mypy . --ignore-missing-imports 2>&1)
    # ft_alembic_4 intentionally produces one mypy error (documented in subject §IV.1)
    unexpected=$(printf '%s\n' "$res" | grep "error:" | grep -v "ft_alembic_4" || true)
    if [ -z "$unexpected" ]; then
        ok "mypy — no unexpected type errors"
        info "ft_alembic_4 mypy error is intentional per subject §IV.1"
    else
        n_errors=$(printf '%s\n' "$unexpected" | grep -c "error:" || true)
        ko "mypy — $n_errors unexpected error(s)"
        printf '%s\n' "$unexpected" | head -5 | sed 's/^/         /'
    fi
fi

# ================================================================
# SUMMARY
# ================================================================
TOTAL=$((PASS + FAIL))
echo ""
echo -e "${CYAN}${BOLD}══════════════════════════════════════${NC}"
echo -e "${CYAN}${BOLD}  RESULTS${NC}"
echo -e "${CYAN}${BOLD}══════════════════════════════════════${NC}"
echo -e "  ${GREEN}Passed : $PASS${NC}"
echo -e "  ${RED}Failed : $FAIL${NC}"
echo -e "  Total  : $TOTAL"
echo -e "${CYAN}${BOLD}══════════════════════════════════════${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "  ${GREEN}${BOLD}🧪  All tests passed! The Great Work is complete!${NC}"
else
    echo -e "  ${RED}${BOLD}💥  $FAIL test(s) failed. Check the alchemist's notes above.${NC}"
fi
echo ""

exit $FAIL
