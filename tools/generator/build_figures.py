import numpy as np
import os
import sys
sys.path.insert(0, os.environ['DIR_SOURCE'])

def build_thumbnail_image():
    
    from scinumtools import ThumbnailImage
    import matplotlib.pyplot as plt
    import numpy as np
    
    size = np.pi
    size1 = (100, 100)
    xaxis = np.linspace(-size, size, size1[0])
    yaxis = np.linspace(-size, size, size1[1])
    data = size*np.vectorize(lambda x,y: np.sin(x)*np.sin(y))(*np.meshgrid(xaxis,yaxis))
    extent1 = (xaxis.min(), xaxis.max(), yaxis.min(), yaxis.max())

    fig, axes = plt.subplots(2,2,figsize=(5,5),tight_layout=True)
    
    ticks1 = [-size,0,size]
    ticks2 = [-size*2,-size,0,size,size*2]
    labels1 = ['$-\pi$','0','$\pi$']
    labels2 = ['$-2\pi$','$-\pi$','0','$\pi$','$2\pi$']
    extent2 = (-size*2, size*2, -size*2, size*2)
    size2 = (20,20)
    plots = [
        ('a.', 0, 0, ticks1, labels1, ThumbnailImage(data, extent1, mode='F') ),
        ('b.', 1, 0, ticks1, labels1, ThumbnailImage(data, extent1).resize(size2) ),
        ('c.', 0, 1, ticks2, labels2, ThumbnailImage(data, extent1).crop(extent2) ),
        ('d.', 1, 1, ticks2, labels2, ThumbnailImage(data, extent1).crop(extent2, bgcolor=2).resize(size2) ),
    ]
    for name, m, n, ticks, labels, ti in plots:
        ax = axes[m,n]
        ti.draw(ax)
        ax.text(0.05, 0.9, name, transform=ax.transAxes)
        ax.text(0.05, 0.05, ti.im.size, transform=ax.transAxes)
        ax.set_xticks(ticks)
        ax.set_xticklabels(labels)
        ax.set_yticks(ticks)
        ax.set_yticklabels(labels)

    dir_figures = os.environ['DIR_DOCS']+"/source/_static/figures"
    file_figure = dir_figures+"/thumbnail_image.png"
    plt.savefig(file_figure)
    print(file_figure)

def build_normalize_data():
    
    from scinumtools import NormalizeData
    import matplotlib.pyplot as plt
    import numpy as np
    
    with NormalizeData(xaxis='lin', yaxis='lin') as nd:
        
        for size in [np.pi*2, np.pi]:
            xaxis = np.linspace(0,size,50)
            yaxis = np.linspace(-size,size,50)
            zdata = size*np.vectorize(lambda x,y: np.sin(x)*np.sin(y))(*np.meshgrid(xaxis,yaxis))
            nd.append(zdata, xaxis, yaxis)
        
        xranges = nd.xranges()
        yranges = nd.yranges()
        norm = nd.linnorm()
    
        fig, axes = plt.subplots(1,2,figsize=(5,3))
    
        for i, (data, extent) in enumerate(nd.items()):
            ax = axes[i]
            im = ax.imshow(data, extent=extent, norm=norm)
            ax.set_xlim(xranges.min, xranges.max)
            ax.set_ylim(yranges.min, yranges.max)
        
        fig.colorbar(im, ax=axes.ravel().tolist())
        
        dir_figures = os.environ['DIR_DOCS']+"/source/_static/figures"
        file_figure = dir_figures+"/normalize_data.png"
        plt.savefig(file_figure)
        print(file_figure)
    
def build_data_plot_grid():
    
    from scinumtools import DataPlotGrid
    import matplotlib.pyplot as plt
    
    dpg = DataPlotGrid(['a','b','c','d','e'],ncols=3,axsize=(1,1))
    
    fig, axes = plt.subplots(dpg.nrows, dpg.ncols, figsize=dpg.figsize, tight_layout=True)
    for i, m, n, v in dpg.items():
        ax = axes[m,n]
        ax.text(0.5, 0.5, v)
    for i, m, n in dpg.items(missing=True):
        ax = axes[m,n]
        ax.set_axis_off()
    dir_figures = os.environ['DIR_DOCS']+"/source/_static/figures"
    file_figure = dir_figures+"/data_plot_grid1.png"
    plt.savefig(file_figure)
    print(file_figure)
    
    fig.clf()
    
    fig, axes = plt.subplots(dpg.nrows, dpg.ncols, figsize=dpg.figsize, tight_layout=True)
    for i, m, n, v in dpg.items(transpose=True):
        ax = axes[m,n]
        ax.text(0.5, 0.5, v)
    for i, m, n in dpg.items(transpose=True, missing=True):
        ax = axes[m,n]
        ax.set_axis_off()
        
    dir_figures = os.environ['DIR_DOCS']+"/source/_static/figures"
    file_figure = dir_figures+"/data_plot_grid2.png"
    plt.savefig(file_figure)
    print(file_figure)
