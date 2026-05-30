"""Voice pattern validator to ensure output matches Bartlett/Hormozi style."""

from __future__ import annotations

import re
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup


class VoiceValidator:
    """Validates text against Bartlett/Hormozi voice fingerprints."""
    
    # Key patterns that should appear in authentic Bartlett/Hormozi style
    VOICE_PATTERNS = {
        "contractions": [r"\b(don't|won't|can't|didn't|isn't|aren't|wasn't|weren't|you're|we're|they're|it's|that's|here's|there's|what's|who's|I'm|I've|I'd)\b"],
        "direct_questions": [r"\?\s*$"],
        "short_punchy_sentences": [r"^[^.!?]{10,40}[.!?]\s*$"],  # 10-40 chars
        "numbers_specificity": [r"\b\d+[%$]?\b", r"\b\d+x\b", r"\b\d+:\d+\b"],
        "action_verbs": [(r"\b(stop|start|fix|cut|build|ship|scale|launch|fire|hire|sell|buy|earn|lose|win|fail|ask|give|take)\b", re.IGNORECASE)],
        "frameworks": [(r"\b\d+\)"), (r"^-\s+"), (r"^•\s+"), (r"playbook", re.IGNORECASE)],
        "emotional_hooks": [(r"\b(fear|scared|failed|lost|mistake|wrong|arrogant|stupid|desperate)\b", re.IGNORECASE)],
        "absolutes": [(r"\b(always|never|every|all|none|only)\b", re.IGNORECASE)],
    }
    
    # Anti-patterns that signal drift from authentic voice
    ANTI_PATTERNS = {
        "hedging": [(r"\b(might|maybe|perhaps|possibly|potentially|somewhat|fairly|quite|rather)\b", re.IGNORECASE)],
        "fluff_openers": [(r"^(In today's|Let's dive|Welcome to|In this)", re.IGNORECASE)],
        "generic_praise": [(r"\b(interesting|amazing|wonderful|great|fantastic)\b(?!\s+because)", re.IGNORECASE)],
        "formal_language": [(r"\b(utilize|facilitate|leverage|optimize|synergy|paradigm|robust)\b", re.IGNORECASE)],
        "passive_voice": [r"\b(is|are|was|were|be|been|being)\s+\w+ed\b"],
    }
    
    def __init__(self):
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Pre-compile all regex patterns for efficiency."""
        self.compiled_positive = {}
        for category, patterns in self.VOICE_PATTERNS.items():
            compiled = []
            for p in patterns:
                if isinstance(p, tuple):
                    # Pattern with flags
                    compiled.append(re.compile(p[0], p[1]))
                elif isinstance(p, str):
                    # Plain pattern
                    compiled.append(re.compile(p))
            self.compiled_positive[category] = compiled
        
        self.compiled_negative = {}
        for category, patterns in self.ANTI_PATTERNS.items():
            compiled = []
            for p in patterns:
                if isinstance(p, tuple):
                    compiled.append(re.compile(p[0], p[1]))
                elif isinstance(p, str):
                    compiled.append(re.compile(p))
            self.compiled_negative[category] = compiled
    
    def validate_html(self, html_content: str) -> Dict[str, any]:
        """Validate HTML content and return detailed scoring."""
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text(" ", strip=True)
        return self.validate_text(text)
    
    def validate_text(self, text: str) -> Dict[str, any]:
        """
        Validate text against voice patterns.
        Returns dict with score (0-100) and detailed breakdown.
        """
        if not text or len(text.strip()) < 50:
            return {"score": 0, "valid": False, "reason": "Text too short"}
        
        sentences = self._split_sentences(text)
        
        # Calculate positive signals
        positive_scores = {}
        for category, patterns in self.compiled_positive.items():
            matches = sum(1 for p in patterns for _ in p.finditer(text))
            positive_scores[category] = matches
        
        # Calculate negative signals (anti-patterns)
        negative_scores = {}
        for category, patterns in self.compiled_negative.items():
            matches = sum(1 for p in patterns for _ in p.finditer(text))
            negative_scores[category] = matches
        
        # Sentence length analysis
        sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
        avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
        short_sentences_ratio = sum(1 for l in sentence_lengths if l <= 15) / len(sentence_lengths) if sentence_lengths else 0
        
        # Calculate overall score
        score = 50  # Start at neutral
        
        # Positive signals (add points)
        score += min(20, positive_scores["contractions"] * 2)  # Max 20 points
        score += min(15, positive_scores["direct_questions"] * 5)  # Max 15 points
        score += min(10, positive_scores["numbers_specificity"])  # Max 10 points
        score += min(10, positive_scores["action_verbs"] * 0.5)  # Max 10 points
        score += min(5, positive_scores["frameworks"] * 2)  # Max 5 points
        
        # Negative signals (subtract points)
        score -= min(15, negative_scores["hedging"] * 3)
        score -= min(10, negative_scores["fluff_openers"] * 5)
        score -= min(10, negative_scores["generic_praise"] * 2)
        score -= min(10, negative_scores["formal_language"] * 2)
        score -= min(5, negative_scores["passive_voice"] * 0.5)
        
        # Sentence length scoring
        if 8 <= avg_sentence_length <= 20:
            score += 10  # Ideal range
        elif avg_sentence_length > 30:
            score -= 15  # Too long, not punchy enough
        
        if short_sentences_ratio >= 0.4:
            score += 10  # Good mix of short sentences
        
        # Clamp score between 0-100
        score = max(0, min(100, score))
        
        result = {
            "score": round(score, 1),
            "valid": score >= 70,
            "positive_signals": positive_scores,
            "negative_signals": negative_scores,
            "sentence_analysis": {
                "avg_length": round(avg_sentence_length, 1),
                "short_ratio": round(short_sentences_ratio, 2),
                "total_sentences": len(sentences),
            },
            "suggestions": self._generate_suggestions(positive_scores, negative_scores, avg_sentence_length),
        }
        
        return result
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitter
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _generate_suggestions(self, positive: Dict, negative: Dict, avg_length: float) -> List[str]:
        """Generate specific improvement suggestions."""
        suggestions = []
        
        if positive["contractions"] < 3:
            suggestions.append("Use more contractions (don't, won't, it's) - sounds too formal")
        
        if positive["direct_questions"] < 1:
            suggestions.append("Add direct questions to force reader action/reflection")
        
        if positive["numbers_specificity"] < 5:
            suggestions.append("Add specific numbers, percentages, or dollar amounts")
        
        if negative["hedging"] > 3:
            suggestions.append("Remove hedging language (might, maybe, perhaps) - be more direct")
        
        if negative["fluff_openers"] > 0:
            suggestions.append("Remove fluff openers like 'In today's newsletter' or 'Let's dive in'")
        
        if negative["formal_language"] > 2:
            suggestions.append("Replace formal language with plain words")
        
        if avg_length > 25:
            suggestions.append("Shorten sentences - mix punchy one-liners with longer explanations")
        
        if positive["emotional_hooks"] < 1:
            suggestions.append("Add emotional vulnerability (fear, mistake, failure)")
        
        return suggestions


def validate_and_score(text_or_html: str) -> Dict[str, any]:
    """Convenience function to validate text or HTML."""
    validator = VoiceValidator()
    if text_or_html.strip().startswith("<"):
        return validator.validate_html(text_or_html)
    return validator.validate_text(text_or_html)
