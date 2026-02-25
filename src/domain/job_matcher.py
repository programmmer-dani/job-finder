def search_matching_position(html, position_keywords):
    if not html or not position_keywords:
        return False
    formatted_html = html.lower()
    for keyword in position_keywords:
        if keyword.strip().lower() in formatted_html:
            return True
    return False