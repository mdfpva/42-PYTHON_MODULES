#!/bin/bash
# =============================================================
#  Python Module 10 — FuncMage (Functional Programming)
#  Deep tester — ex0 lambdas, ex1 higher-order, ex2 closures,
#                ex3 functools, ex4 decorators
#  Usage: bash tester_mod10.sh /path/to/student/repo
# =============================================================
#
#  Foco do módulo: padrões de programação funcional. NÃO há
#  validação de dados nem venv obrigatório (proíbe pip/libs
#  externas). Por isso o tester combina:
#   - inspeção estática (lambda no ex0, nonlocal no ex2,
#     functools.wraps no ex4, etc.)
#   - PROIBIÇÕES do subject (global, File I/O, eval/exec)
#   - harness que importa e CORRE as funções para provar
#     comportamento (closures independentes, reduce, retries…)
# =============================================================

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; MAGENTA='\033[0;35m'; BOLD='\033[1m'; RESET='\033[0m'

pass=0; fail=0; warn=0
ok()   { echo -e "  ${GREEN}[OK]${RESET}   $1"; pass=$((pass+1)); }
ko()   { echo -e "  ${RED}[KO]${RESET}   $1"; fail=$((fail+1)); }
wa()   { echo -e "  ${YELLOW}[!!]${RESET}   $1"; warn=$((warn+1)); }
hdr()  { echo -e "\n${BOLD}${CYAN}══════════════════════════════════════${RESET}\n${BOLD}${CYAN}  $1${RESET}\n${BOLD}${CYAN}══════════════════════════════════════${RESET}"; }
info() { echo -e "  ${MAGENTA}[>>]${RESET}   $1"; }

REPO="${1:-$(pwd)}"
TMP="$(mktemp -d /tmp/m10.XXXXXX)"
trap 'rm -rf "$TMP"; find "$REPO" -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null' EXIT

echo -e "${BOLD}${CYAN}\n╔══════════════════════════════════════╗\n║   Python Module 10 — Deep Tester     ║\n║   FuncMage (Functional Programming)  ║\n╚══════════════════════════════════════╝${RESET}"
echo -e "Repo: ${BOLD}$REPO${RESET}\n"

python3 -m flake8 --version &>/dev/null || pip install flake8 --break-system-packages -q 2>/dev/null
python3 -m mypy --version   &>/dev/null || pip install mypy   --break-system-packages -q 2>/dev/null

find_file() {
  find "$REPO" -name "$1" -not -path '*/__pycache__/*' \
    -not -path '*/.venv/*' -not -path '*/venv/*' 2>/dev/null | head -1
}

