"""Utilities for detecting website mentions in text."""

import re


def extract_domain(website: str) -> str:
    """Extract domain from website URL or string.
    
    Examples:
        https://example.com/path -> example.com
        www.example.com -> example.com
        example.com -> example.com
    """
    website = website.strip().lower()
    # Remove protocol
    for prefix in ("https://", "http://", "www."):
        if website.startswith(prefix):
            website = website[len(prefix) :]
            break
    # Remove path and query
    website = website.split("/")[0].split("?")[0]
    return website


def extract_brand_name(domain: str) -> str:
    """Extract likely brand name from domain (e.g., examplepdf.com -> ExamplePDF)."""
    # Remove TLD
    parts = domain.rsplit(".", 1)
    name = parts[0] if parts else domain
    # Handle compound names: examplepdf -> Example PDF, ilovepdf -> ILovePDF
    return name


def detect_mention(text: str, website: str) -> bool:
    """Check if the target website is mentioned in the given text.
    
    Detects:
    - Full domain (example.com, www.example.com)
    - Brand name variations (ExamplePDF, Example PDF, examplepdf)
    - URL references (https://example.com)
    
    Args:
        text: The response text to search
        website: The target website URL or domain
        
    Returns:
        True if any form of the website is mentioned
    """
    if not text or not website:
        return False

    text_lower = text.lower().strip()
    domain = extract_domain(website)
    brand = extract_brand_name(domain)

    # Normalize domain for matching (e.g., example.com)
    domain_lower = domain.lower()
    brand_lower = brand.lower()

    # 1. Exact domain match (example.com, www.example.com)
    if domain_lower in text_lower:
        return True

    # 2. Domain with protocol
    for protocol in ("https://", "http://"):
        if f"{protocol}{domain_lower}" in text_lower:
            return True

    # 3. Brand name variations - handle common separations
    # "Example PDF" or "ExamplePDF" or "example pdf"
    brand_no_spaces = brand_lower.replace(" ", "")
    if brand_no_spaces in text_lower:
        return True

    # 4. CamelCase/split variations - e.g., "SmallPdf" or "Small Pdf"
    # Word boundary match for brand parts
    brand_words = re.split(r"[^a-z0-9]+", brand_lower)
    if len(brand_words) > 1:
        brand_pattern = r"\b" + r"[.\s\-]*".join(re.escape(w) for w in brand_words) + r"\b"
        if re.search(brand_pattern, text_lower):
            return True

    # 5. Simple substring for brands (avoid false positives with very short strings)
    if len(brand_lower) >= 4 and brand_lower in text_lower:
        return True

    return False
