def format_name(name: str) -> str:
    """
    Format a string converting tildes to their corresponding letter without tilde and lowercasing the string.
    Args:
        name (str): The string to be formatted.
    Returns:
        str: The formatted string.
    """
    tildes_map = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N'
    }
    formatted_name = ''.join(tildes_map.get(char, char) for char in name)

    return formatted_name.lower()
