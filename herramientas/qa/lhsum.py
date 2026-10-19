"""Resume reportes JSON de Lighthouse en una tabla legible."""
import json
import sys

AUDITS = [
    ("largest-contentful-paint", "LCP"),
    ("first-contentful-paint", "FCP"),
    ("total-blocking-time", "TBT"),
    ("cumulative-layout-shift", "CLS"),
    ("speed-index", "SI"),
    ("total-byte-weight", "Peso"),
]


def summarize(path):
    r = json.load(open(path))
    cats = r["categories"]
    out = {k: round((v["score"] or 0) * 100) for k, v in cats.items()}
    for key, label in AUDITS:
        a = r["audits"].get(key, {})
        out[label] = a.get("displayValue", "-")
    failed = []
    for cid in ("seo", "accessibility", "best-practices"):
        for ref in cats[cid]["auditRefs"]:
            a = r["audits"][ref["id"]]
            if a.get("score") is not None and a["score"] < 1 and ref.get("weight", 0) > 0:
                failed.append(f"{cid}:{ref['id']}")
    out["fallas"] = failed
    errs = r.get("runtimeError")
    if errs:
        out["runtimeError"] = errs
    return out


if __name__ == "__main__":
    for p in sys.argv[1:]:
        s = summarize(p)
        print(p.split("/")[-1], json.dumps(s, ensure_ascii=False))
