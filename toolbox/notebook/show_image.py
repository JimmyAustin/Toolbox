import numpy as np
import matplotlib.pyplot as plt

def show_image(*imgs, **kwargs):
    if len(imgs) > 1:
        img = np.concatenate(tuple([ready_image(x) for x in imgs]), axis=1)
    else:
        img = ready_image(imgs[0])
    fig = plt.figure(figsize=(10,5))
    plt.imshow(img)
    fig.suptitle(kwargs.get('title', ''))

def ready_image(image):
    if image.shape[-1] == 1:
        return np.concatenate((image, image, image), axis=2)
    return image