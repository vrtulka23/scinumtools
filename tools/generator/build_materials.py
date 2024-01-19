import numpy as np
import os, sys
sys.path.insert(0, os.environ['DIR_SOURCE'])
import requests
from bs4 import BeautifulSoup
import json
import re

from scinumtools import ProgressBar, CachedFunction
from scinumtools.units import Quantity

path_materials = os.environ['DIR_SOURCE']+'/scinumtools/materials'

def build_periodic_table():
    
    @CachedFunction(os.environ['DIR_TMP']+'/element.npy')
    def load_elements(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
            
    html_data = load_elements("https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl")
    if html_data:
        
        text = [
            "################################################################",
            "# Do not modify this file!                                     #",
            "# It is generated automatically in:                            #",
            "# tools/generator/build_materials.py                           #",
            "# Isotope data was taken from NIST:                            #",
            "# https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl #",
            "################################################################",
            "",
            "PT_HEADER = ['Z','A']",
            "PT_DATA = {",
        ]
        
        soup = BeautifulSoup(html_data, "html.parser")
        table = soup.find("table")
        rows = table.find_all("tr")
        new = None
        Z, A, M, NA, symbol = 0, 0, 0, 0, None
        for row in rows:
            dts = row.find_all('td',{'align':'right'})
            if len(dts)==1:
                A = int(dts[0].get_text().strip())
                new = False
            elif len(dts)==2:
                Z = int(dts[0].get_text().strip())
                A = int(dts[1].get_text().strip())
                symbol = row.find('td',{'align':'center'}).get_text().strip()
                if new is not None:
                    text.append("    }),")
                text.append("    '"+symbol+"': ("+str(Z)+", {")
                new = True
            else:
                continue
            dts = row.find_all('td',{'align':None})
            # relative atomic masses
            M = float(re.sub(r"(\s+|\([0-9#]+\))", '', dts[0].get_text()))
            # isotopic composition
            if ic := dts[1].get_text().strip():
                NA = float(re.sub(r"(\s+|\([0-9#]+\))", '', ic))
            else:
                NA = 0
            text.append(f"        '{A}': ({M}, {NA}),")
            
        text += [
            "    }),",
            "}", 
        ]
        text = "\n".join(text)
        
        # test if we produced a valid Python code
        exec(text, globals())
        assert PT_HEADER
        assert PT_DATA
        
        print('hello')
        
        # save the new version of the code
        path_units = os.environ['DIR_SOURCE']+"/scinumtools/materials"
        path_list = f'{path_units}/periodic_table.py'
        assert os.path.isdir(path_units)
        with open(path_list,'w') as f:
            f.write(text)
        print(path_list)