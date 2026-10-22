"""
Hallucination Detection Engine
Combines rule-based, semantic, and keyword analysis to score AI responses.
"""
import re
import math
from typing import List, Dict


# --- Pattern Libraries ---

OVERCONFIDENCE_PATTERNS = [
    r'\b(definitely|certainly|absolutely|undeniably|unquestionably)\b',
    r'\b(100%|always|never|without exception|in all cases)\b',
    r'\b(it is a fact that|it is proven that|it is established that)\b',
    r'\b(guaranteed|proven|confirmed|verified)\b',
]

HEDGING_PATTERNS = [
    r'\bI think\b', r'\bI believe\b', r'\bprobably\b',
    r'\bmaybe\b', r'\bmight be\b', r'\bcould be\b',
    r'\bperhaps\b', r'\bapparently\b', r'\bseemingly\b',
    r'\bI\'m not sure\b', r'\bI\'m not certain\b',
]

VAGUE_AUTHORITY_PHRASES = [
    'some studies suggest', 'research has shown', 'experts say',
    'scientists have found', 'it is widely believed', 'most people agree',
    'it is well known', 'everyone knows', 'as we all know',
    'obviously', 'clearly', 'it goes without saying', 'needless to say',
    'many experts believe', 'according to experts',
]

SUSPICIOUS_NUMERIC_PATTERN = r'\b\d{1,3}(?:\.\d+)?%\b'
YEAR_CLAIM_PATTERN = r'\b(in|since|from|by|around|circa)\s+\d{4}\b'

QUALITY_INDICATORS = [
    'according to', 'research indicates', 'studies have shown',
    'it has been demonstrated', 'evidence suggests', 'data shows',
    'specifically', 'for example', 'for instance', 'such as',
    'defined as', 'refers to', 'known as', 'is characterized by',
]


