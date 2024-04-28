"""Load ascii art for schwa7."""

import text_to_image
import os

def schwa_text_fn() -> str:

    parent = os.path.dirname(__file__)
    path = os.path.join(parent, "schwa.txt")
    return open(path, "r").read()

schwa_text = schwa_text_fn()
