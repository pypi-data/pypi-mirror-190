from pathlib import Path
import pydra.mark
from fileformats.core.mark import converter
from fileformats.generic import File
from fileformats.text import Plain as PlainText
from . import EncodedText


@converter(source_format=EncodedText, target_format=PlainText, out_file="out_file.txt")
@converter(source_format=PlainText, target_format=EncodedText, out_file="out_file.enc")
@pydra.mark.task
def encoder_task(
    in_file: File,
    out_file: str,
    shift: int = 0,
) -> File:
    with open(in_file) as f:
        contents = f.read()
    encoded = encode_text(contents, shift)
    with open(out_file, "w") as f:
        f.write(encoded)
    return Path(out_file).absolute()


def encode_text(text: str, shift: int) -> str:
    encoded = []
    for c in text:
        encoded.append(chr(ord(c) + shift))
    return "".join(encoded)
