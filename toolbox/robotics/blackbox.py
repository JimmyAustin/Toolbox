from datetime import datetime
import os
import shutil
from scipy.misc import imsave
try:
    import cv2
    cv2_enabled = True
except ImportError:
    cv2_enabled = False
    pass
import scipy
import numpy as np

class Blackbox:
    def __new__(cls, *args, **kwargs):
        if kwargs.get('disabled', False):
            return DummyBlackBox()
        del kwargs['disabled']
        return Blackbox(*args, **kwargs)

    def __init__(self, image_size=(480, 640), feeds=[], folder=None):
        print('blackbox start')
        self.image_size = image_size
        self.feeds=feeds
        self.folder=folder or './last_run'#'./' + datetime.now().isoformat()
        if os.path.exists(self.folder):
            shutil.rmtree(self.folder)
        os.makedirs(self.folder)
        self.current_images = {feed: self.ready_image(None, title=feed) for feed in feeds}
        self.debug_information = {}

    def add_image(self, feed, image, debug_information={}):
        self.current_images[feed] = self.ready_image(image, title=feed)
        self.debug_information.update(debug_information)
        #self.save_image()

    def save_image(self):        
        self.debug_information['current_time'] = datetime.now().isoformat()

        image = self.build_image()
        imsave(self.folder + '/' + datetime.now().strftime("%H:%M:%S_%f") + '.jpg', image)

    def build_image(self):
        images = [self.current_images[x] for x in self.feeds]

        image = np.concatenate(tuple(images), axis=1)
        add_text(image, str(self.debug_information), (2,self.image_size[0]-2))
        return image

    def ready_image(self, image, title=''):
        correct_image_shape = (self.image_size[0], self.image_size[1], 3)
        if image is None:
            return np.zeros(correct_image_shape)
        if image.shape == correct_image_shape:
            return image
        if len(image.shape) == 2 or len(image.shape) == 3 and image.shape[-1] == 1:
            image = np.resize(image, (image.shape[0], image.shape[1], 1))
            image = np.concatenate((image, image, image), axis=2)
        image = scipy.misc.imresize(image, self.image_size)
        add_text(image, title, (10, 10))
        return image

    def make_movie(self):
        raise Exception('Unimplemented')
        pass

def add_text(image, text, bottom_left_corner_of_text):
    if cv2_enabled is False:
        return
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    fontScale              = 0.75
    fontColor              = (255,255,255)
    lineType               = 2

    cv2.putText(image, text, 
            bottom_left_corner_of_text, 
            font, 
            fontScale,
            fontColor,
            lineType)
    return image

class DummyObject:
    def nop(*args, **kw): pass
    def __getattr__(self, _): return self.nop
