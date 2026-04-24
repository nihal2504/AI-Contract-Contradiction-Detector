from sentence_transformers import CrossEncoder
import numpy as np
import re

model = CrossEncoder("cross-encoder/nli-deberta-v3-base")

TOPIC_KEYWORDS = {
    "payment": ["pay", "payment", "invoice", "fee", "amount", "charges"],
    "termination": ["terminate", "termination", "notice", "agreement"],
    "data": ["data", "retain", "delete", "privacy", "customer"],
    "delivery": ["deliver", "delivery", "shipment", "supply"],
    "liability": ["liable", "liability", "damages", "loss"],
}

def get_topic(text):
    text_l = text.lower()
    scores = {}

    for topic, words in TOPIC_KEYWORDS.items():
        scores[topic] = sum(1 for w in words if w in text_l)

    best_topic = max(scores, key=scores.get)
    return best_topic if scores[best_topic] > 0 else "general"

def softmax(x):
    x = np.array(x)
    e = np.exp(x - np.max(x))
    return e / e.sum()

def extract_reason(a, b):
    a_l = a.lower()
    b_l = b.lower()

    nums_a = re.findall(r"\d+", a)
    nums_b = re.findall(r"\d+", b)

    if nums_a and nums_b and nums_a != nums_b:
        return f"Both clauses mention different numeric limits or deadlines: {nums_a} vs {nums_b}."

    if "terminate" in a_l or "terminate" in b_l:
        return "The clauses appear to create conflicting termination notice requirements."

    if "retain" in a_l and "delete" in b_l or "delete" in a_l and "retain" in b_l:
        return "One clause requires data retention while the other requires deletion."

    if "payment" in a_l or "pay" in a_l or "invoice" in a_l:
        return "The clauses appear to define different payment obligations or deadlines."

    return "The clauses may impose conflicting obligations or conditions."

def risk_level(score):
    if score >= 0.85:
        return "High"
    elif score >= 0.70:
        return "Medium"
    return "Low"

def detect_contradictions(pairs, threshold=0.65):
    outputs = []

    for a, b in pairs:
        topic_a = get_topic(a["text"])
        topic_b = get_topic(b["text"])

        if topic_a != topic_b:
            continue

        logits1 = model.predict([(a["text"], b["text"])])[0]
        logits2 = model.predict([(b["text"], a["text"])])[0]

        prob1 = softmax(logits1)
        prob2 = softmax(logits2)

        contradiction_score = float((prob1[0] + prob2[0]) / 2)

        if contradiction_score >= threshold:
            outputs.append({
                "clause_1_id": a["id"],
                "clause_1": a["text"],
                "clause_2_id": b["id"],
                "clause_2": b["text"],
                "topic": topic_a,
                "score": round(contradiction_score, 4),
                "risk": risk_level(contradiction_score),
                "explanation": extract_reason(a["text"], b["text"]),
                "suggested_resolution": "Review both clauses and standardize the obligation, timeline, or condition."
            })

    outputs.sort(key=lambda x: x["score"], reverse=True)
    return outputs