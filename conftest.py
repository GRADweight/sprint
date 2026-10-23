"""pytest: stellt sicheres Repo-Root-Pythonpath, damit Tests die Quelle direkt importieren
(sprint UND sandbox liegen top-level; kein pip-install nötig)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
