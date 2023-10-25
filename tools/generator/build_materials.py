import numpy as np
import os
import sys
sys.path.insert(0, os.environ['DIR_SOURCE'])
import requests
from bs4 import BeautifulSoup

from scinumtools import ProgressBar, CachedFunction

path_materials = os.environ['DIR_SOURCE']+'/scinumtools/materials'

def build_elements():
    
    text = [
        "#############################################",
        "# Do not modify this file!                  #",
        "# It is generated automatically in:         #",
        "# tools/generator/build_materials.py.       #",
        "#############################################",
        ""
        "ELEMENTS = {",
    ]

    columns = [
        ('Name',          'name',   str),
        ('Symbol',        'symbol', str),
        ('Atomic Number', 'Z',      int),
        ('Atomic Weight', 'A',      float),
        ('Density',       'rho',    str)
    ]

    @CachedFunction()
    def load_data(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def get_element(idx):
        CachedFunction()
        url = f"https://periodictable.com/Elements/{idx:03d}/data.html"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find(lambda tag: tag.name == 'a' and 'Atomic Number' in tag.text).find_parent('table')
            values = {}
            for label, name, dtype in columns:
                row = table.find(lambda tag: tag.name=='tr' and label in tag.text)
                value = row.find('td').find_next('td').text
                value = value.replace('[note]','')
                values[name] = dtype(value)
            properties = []
            properties.append(f"{values['Z']}")
            properties.append(f"{values['A']}")
            properties.append(f"'{values['name']}'")
            properties = ", ".join(properties)
            symbol = f"'{values['symbol']}': "
            return f"{symbol:7s}({properties}),"
        else:
            raise Exception('Element information could not be downloaded', idx)
            
    num_elements = 118
    with ProgressBar(num_elements) as pb:
        for i in range(num_elements):
            text.append(get_element(i+1))
            pb.step()

    text.append("}")
    text = "\n".join(text)
    
    # test if we produced a valid Python code
    exec(text, globals())
    assert ELEMENTS
    
    # save the new version of the code
    path_units = os.environ['DIR_SOURCE']+"/scinumtools/materials"
    path_list = f'{path_units}/list_elements.py'
    assert os.path.isdir(path_units)
    with open(path_list,'w') as f:
        f.write(text)
    print(path_list)
