import re


def get_selection_link(element, selector):
    result = element.select(selector)
    if result:
        return result[0].attrs["href"]
    return ""


def get_selection_text(element, selector, separator):
    result = element.select(selector)
    if result:
        text = result[0].get_text(separator)
        text = re.sub(r"\s\s+", " ", text)
        text = re.sub(r"\s([.,])", r"\1", text)  # remove extra white spaces
        return text.strip()
    return ""
