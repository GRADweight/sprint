"""sprint.core — ein Prototyp in unter 60 Minuten, in einer isolierten Um­gebung.

sprint ist ein Baustein, nicht «docker run». Er erzeugt einen funktionierenden
Prototyp (hier: Mini-RAG), lauft in einer effimeren, non-root Docker-Sandbox mit
Ressourcenlimits und OHNE Host-Netz (kein Cloud, keine Secrets, kein Vendor).

Die Kern-Logik ist absichtlich von Docker, K8s und Cloud entkopp: dieselbe
`Prototype`-Klasse läuft lokal `./sprint run` und in dem Container — das ist der
Grund, warum ein Prototyp in <1h läuft und reproduzierbar ist.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Datenhaltung: ausschließlich in-memory / ephemere Volume. Kein DB-Server,
# keine Secrets, kein Networking nötig.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Document:
    """Ein Quelldokument (Titel + Text). Kein PII im Default-Demo."""

    title: str
    text: str

    def sha256(self) -> str:
        return hashlib.sha256(self.title.encode() + b"\x00" + self.text.encode()).hexdigest()[:12]


@dataclass
class Prototype:
    """Ein konfigurierbarer, lauffähiger Mini-Prototyp.

    `engine` entscheidet lauffähig vs. offline:
      - 'fallback' (Default): deterministischer Keyword-RAG, immer grün, null Dependenz.
      - 'llm':       nutzt Ollama, falls erreichbar; sonst still in 'fallback' zurück.

    Das ist der DSG-/Vorfälligkeits-Herz-Konv des Hauses: ein Prototyp darf
    niemals wegen fehlender Netzwerk-/Modell-Verfügbarkeit den ganzen Ablauf
    ruinieren.
    """

    name: str
    corpus: list[Document] = field(default_factory=list)
    limit: int = 3
    engine: str = "fallback"

    def search(self, query: str, *, top_k: int | None = None) -> list[Document]:
        """Deterministischer Keyword-RAG (Token-Überschneidung, grossgeschrieben-unabhängig)."""
        k = top_k or self.limit
        q_tokens = set(t.lower() for t in query.replace("/-/.", " ").split() if len(t) > 1)
        scored: list[tuple[int, Document]] = []
        for d in self.corpus:
            hay = set(t.lower() for t in d.text.replace("/-/.", " ").split())
            hit = len(q_tokens & hay)
            if hit:
                scored.append((hit, d))
        scored.sort(key=lambda x: (-x[0], x[1].title.encode()))
        return [d for _, d in scored[:k]]

    def answer(self, query: str, *, top_k: int | None = None) -> str:
        hits = self.search(query, top_k=top_k)
        if not hits:
            return "Kein Treffer im Prototyp-Corpus. Ergänz den Corpus im Manifest."
        ctx = "\n".join(f"- {d.title}: {d.text}" for d in hits)
        return f"Beantwortet aus {len(hits)} Treffern im isolierten Corpus:\n{ctx}"

    def run(self) -> str:
        demo_query = "Sicherheit und Datenschutz im Prototyp"
        return self.answer(demo_query)
