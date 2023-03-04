from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from extensions.element_visitor import ElementVisitor
import cv2
import numpy as np
import logging


class ImageContrastChecker(ElementVisitor):

    def visit_img(self, element, *args, **kwargs):
        if not element.get('src'):
            logging.info("[WCAG 2.1 - 1.4.3 Contrast (Minimum)] Found an image with no src attribute")
            return
        
        try:
            img = cv2.imread('src\\extensions\\badcontrast.png')
        except:
            logging.info("[WCAG 2.1 - 1.4.3 Contrast (Minimum)] Image %s not found" % element.get('src'))
            return

        if img is None:
            logging.info("[WCAG 2.1 - 1.4.3 Contrast (Minimum)] No image found. Check the path for %s" % element.get('src'))
            return
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # compute contrast
        contrast = img_grey.std()
        logging.info("[WCAG 2.1 - 1.4.3 Contrast (Minimum)] - Estimated contrast of the image(%s) is %s" % (element.get('src'), contrast))
   

class ImageContrastCheckProcessor(Treeprocessor):
    def run(self, root):
        ImageContrastChecker().visit(root)


class ImageContrastExtension(Extension):
    def extendMarkdown(self, md):        
        md.treeprocessors.register(ImageContrastCheckProcessor(md), 'imagecontrasttcheckprocessor', 1)


