from copy import deepcopy
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import app


class KnowledgeBaseSecurityTests(unittest.TestCase):
    def setUp(self):
        self.corpus = patch.object(app, "CORPUS", deepcopy(app.CORPUS))
        self.corpus.start()
        self.addCleanup(self.corpus.stop)

    def test_acl_is_applied_before_ranking(self):
        self.assertEqual(app.rank("外部状态", role="tester", tenant="platform"), [])

    def test_authorized_reviewer_can_retrieve_private_fixture(self):
        hits = app.rank("外部状态", role="reviewer", tenant="platform")
        self.assertEqual([row["id"] for row in hits], ["d6"])

    def test_unauthorized_answer_refuses_without_citation(self):
        result = app.answer("外部状态", role="tester", tenant="platform")
        self.assertEqual(result["status"], "refused")
        self.assertEqual(result["citations"], [])

    def test_direct_document_lookup_checks_both_role_and_tenant(self):
        for role, tenant in [("tester", "platform"), ("reviewer", "test-bank")]:
            with self.subTest(role=role, tenant=tenant), self.assertRaises(PermissionError):
                app.get_doc("d6", role, tenant)
        with self.assertRaises(KeyError):
            app.get_doc("unknown")

    def test_returned_documents_cannot_mutate_corpus_acl(self):
        for lookup in [lambda: app.get_doc("d6", "reviewer", "platform"),
                       lambda: app.rank("外部状态", role="reviewer", tenant="platform")[0]]:
            with self.subTest(lookup=lookup):
                lookup()["allowed_roles"].append("tester")
                self.assertEqual(app.rank("外部状态", role="tester", tenant="platform"), [])

    def test_rank_rejects_invalid_top_k(self):
        for top_k in [0, -1, True, 1.5, "3", None]:
            with self.subTest(top_k=top_k), self.assertRaises(ValueError):
                app.rank("测试", top_k=top_k)

    def test_denied_document_text_is_not_tokenized(self):
        app.CORPUS["d6"]["text"] = object()
        self.assertEqual(app.rank("外部状态", role="tester", tenant="platform"), [])

    def test_answer_binds_citations_to_document_versions(self):
        result = app.answer("外部状态", "reviewer", "platform")
        self.assertEqual(result["citations"], [{"id": "d6", "version": "fixture-v1"}])


class EvaluationGateTests(unittest.TestCase):
    def run_cli(self, *, corpus=None, evalset=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "app.py").write_text(Path(app.__file__).read_text(encoding="utf-8"), encoding="utf-8")
            (root / "corpus.json").write_text(json.dumps(app.CORPUS if corpus is None else corpus), encoding="utf-8")
            (root / "evalset.json").write_text(json.dumps(app.EVALSET if evalset is None else evalset), encoding="utf-8")
            result = subprocess.run([sys.executable, "app.py", "eval"], cwd=root, capture_output=True, text=True)
            return result.returncode, json.loads(result.stdout)

    def test_real_cli_accepts_baseline(self):
        code, result = self.run_cli()
        self.assertEqual(code, 0)
        self.assertTrue(result["passed"])
        self.assertGreaterEqual(result["queries"], 8)
        self.assertEqual(result["citation_coverage"], 1.0)

    def test_real_cli_rejects_retrieval_regression(self):
        code, result = self.run_cli(corpus={})
        self.assertNotEqual(code, 0)

    def test_real_cli_rejects_empty_or_missing_negative_cases(self):
        for cases in [[], [item for item in app.EVALSET if item.get("expect_status") != "refused"],
                      [item for item in app.EVALSET if item.get("expect_status") == "refused"] * 4]:
            with self.subTest(cases=len(cases)):
                code, result = self.run_cli(evalset=cases)
                self.assertNotEqual(code, 0)

    def test_real_cli_rejects_malformed_evalset(self):
        code, result = self.run_cli(evalset=[{"query": "测试", "relevant": []}])
        self.assertNotEqual(code, 0)

    def test_eval_checks_actual_answer_citations_and_refusal_payload(self):
        for status in ["answered", "refused"]:
            with self.subTest(status=status), patch.object(app, "EVALSET", app.EVALSET[:1]), patch.object(app, "answer", return_value={
                "status": status, "citations": [{"id": "d6", "version": "fixture-v1"}]
            }):
                result = app.evaluate()
                self.assertLess(result["permission_pass_rate"], 1.0)

    def test_eval_rejects_permitted_but_irrelevant_citations(self):
        with patch.object(app, "EVALSET", app.EVALSET[:1]), patch.object(app, "answer", return_value={
            "status": "answered", "citations": [{"id": "d2", "version": "fixture-v1"}]
        }):
            result = app.evaluate()
            self.assertEqual(result["permission_pass_rate"], 1.0)
            self.assertEqual(result["hit_rate"], 0.0)
            self.assertFalse(result["passed"])

    def test_eval_rejects_wrong_citation_version(self):
        original = app.answer
        def wrong_version(*args, **kwargs):
            result = original(*args, **kwargs)
            for citation in result["citations"]:
                citation["version"] = "stale-version"
            return result
        with patch.object(app, "answer", side_effect=wrong_version):
            result = app.evaluate()
            self.assertLess(result["citation_coverage"], 1.0)
            self.assertFalse(result["passed"])


class ApprovalExampleTests(unittest.TestCase):
    def test_documented_policy_requires_approval_before_side_effects(self):
        doc = Path(__file__).resolve().parents[2] / "docs/tutorial/pi-agent-runtime.md"
        code = re.search(r"~~~python\n(.*?)\n~~~", doc.read_text(encoding="utf-8"), re.S).group(1)
        namespace = {}
        exec(code, namespace)
        for read_only in [False, True]:
            for requires_approval in [False, True]:
                for approved in [False, True]:
                    tool = namespace["ToolSpec"]("fixture", lambda: None, read_only, requires_approval)
                    with self.subTest(read_only=read_only, requires_approval=requires_approval, approved=approved):
                        expected = approved or (read_only and not requires_approval)
                        self.assertEqual(namespace["can_run"](tool, approved), expected)


if __name__ == "__main__":
    unittest.main()
