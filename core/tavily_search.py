from __future__ import annotations

from typing import Any


class SearchProviderError(RuntimeError):
    """Raised when the configured search provider cannot return results."""


def _get_client(api_key: str) -> Any:
    try:
        from tavily import TavilyClient
    except ImportError as exc:
        raise SearchProviderError(
            "Tavily integration is not installed. Install dependencies with: "
            "python3 -m pip install -r requirements.txt"
        ) from exc
    return TavilyClient(api_key=api_key)


def search_grants(query: str, api_key: str, max_results: int = 8) -> list[dict[str, Any]]:
    if not api_key:
        raise SearchProviderError("SEARCH_API_KEY is not configured.")
    if api_key.strip().lower() in {"your_key_here", "your-api-key", "changeme", "replace_me"}:
        raise SearchProviderError(
            "SEARCH_API_KEY still contains a placeholder. Replace it with a real Tavily API key."
        )

    grant_query = (
        f"{query}. Find current U.S. grants for a for-profit small business. "
        "Prefer official program pages, eligibility, award amount, and deadline."
    )
    try:
        response = _get_client(api_key).search(
            query=grant_query[:399],
            search_depth="advanced",
            max_results=max_results,
            include_domains=[
                "grants.gov",
                "sba.gov",
                "challenge.gov",
                "usda.gov",
                "commerce.gov",
                "energy.gov",
            ],
        )
    except Exception as exc:
        raise SearchProviderError(f"Tavily search failed: {exc}") from exc

    if not isinstance(response, dict) or not isinstance(response.get("results"), list):
        raise SearchProviderError("Tavily returned an invalid search response.")

    results = []
    for item in response["results"]:
        if not isinstance(item, dict) or not item.get("url") or not item.get("title"):
            continue
        results.append(
            {
                "title": str(item["title"]),
                "url": str(item["url"]),
                "summary": str(item.get("content") or "").strip(),
                "published_date": item.get("published_date"),
                "score": item.get("score"),
            }
        )
    return results


def search_web(query: str, api_key: str, max_results: int = 8) -> list[dict[str, Any]]:
    if not api_key:
        raise SearchProviderError("SEARCH_API_KEY is not configured.")
    if api_key.strip().lower() in {"your_key_here", "your-api-key", "changeme", "replace_me"}:
        raise SearchProviderError(
            "SEARCH_API_KEY still contains a placeholder. Replace it with a real Tavily API key."
        )

    try:
        response = _get_client(api_key).search(
            query=query[:399],
            search_depth="advanced",
            max_results=max_results,
        )
    except Exception as exc:
        raise SearchProviderError(f"Tavily search failed: {exc}") from exc

    if not isinstance(response, dict) or not isinstance(response.get("results"), list):
        raise SearchProviderError("Tavily returned an invalid search response.")

    return [
        {
            "title": str(item["title"]),
            "url": str(item["url"]),
            "summary": str(item.get("content") or "").strip(),
            "published_date": item.get("published_date"),
            "score": item.get("score"),
        }
        for item in response["results"]
        if isinstance(item, dict) and item.get("title") and item.get("url")
    ]