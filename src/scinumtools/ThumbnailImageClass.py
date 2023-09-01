from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

class ThumbnailImage:
    """ Create a thumbnail from an image

    :param tuple extent: Extent of an image (xmin, xmax, ymin, ymax)
    :param data: Image data
    """
    
    extent: list
    im: Image = None
    
    def __init__(self, extent, data, mode='F'):
        self.im = Image.fromarray(data).convert(mode)
        self.extent = extent
        self.xratio = np.abs((extent[1]-extent[0])/self.im.size[0])
        self.yratio = np.abs((extent[3]-extent[2])/self.im.size[1])
                
    def resize(self, extent=None, res=None, bgcolor=0):
        """ Resize image

        :param tuple extent: New extent of an image (xmin, xmax, ymin, ymax)
        :param tuple res: Resolution of a new image
        :param bgcolor: Color of the thumbnail padding (loat or a tuple)
        """
        if extent:
            xpix = int(np.round((extent[1]-extent[0])/self.xratio))
            ypix = int(np.round((extent[3]-extent[2])/self.yratio))
            layer = ThumbnailImage(
                extent = extent,
                data = np.full((ypix,xpix),bgcolor).astype(np.asarray(self.im).dtype),
                mode = self.im.mode,
            )
            pos = [int((layer.im.size[i]-self.im.size[i])/2) for i in range(2)]
            layer.im.paste(self.im, pos)
        if res and extent:
            layer.im = layer.im.resize(res)
            return layer
        else:
            self.im = self.im.resize(res)
            return self
        
    def draw(self, ax=None, **kwargs):
        """ Draw current image on an axis

        :param ax: Matplotlib axis
        """
        if not ax: ax=plt
        return ax.imshow(np.asarray(self.im), extent=self.extent, origin='lower', **kwargs)
