from pygments import highlight
from pygments.lexers import get_lexer_by_name


def convert_code_to_html(serializer, formatter):
    html_code = highlight(
        serializer.data["content"],
        get_lexer_by_name(serializer.data["lexer"]["name"]),
        formatter,
    )
    paste = dict(serializer.data)
    paste["content"] = html_code

    return paste
