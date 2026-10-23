"""pytest-Einheits- und Integrations-Tests für sprint.

Die Tests laufen lokal UND in CI — null externe Abhängigkeit.
"""
from __future__ import annotations

from sprint.core import Document, Prototype
from sandbox.isolation import SANDBOX, isolation_flags


class TestPrototype:
    def test_search_returns_document(self):
        p = Prototype("t", [Document("DSG", "Datenschutz Sicherheit Prototyp")])
        r = p.search("Datenschutz")
        assert len(r) == 1 and r[0].title == "DSG"

    def test_search_no_match_returns_empty(self):
        p = Prototype("t", [Document("x", "unabhängig")])
        r = p.search("vollständig-abwesender-terminator-xyz")
        assert r == []

    def test_run_non_empty(self):
        p = Prototype("t", [Document("DSG", "Datenschutz Sicherheit")])
        out = p.run()
        assert len(out) > 10

    def test_limit(self):
        docs = [Document(f"doc{i}", "Sicherheit") for i in range(5)]
        p = Prototype("t", docs, limit=2)
        assert len(p.search("Sicherheit")) == 2


class TestIsolation:
    def test_non_root(self):
        assert SANDBOX["user"] != "root"

    def test_no_host_network(self):
        assert SANDBOX["network"] == "none"

    def test_cap_drop_all(self):
        assert "ALL" in SANDBOX["cap_drop"]

    def test_isolation_flags_contain_key_options(self):
        f = isolation_flags()
        assert "--network" in f
        assert f.index("--network") + 1 < len(f) and f[f.index("--network") + 1] == "none"
        assert "--read-only" in f
        assert "--cap-drop" in f


class TestCLI:
    def test_main_init_and_run(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        from sprint.__main__ import main
        rc = main(["init", "--name", "mini-rag"])
        assert rc == 0

        # Run ohne Corpus-Aktivität:
        rc = main(["run", "--name", "mini-rag"])
        assert rc == 0

    def test_verify_pass(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        from sprint.__main__ import main
        rc = main(["verify"])
        assert rc == 0
