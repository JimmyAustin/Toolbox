import numpy as np
from scipy.ndimage.measurements import label
try:
    import cv2
    cv2_enabled = True
except ImportError:
    cv2_enabled = False

class BoundingBox():
    def __init__(self, x=None, y=None, width=None, height=None, 
                 min_x=None, min_y=None, max_x=None, max_y=None):
        self.x = x or min_x
        self.y = y or min_y
        self.width = width or max_x - self.x
        self.height = height or max_y - self.y
        self.min_x = self.x
        self.max_x = self.x + self.width
        self.min_y = self.y
        self.max_y = self.y + self.height

    def area(self):
        return (self.width * self.height)

    def aspect_ratio(self):
        return self.width / self.height

    def draw_on_image(self, image, title=None, color=(255, 255, 255), thickness=6):
        if cv2_enabled is False:
            return
        try:
            cv2.rectangle(image, (self.x, self.y), (self.max_x, self.max_y), color, thickness)
        except ValueError:
            pass
        if title is not None:
            font                   = cv2.FONT_HERSHEY_SIMPLEX
            fontScale              = 0.75
            fontColor              = (0,0,255)
            lineType               = 2
            try:
                cv2.putText(image, str(title), 
                        (self.x, self.y-thickness), 
                        font, 
                        fontScale,
                        fontColor,
                        lineType)
            except ValueError:
                pass

    def merge(self, other_bbox):
        return BoundingBox(min_x=min(self.min_x, other_bbox.min_x),
                           max_x=min(self.max_x, other_bbox.max_x),
                           min_y=min(self.min_y, other_bbox.min_y),
                           max_y=min(self.max_y, other_bbox.max_y))

    def __repr__(self):
        return "<BoundingBox - X:{0}, Y:{1}, W:{2}, H:{3}>".format(self.x,\
                self.y, self.max_x, self.max_y)

def apply_threshold(image, threshold, replacement_value=0):
    image[image <= threshold] = replacement_value
    return image

def get_image_in_bounding_box(super_image, bbox):
    return super_image[bbox.min_y: bbox.max_y, bbox.min_x: bbox.max_x]

def find_contiguous_sections(image, minimum_area=100):
      
    labels, number_of_sections = label(image)

    results = []

    for section_number in range(1, number_of_sections+1):
        result = _handle_section(labels, section_number, minimum_area)
        if result is not None:
            results.append(result)

    return results

def _handle_section(labels, section_number, minimum_area):
    bounding_box = generate_bounding_box(labels, section_number)
    if bounding_box.area() < minimum_area:
        return
    return bounding_box

def generate_bounding_box(labels, section_number, minimum_area=100):
    nonzero = (labels == section_number).nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])

    return BoundingBox(min_x=np.min(nonzerox), min_y=np.min(nonzeroy), 
                       max_x=np.max(nonzerox), max_y=np.max(nonzeroy))