class HallucinationAnalyzer:
    """
    Analyzes an AI response for hallucination indicators using:
    1. Rule-based pattern matching
    2. Keyword overlap (semantic proxy)
    3. Response coherence and length scoring
    4. Overconfidence / hedging detection
    """

    def __init__(self, query: str, response: str):
        self.query = query.strip()
        self.response = response.strip()
        self.response_lower = response.lower()
        self.query_lower = query.lower()

    # ---------- Sub-scorers ----------

    def _count_overconfidence(self) -> int:
        count = 0
        for pat in OVERCONFIDENCE_PATTERNS:
            count += len(re.findall(pat, self.response, re.IGNORECASE))
        return count

    def _count_hedging(self) -> int:
        count = 0
        for pat in HEDGING_PATTERNS:
            count += len(re.findall(pat, self.response, re.IGNORECASE))
        return count

    def _count_vague_authority(self) -> int:
        return sum(1 for phrase in VAGUE_AUTHORITY_PHRASES if phrase in self.response_lower)

    def _count_quality_indicators(self) -> int:
        return sum(1 for qi in QUALITY_INDICATORS if qi in self.response_lower)

    def _keyword_overlap(self) -> float:
        stop = {'what', 'is', 'are', 'was', 'how', 'why', 'when', 'the', 'a', 'an', 'and', 'or', 'of', 'in', 'to'}
        query_words = set(re.findall(r'\b\w{4,}\b', self.query_lower)) - stop
        resp_words = set(re.findall(r'\b\w{4,}\b', self.response_lower)) - stop
        if not query_words:
            return 0.6
        overlap = query_words & resp_words
        return round(min(len(overlap) / len(query_words), 1.0), 4)

    def _response_length_score(self) -> float:
        words = len(self.response.split())
        # Ideal: 50–300 words. Too short = suspicious, too long = padding
        if words < 20:
            return 0.2
        elif words < 50:
            return 0.5
        elif words <= 300:
            return 1.0
        else:
            return 0.85

    def _sentence_coherence(self) -> float:
        sentences = [s.strip() for s in re.split(r'[.!?]+', self.response) if len(s.strip()) > 8]
        if not sentences:
            return 0.3
        avg_len = sum(len(s.split()) for s in sentences) / len(sentences)
        # Ideal sentence: 10–25 words
        coherence = min(avg_len / 18, 1.0) if avg_len <= 18 else max(1.0 - (avg_len - 18) / 40, 0.5)
        return round(coherence, 4)

    def _suspicious_numeric_count(self) -> int:
        return len(re.findall(SUSPICIOUS_NUMERIC_PATTERN, self.response))

    def _collect_flags(self) -> List[str]:
        flags = []
        for pat in OVERCONFIDENCE_PATTERNS:
            matches = re.findall(pat, self.response, re.IGNORECASE)
            flags.extend(matches[:2])
        return list(set(flags))[:6]

    def _collect_suspicious_phrases(self) -> List[str]:
        found = [p for p in VAGUE_AUTHORITY_PHRASES if p in self.response_lower]
        hedges = []
        for pat in HEDGING_PATTERNS:
            m = re.findall(pat, self.response, re.IGNORECASE)
            hedges.extend(m[:1])
        return list(set(found + hedges))[:6]

    # ---------- Composite scores ----------

    def _compute_factual_consistency(self, overconf: int, vague: int) -> float:
        penalty = overconf * 0.04 + vague * 0.07
        return round(max(0.0, 1.0 - penalty), 4)

    def _compute_confidence_score(self, quality: int, length_score: float, hedging: int) -> float:
        base = 0.45 + (quality * 0.04) + (length_score * 0.3) - (hedging * 0.03)
        return round(min(max(base, 0.0), 1.0), 4)

    def _compute_hallucination_pct(self, factual: float, confidence: float, overlap: float) -> float:
        # Weighted combination of inverse-quality signals
        raw = (1 - factual) * 0.40 + (1 - confidence) * 0.30 + (1 - overlap) * 0.30
        return round(min(raw * 100, 100.0), 2)

    def _compute_accuracy(self, factual: float, overlap: float) -> float:
        return round((factual * 0.55 + overlap * 0.45), 4)

    def _compute_consistency(self, coherence: float, factual: float) -> float:
        return round((coherence * 0.5 + factual * 0.5), 4)

    def _compute_fluency(self, coherence: float, length_score: float) -> float:
        return round((coherence * 0.6 + length_score * 0.4), 4)

    # ---------- Public method ----------

    def analyze(self) -> Dict:
        overconf = self._count_overconfidence()
        hedging = self._count_hedging()
        vague = self._count_vague_authority()
        quality = self._count_quality_indicators()
        overlap = self._keyword_overlap()
        coherence = self._sentence_coherence()
        length_score = self._response_length_score()

        factual = self._compute_factual_consistency(overconf, vague)
        confidence = self._compute_confidence_score(quality, length_score, hedging)
        hall_pct = self._compute_hallucination_pct(factual, confidence, overlap)
        accuracy = self._compute_accuracy(factual, overlap)
        consistency = self._compute_consistency(coherence, factual)
        fluency = self._compute_fluency(coherence, length_score)

        is_hallucinated = hall_pct > 42.0

        return {
            'factual_consistency': factual,
            'confidence_score': confidence,
            'accuracy_score': accuracy,
            'consistency_score': consistency,
            'fluency_score': fluency,
            'similarity_score': round(overlap, 4),
            'hallucination_score': round(hall_pct / 100, 4),
            'hallucination_percentage': hall_pct,
            'is_hallucinated': is_hallucinated,
            'keyword_mismatch_count': overconf + hedging,
            'suspicious_phrases': ', '.join(self._collect_suspicious_phrases()),
            'rule_based_flags': ', '.join(self._collect_flags()),
            'semantic_similarity': overlap,
            'analysis_notes': (
                f"Overconfidence: {overconf}, Hedging: {hedging}, Vague authority: {vague}, "
                f"Quality markers: {quality}, Keyword overlap: {round(overlap*100)}%, "
                f"Response words: {len(self.response.split())}"
            ),
        }