# harness: importa o ficheiro do aluno e corre o snippet (no dir certo)
run_harness() {
  local target="$1" dir mod
  dir="$(dirname "$target")"; mod="$(basename "${target%.py}")"
  ( cd "$dir" && timeout 20 python3 -c "
import importlib
m=importlib.import_module('$mod')
g=globals()
for k in dir(m):
    if not k.startswith('__'):
        g[k]=getattr(m,k)
$(cat)
" 2>&1 )
}
emit() { while IFS='|' read -r st msg; do
  [ "$st" = "PASS" ] && { ok "$1: $msg"; continue; }
  [ "$st" = "FAIL" ] && { ko "$1: $msg"; continue; }
  done; }

EX0="$(find_file lambda_spells.py)"
EX1="$(find_file higher_magic.py)"
EX2="$(find_file scope_mysteries.py)"
EX3="$(find_file functools_artifacts.py)"
EX4="$(find_file decorator_mastery.py)"

# ════════════════════════════════════════════════════════════
hdr "FILES + PROIBIÇÕES GERAIS"
# ════════════════════════════════════════════════════════════
declare -A FILES=( [ex0]="$EX0" [ex1]="$EX1" [ex2]="$EX2" [ex3]="$EX3" [ex4]="$EX4" )
declare -A NAMES=( [ex0]="lambda_spells.py" [ex1]="higher_magic.py" [ex2]="scope_mysteries.py" [ex3]="functools_artifacts.py" [ex4]="decorator_mastery.py" )
for k in ex0 ex1 ex2 ex3 ex4; do
  [ -f "${FILES[$k]}" ] && ok "${NAMES[$k]} encontrado" || ko "falta ${NAMES[$k]}"
done

PY_MIN=$(python3 -c "import sys;print(sys.version_info[1])")
[ "$PY_MIN" -ge 10 ] && ok "Python 3.$PY_MIN >= 3.10" || ko "Python < 3.10"

# proibições do subject (pág. 9): global, File I/O, eval, exec, pip
viol=$(grep -rnE "^[[:space:]]*global[[:space:]]|[^a-zA-Z_]eval\(|[^a-zA-Z_]exec\(|[^a-zA-Z_]open\(" \
       "$REPO" --include=*.py 2>/dev/null | grep -v "__pycache__")
[ -z "$viol" ] && ok "sem global / eval / exec / open (proibições respeitadas)" \
               || { ko "proibições violadas:"; echo "$viol"|head -4|sed 's/^/      /'; }
grep -rqE "^import |^from " "$REPO" --include=*.py 2>/dev/null | grep -qE "pandas|numpy|requests" \
  && ko "import de biblioteca externa (proibido)" || ok "só biblioteca-padrão (sem libs externas)"

# Callable deve vir de collections.abc (instrução do subject)
for k in ex1 ex2 ex3 ex4; do
  f="${FILES[$k]}"; [ -f "$f" ] || continue
  if grep -q "Callable" "$f"; then
    grep -q "from collections.abc import.*Callable\|from collections import abc" "$f" \
      && ok "$k: Callable importado de collections.abc" \
      || wa "$k: Callable devia vir de collections.abc (subject)"
  fi
done

# ════════════════════════════════════════════════════════════
hdr "QUALIDADE — flake8 + mypy"
# ════════════════════════════════════════════════════════════
for k in ex0 ex1 ex2 ex3 ex4; do
  f="${FILES[$k]}"; [ -f "$f" ] || continue
  b="${NAMES[$k]}"
  o=$(python3 -m flake8 "$f" 2>&1); [ -z "$o" ] && ok "flake8 $b limpo" || { ko "flake8 $b:"; echo "$o"|head -3|sed 's/^/      /'; }
  m=$(python3 -m mypy "$f" 2>&1); echo "$m"|grep -q Success && ok "mypy $b limpo" || { ko "mypy $b:"; echo "$m"|grep error|head -3|sed 's/^/      /'; }
done

# ════════════════════════════════════════════════════════════
hdr "EX0 — Lambda Sanctum (lambdas obrigatórias)"
# ════════════════════════════════════════════════════════════
if [ -f "$EX0" ]; then
  grep -q "lambda" "$EX0" && ok "ex0: usa lambda" || ko "ex0: tem de usar lambda"
  for fn in artifact_sorter power_filter spell_transformer mage_stats; do
    grep -q "def $fn" "$EX0" && ok "ex0: $fn definida" || ko "ex0: falta $fn"
  done
  grep -qE "sorted\(" "$EX0" && ok "ex0: usa sorted()" || ko "ex0: artifact_sorter deve usar sorted()"
  grep -qE "filter\(" "$EX0" && ok "ex0: usa filter()" || ko "ex0: power_filter deve usar filter()"
  grep -qE "map\(" "$EX0"    && ok "ex0: usa map()"    || ko "ex0: spell_transformer deve usar map()"
  R=$(run_harness "$EX0" <<'PY'
res=[]
def chk(n,c): res.append(("PASS" if c else "FAIL",n))
arts=[{"name":"A","power":50,"type":"x"},{"name":"B","power":90,"type":"y"}]
s=artifact_sorter(arts)
chk("ordena por power desc", s[0]["power"]==90 and s[1]["power"]==50)
mg=[{"name":"X","power":90,"element":"f"},{"name":"Y","power":40,"element":"a"}]
chk("filtra por min_power", [m["name"] for m in power_filter(mg,70)]==["X"])
chk("transforma spells", spell_transformer(["fire"])==["* fire *"])
st=mage_stats(mg)
chk("stats max/min/avg", st["max_power"]==90 and st["min_power"]==40 and st["avg_power"]==65.0)
chk("stats lista vazia", mage_stats([])["max_power"]==0)
for st_,n in res: print(st_+"|"+n)
PY
)
  echo "$R" | emit ex0
else ko "ex0 ignorado (ausente)"; fi

# ════════════════════════════════════════════════════════════
hdr "EX1 — Higher Realm (funções que devolvem funções)"
# ════════════════════════════════════════════════════════════
if [ -f "$EX1" ]; then
  for fn in spell_combiner power_amplifier conditional_caster spell_sequence; do
    grep -q "def $fn" "$EX1" && ok "ex1: $fn definida" || ko "ex1: falta $fn"
  done
  R=$(run_harness "$EX1" <<'PY'
res=[]
def chk(n,c): res.append(("PASS" if c else "FAIL",n))
def fb(t,p): return f"FB {t} {p}"
def hl(t,p): return f"HL {t} {p}"
comb=spell_combiner(fb,hl)
chk("combiner devolve tuplo", comb("D",10)==("FB D 10","HL D 10"))
amp=power_amplifier(fb,3)
chk("amplifier multiplica power", amp("D",10)=="FB D 30")
cc=conditional_caster(lambda t,p: p>=20, fb)
chk("conditional: falha → fizzled", cc("D",5)=="Spell fizzled")
chk("conditional: passa → executa", cc("D",25)=="FB D 25")
seq=spell_sequence([fb,hl])
chk("sequence devolve lista", seq("D",7)==["FB D 7","HL D 7"])
chk("resultado é callable", callable(seq))
for st_,n in res: print(st_+"|"+n)
PY
)
  echo "$R" | emit ex1
else ko "ex1 ignorado (ausente)"; fi

# ════════════════════════════════════════════════════════════
hdr "EX2 — Memory Depths (closures + nonlocal)"
# ════════════════════════════════════════════════════════════
if [ -f "$EX2" ]; then
  grep -q "nonlocal" "$EX2" && ok "ex2: usa nonlocal (estado em closure)" || ko "ex2: deve usar nonlocal"
  grep -qE "^[[:space:]]*global " "$EX2" && ko "ex2: usa global (proibido!)" || ok "ex2: não usa global"
  for fn in mage_counter spell_accumulator enchantment_factory memory_vault; do
    grep -q "def $fn" "$EX2" && ok "ex2: $fn definida" || ko "ex2: falta $fn"
  done
  R=$(run_harness "$EX2" <<'PY'
res=[]
def chk(n,c): res.append(("PASS" if c else "FAIL",n))
a=mage_counter(); b=mage_counter()
chk("counter conta 1,2", a()==1 and a()==2)
chk("counters independentes", b()==1)
acc=spell_accumulator(100)
chk("accumulator soma", acc(20)==120 and acc(30)==150)
ench=enchantment_factory("Flaming")
chk("enchantment formata", ench("Sword")=="Flaming Sword")
v=memory_vault()
v["store"]("k",42)
chk("vault store/recall", v["recall"]("k")==42)
chk("vault recall ausente", v["recall"]("zzz")=="Memory not found")
for st_,n in res: print(st_+"|"+n)
PY
)
  echo "$R" | emit ex2
else ko "ex2 ignorado (ausente)"; fi

# ════════════════════════════════════════════════════════════
hdr "EX3 — Ancient Library (functools + operator)"
# ════════════════════════════════════════════════════════════
if [ -f "$EX3" ]; then
  grep -q "functools.reduce\|reduce(" "$EX3" && ok "ex3: usa functools.reduce" || ko "ex3: spell_reducer deve usar reduce"
  grep -qE "operator\.(add|mul)" "$EX3" && ok "ex3: usa operator (add/mul)" || ko "ex3: deve usar operator"
  grep -qE "lru_cache|functools.cache" "$EX3" && ok "ex3: fibonacci memoizado (lru_cache)" || ko "ex3: fibonacci deve usar lru_cache"
  grep -q "partial" "$EX3" && ok "ex3: usa functools.partial" || ko "ex3: partial_enchanter deve usar partial"
  R=$(run_harness "$EX3" <<'PY'
res=[]
def chk(n,c): res.append(("PASS" if c else "FAIL",n))
chk("reduce add", spell_reducer([10,20,30,40],"add")==100)
chk("reduce multiply", spell_reducer([10,20,30,40],"multiply")==240000)
chk("reduce max", spell_reducer([10,20,30,40],"max")==40)
chk("reduce lista vazia → 0", spell_reducer([],"add")==0)
bad=False
try: spell_reducer([1,2],"xpto")
except Exception: bad=True
chk("operação desconhecida → erro", bad)
chk("fib(10)=55", memoized_fibonacci(10)==55)
chk("fib(15)=610", memoized_fibonacci(15)==610)
d=spell_dispatcher()
chk("dispatch int", "42" in d(42))
chk("dispatch str", "fireball" in d("fireball"))
chk("dispatch list", "3" in d([1,2,3]))
chk("dispatch desconhecido", d({"a":1})=="Unknown spell type")
for st_,n in res: print(st_+"|"+n)
PY
)
  echo "$R" | emit ex3
else ko "ex3 ignorado (ausente)"; fi

# ════════════════════════════════════════════════════════════
hdr "EX4 — Master's Tower (decorators + staticmethod)"
# ════════════════════════════════════════════════════════════
if [ -f "$EX4" ]; then
  grep -q "functools.wraps" "$EX4" && ok "ex4: usa functools.wraps" || ko "ex4: decorators devem usar functools.wraps"
  grep -q "@staticmethod" "$EX4" && ok "ex4: usa @staticmethod" || ko "ex4: falta @staticmethod"
  for fn in spell_timer power_validator retry_spell; do
    grep -q "def $fn" "$EX4" && ok "ex4: $fn definida" || ko "ex4: falta $fn"
  done
  grep -q "class MageGuild" "$EX4" && ok "ex4: classe MageGuild definida" || ko "ex4: falta MageGuild"
  R=$(run_harness "$EX4" <<'PY'
res=[]
def chk(n,c): res.append(("PASS" if c else "FAIL",n))
# wraps preserva nome
chk("spell_timer preserva __name__", fireball.__name__=="fireball")
# retry: falha sempre → mensagem após N tentativas
out=unstable_spell()
chk("retry esgota tentativas", "failed after 3 attempts" in out)
# retry: sucesso → resultado normal
chk("retry sucesso devolve resultado", successful_orc_spell()=="Waaaaaaagh spelled !")
# staticmethod
chk("validate_mage_name válido", MageGuild.validate_mage_name("Alex Mage") is True)
chk("validate_mage_name inválido", MageGuild.validate_mage_name("A1") is False)
g=MageGuild()
chk("cast_spell power ok", g.cast_spell("Lightning",15)=="Successfully cast Lightning with 15 power")
chk("cast_spell power baixo", g.cast_spell("Spark",5)=="Insufficient power for this spell")
for st_,n in res: print(st_+"|"+n)
PY
)
  echo "$R" | emit ex4
else ko "ex4 ignorado (ausente)"; fi

# ════════════════════════════════════════════════════════════
hdr "EVALUATION SHEET — perguntas para a defesa"
# ════════════════════════════════════════════════════════════
cat << 'Q'

  GERAL:
  → O que torna funções "first-class citizens" em Python?
  → De onde se importa Callable e para que serve callable()?

  EX0 (lambdas):
  → Quando usar lambda vs def?  (lambda: curta, descartável, como argumento)
  → Como o sorted(key=...) usa a lambda para ordenar?

  EX1 (higher-order):
  → O que é devolver uma função e como isso permite composição?
  → Porque combined devolve um tuplo e sequence uma lista?

  EX2 (closures):
  → O que é uma closure e como "lembra" o ambiente onde nasceu?
  → Porque é global proibido mas nonlocal permitido? (encapsulamento vs estado global)
  → Porque dois mage_counter() têm estado independente?

  EX3 (functools):
  → Como reduce agrega uma lista a um valor único?
  → Qual o benefício de lru_cache no fibonacci? (evita recalcular → linear)
  → O que faz functools.partial?

  EX4 (decorators):
  → O que é um decorator e o que faz functools.wraps?
  → Diferença entre decorator simples e decorator factory (com argumento)?
  → @staticmethod vs método de instância?

Q

# ════════════════════════════════════════════════════════════
hdr "SUMMARY"
# ════════════════════════════════════════════════════════════
total=$((pass+fail))
echo ""
echo -e "  Total:    $total"
echo -e "  ${GREEN}Passed:   $pass${RESET}"
[ "$fail" -gt 0 ] && echo -e "  ${RED}Failed:   $fail${RESET}" || echo "  Failed:   0"
[ "$warn" -gt 0 ] && echo -e "  ${YELLOW}Warnings: $warn${RESET}"
echo ""
[ "$fail" -eq 0 ] && echo -e "${BOLD}${GREEN}  ✓ All tests passed!${RESET}\n" || echo -e "${BOLD}${RED}  ✗ Some tests failed — see above${RESET}\n"
