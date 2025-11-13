from bs4 import BeautifulSoup

def get_tm_org(soup: BeautifulSoup) -> str:
    """
    Extract Talent Market org name cleanly and remove the 'About the' prefix.
    """
    about = soup.find(string=lambda t: isinstance(t, str) and "about the" in t.lower())
    if not about:
        return None

    parent = about.find_parent()
    if not parent:
        return None

    text = parent.get_text(" ", strip=True)

    # remove "About the" from the beginning
    if text.lower().startswith("about the "):
        text = text[10:].strip()  # length of 'About the '

    # only take first sentence
    text = text.split(".")[0].strip()

    return text or None

