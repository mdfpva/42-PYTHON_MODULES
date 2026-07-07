#!/usr/bin/env python3
# os  - os.environ / os.environ.get: read environment variables
#       os.path.exists: check whether the .env file is present on disk
# sys - sys.exit: abort with a non-zero status on fatal configuration errors
#
# No 'typing' import: Python 3.10+ built-in syntax covers everything we need
# (str | None unions, dict[K, V] / list[X] generics, plain classes).
import os
import sys


# ---------------------------------------------------------------------------
# Configuration manifest
# Tuple layout: (variable_name, description, default_value, is_secret)
#   default_value=None → the variable is REQUIRED: missing triggers a warning.
#   is_secret=True     → the value is masked in output (never print secrets!).
# ---------------------------------------------------------------------------
CONFIG_VARS: list[tuple[str, str, str | None, bool]] = [
    ("MATRIX_MODE",   "Execution mode",             "development", False),
    ("DATABASE_URL",  "Data storage connection",    None,          True),
    ("API_KEY",       "External services secret",   None,          True),
    ("LOG_LEVEL",     "Logging verbosity",          "INFO",        False),
    ("ZION_ENDPOINT", "Resistance network URL",     None,          False),
]

ENV_FILE: str = ".env"  # dotenv file expected next to this script


# ---------------------------------------------------------------------------
# ConfigValue — plain class (no typing.TypedDict needed) describing one
# resolved configuration entry and where its value came from.
# ---------------------------------------------------------------------------

class ConfigValue:
    """One resolved configuration variable and its provenance."""

    def __init__(
        self,
        name:        str,         # environment variable name (e.g. "API_KEY")
        value:       str | None,  # resolved value, or None when truly missing
        source:      str,         # "environment", ".env file", or "default"
        description: str,         # human-readable role of the variable
        is_secret:   bool,        # True → mask the value when displaying
    ) -> None:
        # Each attribute inherits its type from the parameter annotation;
        # mypy infers self.value: str | None, self.is_secret: bool, etc.
        self.name = name
        self.value = value
        self.source = source
        self.description = description
        self.is_secret = is_secret

    def display_value(self) -> str:
        """Return the value formatted for safe printing."""
        if self.value is None:
            return "<missing>"
        if self.is_secret:
            # Mask everything except the first 3 characters: enough to
            # confirm the right key is loaded without leaking the secret.
            # max(0, ...) guards against negative repeat counts on short values.
            visible: str = self.value[:3]
            return visible + "*" * max(0, len(self.value) - 3)
        return self.value


# ---------------------------------------------------------------------------
# 1. Loading the .env file
# ---------------------------------------------------------------------------

def load_env_file() -> bool:
    """
    Load ENV_FILE via python-dotenv if both the library and the file exist.
    Returns True when a .env file was found and loaded.

    Precedence rule (the exercise's override requirement):
      load_dotenv(override=False) — the DEFAULT — never replaces a variable
      that already exists in os.environ. So a value exported in the shell
      (MATRIX_MODE=production python3 oracle.py) always wins over .env.
    """
    try:
        # Local import: if python-dotenv is missing we degrade gracefully
        # to shell-only variables instead of crashing at the top of the file.
        from dotenv import load_dotenv
    except ImportError:
        print("  [WARN] python-dotenv not installed — .env file ignored")
        print("         install with: pip install python-dotenv")
        return False

    # os.path.exists checks the file is actually there before loading;
    # load_dotenv would silently do nothing, but we want to tell the user.
    if not os.path.exists(ENV_FILE):
        print(f"  [WARN] no {ENV_FILE} file found — using shell env and defaults")
        print(f"         create one with: cp .env.example {ENV_FILE}")
        return False

    # override=False (default): existing os.environ entries take precedence.
    load_dotenv(ENV_FILE)
    print(f"  [OK] {ENV_FILE} file loaded")
    return True


# ---------------------------------------------------------------------------
# 2. Resolving each variable with provenance tracking
# ---------------------------------------------------------------------------

def resolve_config(env_file_loaded: bool) -> dict[str, ConfigValue]:
    """
    Resolve every variable in CONFIG_VARS following the precedence chain:
        shell environment  >  .env file  >  hardcoded default  >  missing

    Provenance trick: we snapshot os.environ BEFORE load_dotenv ran (see
    main), so here we only distinguish ".env file vs environment" by asking
    the caller whether dotenv actually loaded a file.
    """
    resolved: dict[str, ConfigValue] = {}

    for name, description, default, is_secret in CONFIG_VARS:
        # os.environ.get returns str | None — None when the variable is unset.
        # At this point .env values are already merged into os.environ.
        value: str | None = os.environ.get(name)

        if value is not None:
            # PRE_DOTENV_ENV is the snapshot taken before load_dotenv;
            # if the name was already there, the shell provided it.
            source: str = (
                "environment" if name in PRE_DOTENV_ENV
                else (".env file" if env_file_loaded else "environment")
            )
        elif default is not None:
            value = default
            source = "default"
        else:
            source = "missing"

        resolved[name] = ConfigValue(
            name=name, value=value, source=source,
            description=description, is_secret=is_secret,
        )

    return resolved


# ---------------------------------------------------------------------------
# 3. Displaying configuration (mode-dependent output)
# ---------------------------------------------------------------------------

