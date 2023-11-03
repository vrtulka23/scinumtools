import numpy as np
import os
import sys
sys.path.insert(0, os.environ['DIR_SOURCE'])

from scinumtools import RowCollector
from scinumtools.units import Dimensions
from scinumtools.units.settings import *
from scinumtools.units.unit_types import *
from scinumtools.dip import DIP
from scinumtools.dip.exports import ExportPDF

path_docs_static = os.environ['DIR_DOCS']+'/source/_static/tables'

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

def build_export_pdf():
    
    # Generate a PDF documentation from a DIP file
    file_definitions = os.environ['DIR_TESTS']+"/dip/examples/pdf_definitions.dip"
    dir_pdf = os.environ['DIR_DOCS']+"/source/_static/pdf"
    file_pdf = f"{dir_pdf}/documentation.pdf"
    # Create directory if missing
    if not os.path.isdir(dir_pdf):
        os.mkdir(dir_pdf)
    # Create a DIP environment
    with DIP(docs=True) as p:
        p.from_file(file_definitions)
        env = p.parse_docs()
    # Export parameters as a PDF
    with ExportPDF(env) as exp:
        title = "Example documentation"
        pageinfo = "DIP Documentation"
        exp.build(file_pdf, title, pageinfo)
    print(file_pdf)

def build_prefixes():
    
    # Create table of unit prefixes
    rc = RowCollector(['Symbol','Name','Magnitude'])
    for symbol, prefix in UNIT_PREFIXES.items():
        exponent = int(np.log10(prefix.magnitude))
        rc.append([symbol, prefix.name, ":math:`10^{"+f"{exponent:d}"+"}`"])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/prefixes.csv"
    df.to_csv(file_path, index=False)
    print(file_path)

def build_base_units():

    # create table of base units
    rc = RowCollector(['Symbol','Name','Prefixes'])
    for symbol, unit in UNIT_STANDARD.items():
        if unit.definition is not None:
            continue
        if unit.prefixes is True:
            prefixes = 'all'
        elif isinstance(unit.prefixes, list):
            prefixes = ", ".join([f"{p}{symbol}" for p in unit.prefixes])
        else:
            prefixes = ''
        rc.append([symbol, unit.name, prefixes])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/unit_base.csv"
    df.to_csv(file_path, index=False)
    print(file_path)
    
def build_standard_units():    

    # create table of standard units
    rc = RowCollector(['Symbol','Name','Definition','Prefixes'])
    for symbol, unit in UNIT_STANDARD.items():
        if not isinstance(unit.definition, str):
            continue
        if symbol in ['K','degR','AR','PR']:
            continue
        if symbol.startswith('['):
            continue
        if unit.prefixes is True:
            prefixes = 'all'
        elif isinstance(unit.prefixes, list):
            prefixes = ", ".join([f"{p}{symbol}" for p in unit.prefixes])
        else:
            prefixes = ''
        if len(rc) and unit.name in rc.Name:
            idx = rc.Name.index(unit.name)
            rc.Symbol[idx] += ", "+symbol
            rc.Prefixes[idx] += ", "+prefixes if rc.Prefixes[idx] else ""
        else:
            rc.append([symbol, unit.name, unit.definition, prefixes])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/unit_standard.csv"
    df.to_csv(file_path, index=False)
    print(file_path)
    
def build_constants():
    
    # create table of constants
    rc = RowCollector(['Symbol','Name','Definition'])
    for symbol, unit in UNIT_STANDARD.items():
        if not symbol.startswith('['):
            continue
        if len(rc) and unit.name in rc.Name:
            idx = rc.Name.index(unit.name)
            rc.Symbol[idx] += ", "+symbol
        else:
            rc.append([symbol, unit.name, unit.definition])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/constants.csv"
    df.to_csv(file_path, index=False)
    print(file_path)
    
def build_logarithmic_units():
    
    # create table of logarithmic units
    rc = RowCollector(['Symbol','Name','Prefixes'])
    for symbol, unit in UNIT_STANDARD.items():
        if symbol not in ['AR','PR'] and unit.definition != LogarithmicUnitType:
            continue
        if unit.prefixes is True:
            prefixes = 'all'
        elif isinstance(unit.prefixes, list):
            prefixes = ", ".join([f"{p}{symbol}" for p in unit.prefixes])
        else:
            prefixes = ''
        if len(rc) and unit.name in rc.Name:
            idx = rc.Name.index(unit.name)
            rc.Symbol[idx] += ", "+symbol
            rc.Prefixes[idx] += ", "+prefixes if rc.Prefixes[idx] else ""
        else:
            rc.append([symbol, unit.name, prefixes])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/unit_logarithmic.csv"
    df.to_csv(file_path, index=False)
    print(file_path)
    
def build_temperature_units():
    
    # create table of temperature units
    rc = RowCollector(['Symbol','Name','Prefixes'])
    for symbol, unit in UNIT_STANDARD.items():
        if symbol not in ['K','degR'] and unit.definition != TemperatureUnitType:
            continue
        if unit.prefixes is True:
            prefixes = 'all'
        elif isinstance(unit.prefixes, list):
            prefixes = ", ".join([f"{p}{symbol}" for p in unit.prefixes])
        else:
            prefixes = ''
        rc.append([symbol, unit.name, prefixes])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/unit_temperature.csv"
    df.to_csv(file_path, index=False)
    print(file_path)
    
def build_si_quantities():

    # create table of physical quantities SI
    rc = RowCollector(['Symbol','Name','Definition','Dimensions'])
    for q in range(len(QUANTITY_LIST)):
        name = QUANTITY_LIST.name[q]
        symbol = QUANTITY_LIST.symbol[q]
        definition = QUANTITY_LIST.SI[q]
        magnitude, dimensions = QUANTITY_UNITS[f"#S{symbol}"]
        rc.append([f"#S{symbol}", f"SI.{name}", definition, dimensions])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/quantities_si.csv"
    df.to_csv(file_path, index=False)
    print(file_path)
    
def build_cgs_quantities():
    
    # create table of physical quantities CGS
    rc = RowCollector(['Symbol','Name','Definition'])
    for q in range(len(QUANTITY_LIST)):
        symbol = QUANTITY_LIST.symbol[q]
        if f"#C{symbol}" not in QUANTITY_UNITS:
            continue
        name = QUANTITY_LIST.name[q]
        definition = QUANTITY_LIST.CGS[q]
        rc.append([f"#C{symbol}", f"CGS.{name}", definition])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/quantities_cgs.csv"
    df.to_csv(file_path, index=False)
    print(file_path)
    
def build_au_quantities():
    
    # create table of physical quantities AU
    rc = RowCollector(['Symbol','Name','Definition'])
    for q in range(len(QUANTITY_LIST)):
        symbol = QUANTITY_LIST.symbol[q]
        if f"#A{symbol}" not in QUANTITY_UNITS:
            continue
        name = QUANTITY_LIST.name[q]
        definition = QUANTITY_LIST.AU[q]
        rc.append([f"#A{symbol}", f"AU.{name}", definition])
    df = rc.to_dataframe()
    file_path = f"{path_docs_static}/quantities_au.csv"
    df.to_csv(file_path, index=False)
    print(file_path)
    
