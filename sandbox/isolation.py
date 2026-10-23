"""Isolationsschicht: effimer, non-root, Ressourcenlimits, kein Host-Netz.

Diese Module beschreibt die Container-Sandbox in Code — nicht in Prosa.
Dockerfile, Docker-Compose-Overlay und CI-Workflow importieren diese Werte.
"""

from __future__ import annotations

# --- Hardened Container Defaults (fail-closed) ---
SANDBOX = {
    "user": "nobody",           # non-root
    "memory_limit": "512Mi",    # Ressourcenlimit
    "cpus": 1,                  # CPU-Limit
    "network": "none",          # kein Host-Netz, kein Internet
    "read_only_root_fs": True,  # schreibgeschützt
    "tmpfs": ["/tmp:rw,noexec,size=64m"],
    "cap_drop": ["ALL"],        # keine Capabilities im Container
    "cap_add": [""],            # explizit keine hinzufügen
}


def isolation_flags() -> list[str]:
    """docker run-Argumente aus SANDBOX ableiten."""
    flags: list[str] = []
    flags.extend(["--user", "nobody"])
    flags.extend(["--memory", "512m"])
    flags.extend(["--cpus", "1"])
    flags.extend(["--network", "none"])
    if SANDBOX["read_only_root_fs"]:
        flags.append("--read-only")
    else:
        flags.append("--init")
    for cap in SANDBOX["cap_drop"]:
        flags.extend(["--cap-drop", cap])
    for cap in SANDBOX["cap_add"]:
        if cap:
            flags.extend(["--cap-add", cap])
    if SANDBOX["tmpfs"]:
        flags.extend(["--tmpfs", "tmp:rw,noexec,size=64m"])
    return flags
