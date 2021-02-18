import os
import itertools
import json

import cv2

# Seq: A-Z, a-z, 0-9, SPECIAL_CHARS
ALL_CHARS = list(
    itertools.chain(
        range(65, 91),
        range(97, 123),
        range(48, 58),
        [ord(i) for i in ".,;:!?\"'-+=/%&()[]"],
    )
)




class SheetToPNG:



    """Converter class to convert input sample sheet to character PNGs."""

    def convert(self, sheet, characters_dir, config, cols=8, rows=10):
        """Convert a sheet of sample writing input to a custom directory structure of PNGs.

        Detect all characters in the sheet as a separate contours and convert each to
        a PNG image in a temp/user provided directory.

        Parameters
        ----------
        sheet : str
            Path to the sheet file to be converted.
        characters_dir : str
            Path to directory to save characters in.
        config: str
            Path to config file.
        cols : int, default=8
            Number of columns of expected contours. Defaults to 8 based on the default sample.
        rows : int, default=10
            Number of rows of expected contours. Defaults to 10 based on the default sample.
        """
        with open(config) as f:
            threshold_value = json.load(f).get("threshold_value", 200)
        characters = self.detect_characters(
            sheet, threshold_value, cols=cols, rows=rows
        )
        self.save_images(
            characters,
            characters_dir
        )



    def detect_characters(self, sheet_image, threshold_value, cols=8, rows=10):
        """Detect contours on the input image and filter them to get only characters.

        Uses opencv to threshold the image for better contour detection. After finding all
        contours, they are filtered based on area, cropped and then sorted sequentially based
        on coordinates. Finally returs the cols*rows top candidates for being the character
        containing contours.

        Parameters
        ----------
        sheet : str
            Path to the sheet file to be converted.
        threshold_value : int
            Value to adjust thresholding of the image for better contour detection.
        cols : int, default=8
            Number of columns of expected contours. Defaults to 8 based on the default sample.
        rows : int, default=10
            Number of rows of expected contours. Defaults to 10 based on the default sample.

        Returns
        -------
        sorted_characters : list of list
            Final rows*cols contours in form of list of list arranged as:
            sorted_characters[x][y] denotes contour at x, y position in the input grid.
        """
        # TODO Raise errors and suggest where the problem might be

        # Read the image and convert to grayscale
        image = cv2.imread(sheet_image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Threshold and filter the image for better contour detection
        _, thresh = cv2.threshold(gray, threshold_value, 255, 1)
        close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, close_kernel, iterations=2)

        # Search for contours.
        contours, h = cv2.findContours(
            close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # Filter contours based on number of sides and then reverse sort by area.
        contours = sorted(
            filter(
                lambda cnt: len(
                    cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
                )
                == 4,
                contours,
            ),
            key=cv2.contourArea,
            reverse=True,
        )

        # Calculate the bounding of the first contour and approximate the height
        # and width for final cropping.
        x, y, w, h = cv2.boundingRect(contours[0])
        space_h, space_w = 7 * h // 16, 7 * w // 16

        # Since amongst all the contours, the expected case is that the 4 sided contours
        # containing the characters should have the maximum area, so we loop through the first
        # rows*colums contours and add them to final list after cropping.
        characters = []
        for i in range(rows * cols):
            x, y, w, h = cv2.boundingRect(contours[i])
            cx, cy = x + w // 2, y + h // 2

            roi = image[cy - space_h : cy + space_h, cx - space_w : cx + space_w]
            characters.append([roi, cx, cy])

        # Now we have the characters but since they are all mixed up we need to position them.
        # Sort characters based on 'y' coordinate and group them by number of rows at a time. Then
        # sort each group based on the 'x' coordinate.
        characters.sort(key=lambda x: x[2])
        sorted_characters = []
        for k in range(rows):
            sorted_characters.extend(
                sorted(characters[cols * k : cols * (k + 1)], key=lambda x: x[1])
            )

        return sorted_characters

    def save_images(self, characters, characters_dir):
        """Create directory for each character and save as PNG.

        Creates directory and PNG file for each image as following:

            characters_dir/ord(character)/ord(character).png  (SINGLE SHEET INPUT)
            characters_dir/sheet_filename/ord(character)/ord(character).png  (MULTIPLE SHEETS INPUT)

        Parameters
        ----------
        characters : list of list
            Sorted list of character images each inner list representing a row of images.
        characters_dir : str
            Path to directory to save characters in.
        """
        os.makedirs(characters_dir, exist_ok=True)

        # Create directory for each character and save the png for the characters
        # Structure (single sheet): UserProvidedDir/ord(character)/ord(character).png
        # Structure (multiple sheets): UserProvidedDir/sheet_filename/ord(character)/ord(character).png
        for k, images in enumerate(characters):
            character = os.path.join(characters_dir, str(ALL_CHARS[k]))
            if not os.path.exists(character):
                os.mkdir(character)
            cv2.imwrite(
                os.path.join(character, str(ALL_CHARS[k]) + ".png"),
                images[0],
            )
