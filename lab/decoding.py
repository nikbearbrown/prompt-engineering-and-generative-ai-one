"""A toy finite-logit decoder. No hosted models, data, or randomness."""
import math


def probabilities(logits, temperature):
    scores = tuple(logits)
    if not scores or any(not math.isfinite(z) for z in scores):
        raise ValueError("Give at least one finite logit.")
    if not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("Temperature must be finite and positive.")
    top = max(scores)
    weights = [math.exp((z - top) / temperature) for z in scores]
    total = sum(weights)
    return tuple(w / total for w in weights)


def pick(probs, draw):
    values = tuple(probs)
    if not values or any(not math.isfinite(p) or p < 0 for p in values):
        raise ValueError("Expected nonnegative, finite probabilities.")
    if not math.isclose(sum(values), 1.0, rel_tol=1e-12, abs_tol=1e-12):
        raise ValueError("Probabilities must sum to 1.")
    if not 0 <= draw < 1:
        raise ValueError("Draw must be in [0,1).")
    cumulative = 0.0
    final_positive = 0
    for i, probability in enumerate(values):
        if not probability:
            continue
        final_positive = i
        cumulative += probability
        if draw < cumulative:
            return i
    return final_positive  # guard against negligible summation error


if __name__ == "__main__":
    labels = ("A", "B", "C")
    logits = (math.log(4), math.log(2), 0.0)
    for t in (0.5, 1.0, 2.0):
        probs = probabilities(logits, t)
        print(f"T={t:g} p={tuple(round(p, 5) for p in probs)}; draw 0.7 -> {labels[pick(probs, 0.7)]}")
