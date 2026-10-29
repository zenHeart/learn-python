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
    words = re.findall(r"[a-z0-9_]+|[一-鿿]", text)
    return words

def rank(query: str, top_k: int = 3) -> list[dict]:
    query_terms = set(tokenize(query))
    rows = []
    for doc_id, doc in CORPUS.items():
        terms = tokenize(doc["title"] + " " + doc["text"])
        score = sum(1 for term in query_terms if term in terms)
        rows.append((score, doc_id))
    rows.sort(key=lambda item: (-item[0], item[1]))
    return [
        {"id": doc_id, "score": score, **CORPUS[doc_id]}
        for score, doc_id in rows[:top_k]
        if score > 0
    ]

def get_doc(doc_id: str, role: str = "tester") -> dict:
    if role not in {"tester", "reviewer"}:
        raise PermissionError("role is not allowed")
    if doc_id not in CORPUS:
        raise KeyError("unknown document")
    return {"id": doc_id, "version": "fixture-v1", **CORPUS[doc_id]}

def answer(query: str, role: str = "tester") -> dict:
    hits = rank(query)
    if not hits:
        return {"status": "refused", "reason": "no evidence", "citations": []}
    citations = [get_doc(hit["id"], role)["id"] for hit in hits]
    return {
        "status": "answered",
        "answer": "基于合成知识库返回候选证据，请继续核验引用内容。",
        "citations": citations,
        "trace": {"query": query, "role": role, "retriever": "token-overlap", "version": "fixture-v1"}
    }

def reciprocal_rank(ranked: list[str], relevant: list[str]) -> float:
    wanted = set(relevant)
    for pos, doc_id in enumerate(ranked, start=1):
        if doc_id in wanted:
            return 1.0 / pos
    return 0.0

def evaluate() -> dict:
    hits, recalls, mrrs = [], [], []
    for item in EVALSET:
        ranked = [row["id"] for row in rank(item["query"])]
        relevant = set(item["relevant"])
        hits.append(float(bool(relevant & set(ranked))))
        recalls.append(len(relevant & set(ranked)) / len(relevant))
        mrrs.append(reciprocal_rank(ranked, item["relevant"]))
    return {
        "queries": len(EVALSET),
        "hit_rate": round(fmean(hits), 3),
        "recall_at_3": round(fmean(recalls), 3),
        "mrr": round(fmean(mrrs), 3)
    }

def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: python app.py query <text> | eval")
        return 2
    if argv[1] == "query":
        print(json.dumps(answer(" ".join(argv[2:])), ensure_ascii=False, indent=2))
        return 0
    if argv[1] == "eval":
        print(json.dumps(evaluate(), ensure_ascii=False, indent=2))
        return 0
    print("unknown command")
    return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
