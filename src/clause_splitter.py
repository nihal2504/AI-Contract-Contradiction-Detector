import re

def split_clauses(text):
    raw = re.split(r'\n+|[.;]\s+', text)
    clauses = []

    for i, clause in enumerate(raw):
        clause = clause.strip()
        if len(clause) > 15:
            clauses.append({
                "id": f"C{i+1}",
                "text": clause
            })

    return clauses