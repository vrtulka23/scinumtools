from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

class ThumbnailImage:
    """ Create a thumbnail from an image

    :param data: Image data array or a file name string
    :param tuple extent: Extent of an image (xmin, xmax, ymin, ymax)
    :param str mode: Image mode F/RGB/RGBA
    """
    
    extent: list
    im: Image = None
    
    def __init__(self, data, extent=None, mode='F'):
        if isinstance(data, str):
            self.im = Image.open(data).convert(mode)
        else:
            self.im = Image.fromarray(data).convert(mode)
        self.extent = extent if extent else (0,1,0,1)
        self.xratio = np.abs(self.im.size[0]/(self.extent[1]-self.extent[0]))
        self.yratio = np.abs(self.im.size[1]/(self.extent[3]-self.extent[2]))
           
    def crop(self, *extent, bgcolor=0):
        """ Change image extent

        :param extent: New extent of an image can be a tuple (xmin, xmax, ymin, ymax), or 4 floats
        :param bgcolor: Color of the thumbnail padding (float or a tuple)
        """
        if len(extent) in [2,5]:
            bgcolor = extent[-1]
        extent = extent[0] if isinstance(extent[0], tuple) else tuple(extent[:4])
        xpix = int(np.round((extent[1]-extent[0])*self.xratio))
        ypix = int(np.round((extent[3]-extent[2])*self.yratio))
        layer = ThumbnailImage(
            extent = extent,
            data = np.full((ypix,xpix),bgcolor).astype(np.asarray(self.im).dtype),
            mode = self.im.mode,
        )
        pos = [int((layer.im.size[i]-self.im.size[i])/2) for i in range(2)]
        layer.im.paste(self.im, pos)
        self.im = layer.im
        self.extent = extent
        self.xratio = np.abs(self.im.size[0]/(extent[1]-extent[0]))
        self.yratio = np.abs(self.im.size[1]/(extent[3]-extent[2]))
        return self

    def resize(self, *resolution):
        """ Change image resolution
        
        :param resolution: Resolution of a new image an be a tuple (xres, yres), or 2 floats
        """
        resolution = resolution[0] if isinstance(resolution[0],tuple) else tuple(resolution)
        self.im = self.im.resize(resolution)
        return self
        
    def draw(self, ax=None, **kwargs):
        """ Draw current image on an axis

        :param ax: Matplotlib axis
        """
        if not ax: ax=plt
        return ax.imshow(np.asarray(self.im), extent=self.extent, origin='lower', **kwargs)
        
    def save(self, file_name:str, format:str=None):
        """ Save thumbnail as a file
        
        :param str file_name: Name of the image file
        """
        if self.im.mode != 'RGB':
            self.im = self.im.convert('RGB')
        self.im.save(file_name, format=format)
