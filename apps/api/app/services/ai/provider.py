"""Grounded answer provider (ported from V1's AI abstraction, PRD §8).

The provider only ever sees retrieved chunks from the student's own courses, and
the prompt tells it to answer *only* from them. Retrieval and the honest-decline
decision happen in `ask.py` before the provider is called, so swapping providers
cannot weaken the rule that an answer must be grounded.

`ExtractiveProvider` is the default when no API key is configured: it composes an
answer from the best-matching sentences of the retrieved material. It is not a
language model, and the UI says so; it exists so local development, tests and a
provider outage still produce a grounded answer instead of an error or a guess.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol

from app.core.config import get_settings

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
WORD = re.compile(r"[a-z0-9]+")

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "do", "does", "for",
    "from", "how", "i", "in", "is", "it", "of", "on", "or", "that", "the", "this",
    "to", "was", "what", "when", "where", "which", "who", "why", "with", "you",
    "your", "me", "my", "we", "our", "us", "explain", "define", "tell",
}


def terms(text: str) -> set[str]:
    return {
        word
        for word in WORD.findall(text.lower())
        if len(word) > 2 and word not in STOPWORDS
    }


@dataclass(frozen=True)
class ContextChunk:
    chunk_id: int
    material_id: int
    material_title: str
    course_code: str | None
    content: str


class ProviderError(RuntimeError):
    pass


class AnswerProvider(Protocol):
    name: str

    def answer(self, question: str, chunks: list[ContextChunk]) -> str: ...


class ExtractiveProvider:
    """Compose an answer from the most relevant sentences of the retrieved text."""

    name = "extractive"

    def answer(self, question: str, chunks: list[ContextChunk]) -> str:
        question_terms = terms(question)
        scored: list[tuple[int, str]] = []
        for chunk in chunks:
            for sentence in SENTENCE_SPLIT.split(chunk.content):
                sentence = sentence.strip()
                if len(sentence) < 20:
                    continue
                overlap = len(question_terms & terms(sentence))
                if overlap:
                    scored.append((overlap, sentence))
        scored.sort(key=lambda item: (-item[0], len(item[1])))
        if not scored:
            return "The material I have does not answer that directly."
        best = [sentence for _score, sentence in scored[:3]]
        return " ".join(best)


class OpenRouterProvider:
    """An OpenAI-compatible chat completion, grounded on the retrieved chunks."""

    name = "openrouter"

    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def answer(self, question: str, chunks: list[ContextChunk]) -> str:
        import httpx

        context = "\n\n".join(
            f"[{index + 1}] ({chunk.material_title}, {chunk.course_code or 'course'})\n{chunk.content}"
            for index, chunk in enumerate(chunks)
        )
        prompt = (
            "You are a study assistant for a university student. Answer ONLY from the "
            "numbered material below. If it does not contain the answer, say so plainly. "
            "Do not invent facts. Keep the answer short and refer to sources as [1], [2].\n\n"
            f"MATERIAL:\n{context}\n\nQUESTION: {question}"
        )
        try:
            response = httpx.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                    "max_tokens": 400,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
            return str(data["choices"][0]["message"]["content"]).strip()
        except Exception as exc:  # noqa: BLE001 - normalise to one provider failure
            raise ProviderError(str(exc)) from exc


def get_provider() -> AnswerProvider:
    settings = get_settings()
    if settings.OPENROUTER_API_KEY:
        return OpenRouterProvider(settings.OPENROUTER_API_KEY, settings.OPENROUTER_MODEL)
    return ExtractiveProvider()
