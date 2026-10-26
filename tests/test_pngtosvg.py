import os
import tempfile
import unittest

from PIL import Image

from handwrite.pngtosvg import PNGtoSVG


class TestPNGtoSVG(unittest.TestCase):
    def setUp(self):
        self.directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "test_data" + os.sep + "pngtosvg",
        )
        self.converter = PNGtoSVG()

    def test_bmpToSvg(self):
        self.converter.bmpToSvg(self.directory + os.sep + "45.bmp")
        self.assertTrue(os.path.exists(self.directory + os.sep + "45.svg"))
        os.remove(self.directory + os.sep + "45.svg")

    def test_pngToBmp_threshold(self):
        # Background is white or transparent white; ink is anything that is not
        # bright in all of R, G and B (e.g. a yellow pen stroke).
        pixels = {
            (0, 0): ((255, 255, 255, 255), "background"),
            (1, 0): ((255, 255, 255, 0), "background"),
            (2, 0): ((0, 0, 0, 255), "ink"),
            (3, 0): ((255, 255, 0, 255), "ink"),
        }
        with tempfile.TemporaryDirectory() as tmp:
            png = os.path.join(tmp, "65.png")
            img = Image.new("RGBA", (100, 100), (255, 255, 255, 255))
            for xy, (color, _) in pixels.items():
                img.putpixel(xy, color)
            img.save(png)

            self.converter.pngToBmp(png)

            with Image.open(os.path.join(tmp, "65.bmp")) as bmp:
                bmp = bmp.convert("RGB")
                for xy, (color, expected) in pixels.items():
                    actual = "ink" if bmp.getpixel(xy) == (0, 0, 0) else "background"
                    self.assertEqual(actual, expected, f"pixel {color}")

    def test_convert(self):
        self.converter.convert(self.directory)
        path = os.walk(self.directory)
        for root, dirs, files in path:
            for f in files:
                if f[-4:] == ".png":
                    self.assertTrue(os.path.exists(root + os.sep + f[0:-4] + ".bmp"))
                    self.assertTrue(os.path.exists(root + os.sep + f[0:-4] + ".svg"))
                    os.remove(root + os.sep + f[0:-4] + ".bmp")
                    os.remove(root + os.sep + f[0:-4] + ".svg")
