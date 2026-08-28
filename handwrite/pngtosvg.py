from PIL import Image, ImageChops
import os
import shutil
import subprocess


class PotraceNotFound(Exception):
    pass


class PNGtoSVG:
    """Converter class to convert character PNGs to BMPs and SVGs."""

    def convert(self, directory):
        """Call converters on each .png in the provider directory.

        Walk through the custom directory containing all .png files
        from sheettopng and convert them to png -> bmp -> svg.
        """
        path = os.walk(directory)
        for root, dirs, files in path:
            for f in files:
                if f.endswith(".png"):
                    self.pngToBmp(root + "/" + f)
                    # self.trim(root + "/" + f[0:-4] + ".bmp")
                    self.bmpToSvg(root + "/" + f[0:-4] + ".bmp")

    def bmpToSvg(self, path):
        """Convert .bmp image to .svg using potrace.

        Converts the passed .bmp file to .svg using the potrace
        (http://potrace.sourceforge.net/). Each .bmp is passed as
        a parameter to potrace which is called as a subprocess.

        Parameters
        ----------
        path : str
            Path to the bmp file to be converted.

        Raises
        ------
        PotraceNotFound
            Raised if potrace not found in path by shutil.which()
        """
        if shutil.which("potrace") is None:
            raise PotraceNotFound("Potrace is either not installed or not in path")
        else:
            subprocess.run(["potrace", path, "-b", "svg", "-o", path[0:-4] + ".svg"])

    def pngToBmp(self, path):
        """Convert .bmp image to .svg using potrace.

        Converts the passed .bmp file to .svg using the potrace
        (http://potrace.sourceforge.net/). Each .bmp is passed as
        a parameter to potrace which is called as a subprocess.

        Parameters
        ----------
        path : str
            Path to the bmp file to be converted.

        Raises
        ------
        PotraceNotFound
            Raised if potrace not found in path by shutil.which()
        """
        img = Image.open(path).convert("RGBA").resize((100, 100))

        # Threshold image to convert each pixel to either black or white
        threshold = 200
        data = []
        for pix in img.get_flattened_data():
            if pix[0] >= threshold and pix[1] >= threshold and pix[3] >= threshold:
                data.append((255, 255, 255, 0))
            else:
                data.append((0, 0, 0, 1))
        img.putdata(data)
        img.save(path[0:-4] + ".bmp")

    def trim(self, im_path):
        im = Image.open(im_path)
        bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
        diff = ImageChops.difference(im, bg)
        bbox = list(diff.getbbox())
        bbox[0] -= 1
        bbox[1] -= 1
        bbox[2] += 1
        bbox[3] += 1
        cropped_im = im.crop(bbox)
        cropped_im.save(im_path)
