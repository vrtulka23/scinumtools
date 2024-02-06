from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from typing import Union

class ThumbnailImage:
    """ Create a thumbnail from an image

    :param data: Image data array or a file name string
    :param tuple extent: Extent of an image (xmin, xmax, ymin, ymax)
    :param str mode: Image mode F/RGB/RGBA
    """
    
    extent: list
    im: Image = None
    
    def __init__(self, data, extent:list=None, mode=None):
        if isinstance(data, str):
            if mode is None: mode = 'RGB'
            self.im = Image.open(data).convert(mode)
        else:
            if mode is None: mode = 'F'
            self.im = Image.fromarray(data).convert(mode)
        self.extent = list(extent if extent else [0,1,0,self.im.size[1]/self.im.size[0]])
        self.xratio = np.abs(self.im.size[0]/(self.extent[1]-self.extent[0]))
        self.yratio = np.abs(self.im.size[1]/(self.extent[3]-self.extent[2]))
           
    def crop(self, left:Union[float,tuple], right:float=None, bottom:float=None, top:float=None, bgcolor=0):
        """ Change image extent

        :param left: Tuple with an image extent, or left extent
        :param float right: Right extent
        :param float bottom: Bottom extent
        :param float top: Top extent
        :param bgcolor: Color of the thumbnail padding (float or a tuple)
        """
        if isinstance(left, (list,tuple)) and right is None and bottom is None and top is None:
            extent = left  
        elif left is None and right is None and bottom is None and top is None:
            raise Exception("This function requires at least one extent:", left, right, botom, top)
        else:
            extent = list(self.extent)
            if left is not None:   extent[0] = left
            if right is not None:  extent[1] = right
            if bottom is not None: extent[2] = bottom
            if top is not None:    extent[3] = top
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
        self.extent = list(extent)
        self.xratio = np.abs(self.im.size[0]/(extent[1]-extent[0]))
        self.yratio = np.abs(self.im.size[1]/(extent[3]-extent[2]))
        return self

    def resize(self, xres:int = None, yres:int = None):
        """ Change image resolution
        
        :param int xres: Resolution on the X-axis
        :param int yres: Resolution on the Y-axis
        """
        if isinstance(xres, tuple):
            resolution = xres
        elif xres is None and yres is None:
            raise Exception("At least one resolution has to be set:", xres, yres)
        else:
            resolution = list(self.im.size)
            if xres is not None: resolution[0] = xres
            if yres is not None: resolution[1] = yres
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
