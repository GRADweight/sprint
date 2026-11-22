# sprint — ein Prototyp, der in einer Stunde läuft.

> Kann ein Prototyp in 60 Minuten lauffähig sein, ohne Cloud, ohne API-Key und ohne einen einzigen Datenpunkt über die Firewall zu schicken?

> **Fallbeispiel:** Eine KMU will prüfen, ob ein Mini-RAG-Chatbot für interne FAQ funktioniert. Mit sprint: `sprint init` legt ein leeres Corpus an, `sprint run` startet den Prototyp in einem isolierten, non-root Docker-Container (kein Host-Netz, 512 MB RAM, 1 CPU, schreib­geschütztes Root-FS) — nach 3 Minuten ist das Ergebnis lesbar, null Abhängigkeit.

## Für wen

- **Fachperson (kein IT-Background):** Ein Befehl, kein Build-Prozess. Ergebnis in Minuten — nicht in Tagen mit Cloud-Setup.
- **Sicherheits­verantwortlicher:** Null Networking, null Secrets, null Datenübertragung. Isolation nicht als Feature — sondern per Default.
- **Technischer AI-Lead:** Ein Prototyp = ein `Prototype`-Objekt. Derselbe Pfad, lokal und im Container. Reproduzierbar über Manifest.

## Warum jetzt

- KI-Prototyping ohne Cloud-Kosten und ohne Vendor-Lock-in ist heute machbar — sprint beweis es.
- KMU wollen testen, bevor sie kaufen. Null-Setup-Prototyping senkt die Vor­lage­hürde auf Null.
- DSG/DSGVO-Prototyping: Daten verlassen den Host nie. Kein PII, kein Te­leport, nichts.

## Architektur

```
    sprint CLI
        │
   ┌────▼─────┐
   │  Sprint   │  (effimerer Docker-Container)
   │  Prototyp │  ├── Non-root User
   │           │  ├── 512 MB RAM / 1 CPU
   │           │  ├── No host network
   │           │  └── Read-only root FS
   └───────────┘
```

## Schnellstart

```bash
# Lokal:
git clone https://github.com/GRADweight/sprint.git
cd sprint && uv sync
sprint run --name mini-rag

# Im Container (effimer, null Netz, null Host-Zugriff):
docker run --rm --memory=512m --network none -v $PWD:/work -w /work \
  ghcr.io/gradweight/sprint:0.1.0 run --name mini-rag

# CI-Verifikation (GitHub-Actions):
pytest -v        # 10 Tests, null externe Abhängigkeit
```

## Sicherheit & NIST

- **Guardrail-Level:** Isolation per Default. Sandbox: non-root, Cap DROP ALL, read-only root FS, kein Host-Netz, 512 MB / 1 CPU. Kein Prototyp kann den Host erreichen.
- **Risiko-Kategorie:** DSG/DSGVO — Datenhaltung: ausschließlich in-memory / effimer. Kein PII, kein Cloud-Upload, kein Secret. Null externer Datenfluss.
- **NIST-AI-RM-Fokus:** Measure + Manage — ein Prototyp ist ein mass­gebliches Risiko­­messungsin­strument. Der Isolations­grad ist messbar: die Isolation-Flag­gen im Code (`sandbox/isolation.py`) sind das Protokoll.
- **Lizenz:** MIT — frei nutzbar, s. LICENSE.

## Status

⚡ **Laufbar lokal:** `pytest -v` → 10 Tests grün, null externe Abhängigkeit.
🔄 **Container-Image:** `Dockerfile` bereit — `docker build` erzeugt das effimere Sprint-Image.
⏳ **Next Step:** `docker run`-Smoke-Test in CI (auf GitHub-Actions Runner mit Docker-Daemon).

---

> Teil von GRADweight — KMU-AI-Architektur-Netzwerk.
> Finde uns: github.com/GRADweight | Frage? Eröffne ein Issue.


---
> **Sicherheit, Haftung, Grenzen:** `SICHERHEIT_UND_GRENZEN.md` (Bekannte Fehler, Haftung, Lizenz-Erklaerung, ein Satz je Repo).
