import numpy as np
import os
import sys
sys.path.insert(0, os.environ['DIR_SOURCE'])
import requests
from bs4 import BeautifulSoup
import json
import re

from scinumtools import ProgressBar, CachedFunction
from scinumtools.units import Quantity

path_materials = os.environ['DIR_SOURCE']+'/scinumtools/materials'

def build_elements():
    
    unit_density = 'g/cm3'

    columns = [
        ('Symbol',        'symbol',   str,   8,  r"'{value}': ", ''      ),
        ('Atomic Number', 'Z',        int,   7,  r"{value},",    ''      ),
        ('Atomic Weight', 'A',        int,   7,  r"{value},",    ''      ),
        ('Name',          'name',     str,   20, r"'{value}', ", ''      ),
    ]

    isotope_data = [
        (r'Weight',   'Ar',        float, 16,  r"{value},", 'Da'   ),
        ('Abundance', 'abundance', float, 10,  r"{value},", '%'    ),
        ('Binding',   'E_bind',    float, 10,  r"{value},", 'MeV'  ),
    ]
    
    def dformat_rho(table):
        # find isotope ID
        row = table.find(lambda tag: tag.name=='tr' and 'Atomic Weight' in tag.text)
        value = row.find('td').find_next('td').text
        value = value.replace('[note]','')
        isotope = int(np.round(float(value)))
        # find density
        row = table.find(lambda tag: tag.name=='tr' and 'Density' in tag.text)
        value = row.find('td').find_next('td').text
        value = value.replace('[note]','')
        if value in ['N/A']:
            return isotope, None
        else:
            mag, unit = value.split(" ")
            density = Quantity(float(mag), unit).value(unit_density)
            return isotope, density

    @CachedFunction(os.environ['DIR_TMP']+'/isotopes.npy')
    def load_isotopes(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
            
    @CachedFunction(os.environ['DIR_TMP']+'/element.npy')
    def load_elements(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
            
    def get_isotopes(id_element, id_isotope, density=None):
        url = f"https://periodictable.com/Isotopes/{id_element:03d}.{id_isotope:d}/index.html"
        html_data = load_isotopes(url)
        if html_data:
            soup = BeautifulSoup(html_data, "html.parser")
            table = soup.find(lambda tag: tag.name == 'font' and 'Abundance' in tag.text).find_parent('table')
            values = {}
            for label, name, dtype, length, dformat, unit in isotope_data:
                row = table.find(lambda tag: tag.name=='tr' and label in tag.text)
                value = row.find('td').find_next('td').text
                if value in ['None', 'N/A']:
                    value = 'None,'
                    values[name] = rf"{value:{length}s}"
                    continue
                value = str(dtype(value.replace('%','').replace('×10','e').replace('MeV','')))  
                value = dformat.format(value=value) if isinstance(dformat,str) else dformat(value, unit)
                value = rf"{value:{length}s}"
                values[name] = value
            #if 'None' in values['abundance'] and density is None:
            #    return None
            symbol = f"'{id_isotope:d}':"
            values['N']   = r"{value:5s}".format(value=f"{id_isotope-id_element:d},")
            values['rho'] = r"{value:16s}".format(value=f"{density:.04e}," if density else "None,")
            properties = " ".join(values.values())
            text = f"  {symbol:7s}({properties}),"
        else:
            raise Exception('Isotope information could not be downloaded', id_element, id_isotope)
        return text

    def get_element(id_element):
        url = f"https://periodictable.com/Elements/{id_element:03d}/data.html"
        html_data = load_elements(url)
        if html_data:
            soup = BeautifulSoup(html_data, "html.parser")
            
            # find element information
            table = soup.find(lambda tag: tag.name == 'a' and 'Atomic Number' in tag.text).find_parent('table')
            values = {}
            for label, name, dtype, length, dformat, unit in columns:
                row = table.find(lambda tag: tag.name=='tr' and label in tag.text)
                value = row.find('td').find_next('td').text
                if value=='N/A':
                    value = 'None,'
                    values[name] = rf"{value:{length}s}"
                    continue
                value = str(dtype(value.replace('[note]','')))
                value = dformat.format(value=value) if isinstance(dformat,str) else dformat(value, unit)
                value = rf"{value:{length}s}"
                values[name] = value
            symbol = values['symbol']
            del values['symbol']
            properties = " ".join(values.values())
            
            isotope, density = dformat_rho(table)

            # find isotopes
            isotopes = soup.find(lambda tag: tag.name == 'a' and 'Known Isotopes' in tag.text).find_parent('td').find_next('td').find_all('a')
            id_isotopes = [int(re.match(".*[0-9]{3}\.([0-9]+).*",iso.get('href')).group(1)) for iso in isotopes]
            text_isotopes = []
            for id_isotope in id_isotopes:
                rho = density if id_isotope == isotope else None
                text_isotope = get_isotopes(id_element, id_isotope, rho)
                if text_isotope is not None:
                    text_isotopes.append( text_isotope )
            text_isotopes = "\n".join(text_isotopes)

            # create text
            if text_isotopes:
                text = f"{symbol:7s}({properties}"+"{"+f"\n{text_isotopes}"+"\n}),"
            else: 
                text = f"{symbol:7s}({properties} None),"
            return text
        else:
            raise Exception('Element information could not be downloaded', id_element)
      
    element_columns = {column[1]:column[5] for column in columns[1:]}
    element_columns['isotopes'] = ''
    element_columns = json.dumps(element_columns)
    
    isotope_columns = {column[1]:column[5] for column in isotope_data}
    isotope_columns['N'] = ''
    isotope_columns['Density'] = unit_density
    isotope_columns = json.dumps(isotope_columns)
      
    text = [
        "#############################################",
        "# Do not modify this file!                  #",
        "# It is generated automatically in:         #",
        "# tools/generator/build_materials.py.       #",
        "#############################################",
        ""
        "NUCLEON_COLUMNS = {'Z': '', 'N': '', 'E': '', 'A': 'Da', 'name': ''}",
        "NUCLEONS = {",
        "'[e]':   (0, 0, 1, 5.48579909065e-4, 'Electron',  ),",
        "'[n]':   (0, 1, 0, 1.00866491588,    'Neutron',   ),",
        "'[p]':   (1, 0, 0, 1.007276466621,   'Proton',    ),",
        "}",
        f"ELEMENT_COLUMNS = {element_columns}",
        f"ISOTOPE_COLUMNS = {isotope_columns}",
        "ELEMENTS = {",
    ]
      
    num_elements = 118
    for i in range(num_elements):
        text.append(get_element(i+1))
        #break

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
