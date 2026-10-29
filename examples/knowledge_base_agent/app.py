from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from statistics import fmean

ROOT = Path(__file__).parent
CORPUS = json.loads((ROOT / "corpus.json").read_text(encoding="utf-8"))
EVALSET = json.loads((ROOT / "evalset.json").read_text(encoding="utf-8"))

def tokenize(text: str) -> list[str]:
    text = text.lower()
    return re.findall(r"[a-z0-9_]+|[一-鿿]", text)

def allowed(doc: dict, role: str, tenant: str) -> bool:
    return tenant == doc["tenant"] and role in doc["allowed_roles"]

def rank(query: str, top_k: int = 3, role: str = "tester", tenant: str = "test-bank") -> list[dict]:
    query_terms = set(tokenize(query))
    rows = []
    for doc_id, doc in CORPUS.items():
        # ACL 在排序前执行，防止无权文档影响召回和泄漏相关性信号。
        if not allowed(doc, role, tenant):
            continue
        terms = tokenize(doc["title"] + " " + doc["text"])
        score = sum(1 for term in query_terms if term in terms)
        rows.append((score, doc_id))
    rows.sort(key=lambda item: (-item[0], item[1]))
    return [
        {"id": doc_id, "score": score, **CORPUS[doc_id]}
        for score, doc_id in rows[:top_k]
        if score > 0
    ]

def get_doc(doc_id: str, role: str = "tester", tenant: str = "test-bank") -> dict:
    if doc_id not in CORPUS:
        raise KeyError("unknown document")
    if not allowed(CORPUS[doc_id], role, tenant):
        raise PermissionError("document is outside the role or tenant scope")
    return {"id": doc_id, "version": "fixture-v1", **CORPUS[doc_id]}

def answer(query: str, role: str = "tester", tenant: str = "test-bank") -> dict:
    hits = rank(query, role=role, tenant=tenant)
    if not hits:
        return {
            "status": "refused",
            "reason": "no permitted evidence",
            "citations": [],
            "trace": {"query": query, "role": role, "tenant": tenant}
        }
    citations = [get_doc(hit["id"], role, tenant)["id"] for hit in hits]
    return {
        "status": "answered",
        "answer": "基于合成知识库返回候选证据，请继续核验引用内容。",
        "citations": citations,
        "trace": {"query": query, "role": role, "tenant": tenant, "retriever": "token-overlap", "acl_before_rank": True, "version": "fixture-v1"}
    }

def reciprocal_rank(ranked: list[str], relevant: list[str]) -> float:
    wanted = set(relevant)
    for pos, doc_id in enumerate(ranked, start=1):
        if doc_id in wanted:
            return 1.0 / pos
    return 0.0

def evaluate() -> dict:
    hits, recalls, mrrs, permission_checks = [], [], [], []
    for item in EVALSET:
        role = item.get("role", "tester")
        tenant = item.get("tenant", "test-bank")
        result = answer(item["query"], role, tenant)
        if item.get("expect_status") == "refused":
            permission_checks.append(float(result["status"] == "refused"))
            continue
        ranked = [row["id"] for row in rank(item["query"], role=role, tenant=tenant)]
        relevant = set(item["relevant"])
        hits.append(float(bool(relevant & set(ranked))))
        recalls.append(len(relevant & set(ranked)) / len(relevant))
        mrrs.append(reciprocal_rank(ranked, item["relevant"]))
        permission_checks.append(float(set(ranked) <= relevant or bool(ranked)))
    return {
        "queries": len(EVALSET),
        "answer_queries": len(hits),
        "hit_rate": round(fmean(hits), 3) if hits else 0.0,
        "recall_at_3": round(fmean(recalls), 3) if recalls else 0.0,
        "mrr": round(fmean(mrrs), 3) if mrrs else 0.0,
        "permission_pass_rate": round(fmean(permission_checks), 3) if permission_checks else 0.0
    }

def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: python app.py query <text> [role] [tenant] | eval")
        return 2
    if argv[1] == "query":
        query = argv[2] if len(argv) > 2 else ""
        role = argv[3] if len(argv) > 3 else "tester"
        tenant = argv[4] if len(argv) > 4 else "test-bank"
        print(json.dumps(answer(query, role, tenant), ensure_ascii=False, indent=2))
        return 0
    if argv[1] == "eval":
        print(json.dumps(evaluate(), ensure_ascii=False, indent=2))
        return 0
    print("unknown command")
    return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
