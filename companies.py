WATCHLIST = {
    "Samsung": ["samsung"],
    "Google": ["google", "alphabet"],
    "OpenAI": ["openai", "chatgpt"],
    "Jaguar": ["jaguar"],
    "Royal Mail": ["royal mail"],
    "Amazon": ["amazon"],
    "Barclays": ["barclays"],
}


def match_companies(title):
    text = title.lower()
    found = []
    for company, words in WATCHLIST.items():
        for word in words:
            if word in text:
                found.append(company)
                break
    return found
