from ._version import __version__
from fileformats.core import import_converters
from fileformats.generic import File
from fileformats.serialization import Json
from fileformats.core.mixin import WithSideCar, WithSeparateHeader


class Y(File):
    ext = ".y"


class Xy(WithSideCar, File):

    ext = ".x"
    side_car_type = Y


class MyFormat(File):

    ext = ".my"


class MyFormatGz(MyFormat):

    ext = ".my.gz"


class MyFormatX(WithSideCar, MyFormat):

    side_car_type = Json


class YourFormat(File):

    ext = ".yr"


class SeparateHeader(File):

    ext = ".hdr"


class ImageWithHeader(WithSeparateHeader, File):

    ext = ".img"
    header_type = SeparateHeader


class MyFormatGzX(MyFormatX, MyFormatGz):

    pass


class EncodedText(File):
    """A text file where the characters ASCII codes are shifted on conversion
    from text
    """

    ext = ".enc"


import_converters(__name__)
