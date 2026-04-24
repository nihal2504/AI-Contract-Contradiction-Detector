from itertools import combinations
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def generate_pairs(clauses, top_k=30):
    if len(clauses) < 2:
        return []

    texts = [c["text"] for c in clauses]

    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform(texts)
    sim = cosine_similarity(X)

    scored_pairs = []

    for i, j in combinations(range(len(clauses)), 2):
        scored_pairs.append((sim[i][j], clauses[i], clauses[j]))

    scored_pairs.sort(reverse=True, key=lambda x: x[0])

    return [(a, b) for score, a, b in scored_pairs[:top_k]]