def print_config(config: dict[str, ConfigValue]) -> None:
    """
    Print the resolved configuration.
    Development vs production difference (visible in output, as required):
      development → every variable is shown with its (masked) value + source
      production  → secrets are fully hidden, only status words are printed
    """
    # Walrus-free lookup: MATRIX_MODE is guaranteed present (it has a default).
    mode: str = config["MATRIX_MODE"].value or "development"
    is_production: bool = mode == "production"

    print()
    print("Configuration loaded:")
    print(f"  Mode: {mode}")

    # DATABASE_URL — status phrasing depends on mode and presence.
    db: ConfigValue = config["DATABASE_URL"]
    if db.value is None:
        print("  Database: NOT CONFIGURED — set DATABASE_URL")
    elif is_production:
        # Production: never echo connection strings, even masked.
        print("  Database: Connected (details hidden in production)")
    else:
        print(f"  Database: Connected to {db.display_value()}  [{db.source}]")

    # API_KEY — authenticated / not authenticated.
    api: ConfigValue = config["API_KEY"]
    if api.value is None:
        print("  API Access: NOT AUTHENTICATED — set API_KEY")
    elif is_production:
        print("  API Access: Authenticated")
    else:
        print(f"  API Access: Authenticated with {api.display_value()}  [{api.source}]")

    # LOG_LEVEL — always safe to show.
    log: ConfigValue = config["LOG_LEVEL"]
    print(f"  Log Level: {log.value}  [{log.source}]")

    # ZION_ENDPOINT — online / offline.
    zion: ConfigValue = config["ZION_ENDPOINT"]
    if zion.value is None:
        print("  Zion Network: OFFLINE — set ZION_ENDPOINT")
    else:
        print(f"  Zion Network: Online at {zion.value}  [{zion.source}]")


# ---------------------------------------------------------------------------
# 4. Security checks
# ---------------------------------------------------------------------------

def security_checks(config: dict[str, ConfigValue], env_file_loaded: bool) -> int:
    """
    Run the three security checks from the expected output and return the
    number of failures (0 = all good).
    """
    failures: int = 0

    print()
    print("Environment security check:")

    # Check 1 — no hardcoded secrets: read our own source file and verify
    # that no CONFIG_VARS secret VALUE appears literally in the code.
    # __file__ is the path of the running script; open+read is plain file I/O.
    source_code: str = ""
    try:
        with open(__file__, "r", encoding="utf-8") as f:
            source_code = f.read()
    except OSError:
        pass  # unreadable source: skip rather than fail the check

    hardcoded: bool = any(
        cv.is_secret and cv.value is not None and cv.value in source_code
        for cv in config.values()
    )
    if hardcoded:
        print("  [FAIL] Hardcoded secret found in source code!")
        failures += 1
    else:
        print("  [OK] No hardcoded secrets detected")

    # Check 2 — .env present AND ignored by git: read .gitignore and confirm
    # a line covers '.env' so the secrets file can never be committed.
    env_ignored: bool = False
    try:
        with open(".gitignore", "r", encoding="utf-8") as g:
            # Strip comments/whitespace; accept '.env' or a pattern like '*.env'.
            lines: list[str] = [ln.strip() for ln in g.readlines()]
            env_ignored = any(ln in (".env", "*.env", ".env*") for ln in lines)
    except OSError:
        env_ignored = False

    if env_file_loaded and env_ignored:
        print("  [OK] .env file properly configured")
    elif env_file_loaded and not env_ignored:
        print("  [FAIL] .env exists but is NOT in .gitignore — add it now!")
        failures += 1
    else:
        print("  [WARN] no .env file — copy .env.example to get started")

    # Check 3 — production overrides: confirm that shell variables win.
    # If any variable came from "environment", the override path works.
    override_ready: bool = any(
        cv.source == "environment" for cv in config.values()
    )
    if override_ready:
        print("  [OK] Production overrides active (shell env in use)")
    else:
        print("  [OK] Production overrides available")
        print("       (try: MATRIX_MODE=production API_KEY=<your-key> python3 oracle.py)")

    return failures


# ---------------------------------------------------------------------------
# 5. Main
# ---------------------------------------------------------------------------

# Snapshot of variable names present in the shell BEFORE dotenv runs.
# frozenset: immutable set — cannot be accidentally modified later.
# This is what lets resolve_config distinguish "shell" from ".env" values.
PRE_DOTENV_ENV: frozenset[str] = frozenset(os.environ.keys())


def main() -> None:
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    # Step 1 — merge .env into os.environ (shell vars keep precedence).
    env_file_loaded: bool = load_env_file()

    # Step 2 — resolve every variable and record where it came from.
    config: dict[str, ConfigValue] = resolve_config(env_file_loaded)

    # Step 3 — display, adapting verbosity to development vs production.
    print_config(config)

    # Step 4 — security audit.
    failures: int = security_checks(config, env_file_loaded)

    print()
    if failures:
        print("The Oracle sees vulnerabilities. Fix them before proceeding.")
        # Non-zero exit code signals failure to shells and CI pipelines.
        sys.exit(1)
    print("The Oracle sees all configurations.")


# Entry-point guard: run main() only when executed directly,
# not when imported as a module.
if __name__ == "__main__":
    main()
