import base64
import json
import zlib

from factorio.blueprint.objects.blueprint import Blueprint


def deserialize_factorio_format(b):
    decoded = base64.b64decode(b[1:])
    decompressed = zlib.decompress(decoded)
    return json.loads(decompressed)


def serialize_factorio_format(json_obj):
    decompressed = json.dumps(json_obj, separators=(',', ':')).encode('ascii')
    compressed = zlib.compress(decompressed, level=9)
    return (b'0' + base64.b64encode(compressed)).decode("ascii")


if __name__ == '__main__':
    _sample_str = "0eNqtXFtuGzkQvMt8S8HwTfoqgbGQ5VlnEFkSJDlYI/DddyQnkhWzzOp2/uIgLlY3m+xHcfKzu1s9DdvduD50Nz+7cblZ77ubrz" \
                 "+7/fiwXqyOf3d43g7dTTcehsdu1q0Xj8efNuNqvhv+HdfD7rl7mXXj+n74r7sxL7Pmry6/DY/jcrGab1eLadXLL9uX21k3rA" \
                 "/jYRxeSZx+eP5n/fR4N+wm9DPG/rDZLR6G+WGx/j4hbzf76Zc26+OaRxa+fAmz7nmCjF/CtMD9uBuWr//AHhn+gWsRt4+Qy5" \
                 "/IftZNfx5PFq+e7nYTzsm8d8s51ozgfy3mesYMf8bdHllU8PrfeGbCqyCEJoJpIMQmgm0gpDPC43A/Pj3Oh9Vk9OTN+Xaz" \
                 "+piTPXlpPYwP3+42T7tjDJm+v60skq9ozg+b+cNu87S+/5CwrRMuLZNd+o3g6wim5yECgDC8RS6/5XMVVrEGbXlo7yB0LWKNaxl" \
                 "+AUSGewE7LzM8aKADBd08J+eLBhqeBOyKbFsyf5MgdoWHAKfC9oJDakQ7a40GOlC5xPI3IPCddQJ2sgNnvQaaCmnbTh6" \
                 "+ZXjkIVDQCE5FCLKgyRpoLmiKADqJdtw1c0uIjW1xRsOOChrXPi25xc7xECBonORUFFHQuKCBpoLGRR46GlnQpJZPYysBuKxhxw" \
                 "VNM7fE1hXrex4CBI0XnIroREHjrQaaChovyC0xiILGN/uP2EoAPmjYUUHjm7kltu5BL8gtMcl2PPPsUDwWDTsqaIKgEotFtC3" \
                 "BNA1vJYBg+e4pAgjHQyQA4euzkUoxfr468zvnvxkhHFG2u81y2O/H9cP827D48VybJoSgac+QFZFvyJAvVX0JAsv8aOZSqKe" \
                 "TX8+ePLlufvTncrdYfp+8WfVjESwVPrVU7AVLlc8tZfilovvcUoIxWkyfW0qQxVyEx83XoJtZ7AJYwAws8LcJghDUdhewDMA" \
                 "Sf6gRhKCa8wE6vJYBYtFMWYDfUrOuu0AAU5PRmFqY2EqSSVrGWaIG7fiBEjLc8xDI/YIBMoKI/OAIQTTj/TLaQBCZn+IgiPYE" \
                 "LDQgcs/PQxBEs74KrbsoW36CgCDaPXortLLn23wE0YzO2IrOHPnGGEG0e+tWdObMd68Iot1Dt6Kz9Hy/hyCMpmcpTFoplu+oE" \
                 "DtBlZEwu9p1XTyrAabfB+PYNlRZBkUtBMH4+h9CJDoFQ4hmfJ8TL4QoiizuDdLnerEoeUXwD1EyzUxvZibF2+piRrpY9B8sdiR" \
                 "vcqovZRVl5jEC2rWO6Z24IfbhbzTEpvdSB14Y1CTkCJwX+LPiUGBFRfP+i2RzAzSNOLu5fH2EbS8KLeo9v6q8anqFVvMeuyqOGk" \
                 "PXQ9B2iaYektB2p5AcWNs9Xf9g24NCGWBtj4rJOWt7ousdbHtWDLhZ2zUDYNJ229NjWmi7NfKah2RnNSVQoG46iRh/SZHoVYT" \
                 "19GjIo8dCVpB3IA9V3oGMBCUfZJQVYyDvuT0s9GQD2ug0r1E8987IGXrmgflZxaTcx+vp62oqew7N6ashJHfb5Kt5ieLJV2X8" \
                 "UxTML2oqCHK/k0Jq0O5V5qsV6AvN8xRyr9pK/HmuA/lJpPhQZHvlrUKrUe6Vd3x1BX3hNdUVuVeBnjthfqoKjdyrpBC7tHuV+" \
                 "WoQ+qJoqkFur0SafZL5mRDtm3dK0KiFyr0KTvF+gfWF5ytj6IugGDSycRD5ijMifklTXyeElmmFFTMqfA2MeEReK8QYhp9UQg" \
                 "yrGVVGqvKVCOUXa5HXo+St/VUcEA/iA1+jQ09Ghb76nl/1HMWkHyqW2lTWz0yqfptiRGK7u16kGRCquXhGnyCI5+IXt+fqpB" \
                 "VOxZPh4wPStbQ8jTEc36tBDM/3TxAj0CI3xoh6WaMApSFhtYHQ5X2TcqZVdYxR+JYIYRDSfGpiGL71gRiWVtYxhqDtgBie1tY" \
                 "xhqC9gBiRVtcxRtILcNVjgbW+LOgiIF1eyocYRdUtUO+7TBF0C5Cf1VTI1MspU5x8Ll0QT6+YFoeeSt2Ff1YYkJD9Rt9nRdlg" \
                 "/4ooW5KiqMF2ZLr+Dz3C0Dw8PDFq7pV982CAjamKn6vIho8Chz6s1OglwXKWO7q7w/xUp8giNF4vwRhRUTYHx3ksaeIQ+i7TX" \
                 "S22tmjiA32R2f66/eJ/iGF4qyCGps8O6FNV4tP1cMXodvb6/2DcvPkfN2bdj2G3fz3s2fhUbPIu+mLzy8v/fXRhuA=="

    assert _sample_str == serialize_factorio_format(deserialize_factorio_format(_sample_str))

    b = Blueprint.from_json(deserialize_factorio_format(_sample_str))

    import pyperclip
    pyperclip.copy(serialize_factorio_format(b.to_json()))
    pass
