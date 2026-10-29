import unittest

import app


class KnowledgeBaseSecurityTests(unittest.TestCase):
    def test_acl_is_applied_before_ranking(self):
        self.assertEqual(app.rank("外部状态", role="tester", tenant="platform"), [])

    def test_authorized_reviewer_can_retrieve_private_fixture(self):
        hits = app.rank("外部状态", role="reviewer", tenant="platform")
        self.assertEqual([row["id"] for row in hits], ["d6"])

    def test_unauthorized_answer_refuses_without_citation(self):
        result = app.answer("外部状态", role="tester", tenant="platform")
        self.assertEqual(result["status"], "refused")
        self.assertEqual(result["citations"], [])


if __name__ == "__main__":
    unittest.main()
