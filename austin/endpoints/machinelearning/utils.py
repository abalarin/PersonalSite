import codecs
import markdown
from flask import Markup

from austin.config import Config


def load_md(filename):

    filepath = Config.APP_ROOT + "/static/markdown/" + filename
    input_file = codecs.open(filepath, mode="r", encoding="utf-8")
    text = input_file.read()

    html = markdown.markdown(text)
    html = Markup(html)
    return html
