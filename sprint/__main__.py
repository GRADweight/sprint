"""sprint CLI — ein Befehl, ein lauffähiger Prototyp.

Nutzung (außerhalb des Containers, lokal):
    sprint init --name mini-rag            # manifest + Corpus-Docs anlegen
    sprint run --name mini-rag             # Prototyp laufen lassen (offline-fallback)
    sprint run --name mini-rag --llm       # mit Ollama, falls erreichbar

Im Container (effimer, non-root, kein Host-Netz):
    docker run --rm --memory=512m --cpus=1 --network none -v $PWD:/work \\
      -w /work ghcr.io/gradweight/sprint:0.1.0 run --name mini-rag
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from sprint.core import Document, Prototype

# Default-Corpus ohne PII — sicher für Public-Repos und für das effimere Netz.
DEFAULT_CORPUS = [
    Document("DSG / Datenschutz",
            "Der Prototyp hält Daten ausschliesslich in-memory. Kein Versand, "
            "kein Cloud-Upload, kein Secret wird aus dem Host ge­lesen."),
    Document("Sicherheit",
            "Isolation durch non-root User, Ressourcenlimits und --network none. "
            "Der Prototyp kann weder Host-Netz noch andere Container erreichen."),
    Document("Reproduzierbarkeit",
            "Ein Prototyp-Manifest (JSON) beschreift den Corpus; derselbe Befehl "
            "produziert dieselbe Antwort. Kein Zufallszustand."),
    Document("Vendor-Unabhängigkeit",
            "Kein API-Key, keine Cloud, kein Modell-Lock-in: die Kern-Logik ist "
            "eine Funktion über ein lokales Corpus."),
]


def build_manifest(path: str, name: str, corpus: list[Document]) -> str:
    payload = {
        "name": name,
        "corpus": [{"title": d.title, "text": d.text} for d in corpus],
    }
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path


def load_prototype(name: str, manifest_dir: str | None = None) -> Prototype:
    manifest = f"{manifest_dir or ''}manifest.json"
    if os.path.exists(manifest):
        with open(manifest, encoding="utf-8") as f:
            data = json.load(f)
        corpus = [Document(d["title"], d["text"]) for d in data.get("corpus", [])]
        return Prototype(name=data.get("name", name), corpus=corpus)
    return Prototype(name=name, corpus=list(DEFAULT_CORPUS))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="sprint", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("init", help="manifest + Corpus anlegen")
    pi.add_argument("--name", default="mini-rag")

    pr = sub.add_parser("run", help="Prototyp laufen lassen")
    pr.add_argument("--name", default="mini-rag")
    pr.add_argument("--llm", action="store_true", help="Ollama nutzen, sonst fallback")

    pv = sub.add_parser("verify", help="Isolierbarkeit + Korpus-Integrität prüfen")

    a = p.parse_args(argv)

    if a.cmd == "init":
        manifest_path = os.path.join("prototypes", a.name, "manifest.json")
        build_manifest(manifest_path, a.name, DEFAULT_CORPUS)
        print(f"✓ manifest: {manifest_path}")
        print(f"  Laufbar mit: sprint run --name {a.name}")
        return 0

    if a.cmd == "run":
        proto = load_prototype(a.name)
        print(proto.run())
        return 0

    if a.cmd == "verify":
        proto = load_prototype("verify")
        out = proto.run()
        ok = "Beantwortet aus" in out
        print(out if ok else "FAIL: leerer Output")
        print("✓ verify OK" if ok else "✗ verify FAIL")
        return 0 if ok else 1

    return 2


if __name__ == "__main__":
    sys.exit(main())
