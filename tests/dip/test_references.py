import sys, os
import pytest
import numpy as np
sys.path.insert(0, 'src')

from scinumtools.dip import DIP
from scinumtools.dip.settings import Format
from scinumtools.dip.datatypes import FloatType, IntegerType, StringType

def parse(code):
    with DIP() as p:
        p.add_string(code)
        return p.parse().data(verbose=True,format=Format.TYPE)

def test_import_nodes():
    data = parse('''
$source nodes = blocks/nodes.dip
    
{nodes?*}                        # base import
box
  {nodes?*}                      # import into a group node
basket.bag {nodes?*}             # import into a namespace
    ''')
    np.testing.assert_equal(data,{
        'fruits': IntegerType(0),
        'vegies': IntegerType(1),
        'vegies.potato': FloatType(200.0, 'g'),
        'box.fruits': IntegerType(0),
        'box.vegies': IntegerType(1),
        'box.vegies.potato': FloatType(200.0, 'g'),
        'basket.bag.fruits': IntegerType(0),
        'basket.bag.vegies': IntegerType(1),
        'basket.bag.vegies.potato': FloatType(200.0, 'g'),
    })

def test_import_query_remote():
    data = parse('''
$source nodes = blocks/nodes.dip

bag {nodes?*}                # import all
bowl 
  {nodes?fruits}             # selecting a specific node
  {nodes?vegies.potato}      # selecting a specific subnode
plate {nodes?vegies.*}       # selecting all subnodes
    ''')
    np.testing.assert_equal(data,{
        'bag.fruits': IntegerType(0),
        'bag.vegies': IntegerType(1),
        'bag.vegies.potato': FloatType(200.0, 'g'),
        'bowl.fruits': IntegerType(0),
        'bowl.potato': FloatType(200.0, 'g'),
        'plate.potato': FloatType(200.0, 'g'),
    })

def test_source_inject():
    data = parse('''
file str = blocks/nodes.dip
$source nodes = {?file}
{nodes?fruits}              
    ''')
    np.testing.assert_equal(data,{
        'file':   StringType('blocks/nodes.dip'),
        'fruits': IntegerType(0),
    })

def test_source_import_single():
    data = parse('''
$source file = blocks/nodes.dip
$source {file?blocks}
{blocks?energy}              
    ''')
    np.testing.assert_equal(data,{
        'energy': FloatType(13, 'J')
    })
    
def test_source_import_all():
    data = parse('''
$source file = blocks/nodes.dip
$source {file?*}
{blocks?energy}              
    ''')
    np.testing.assert_equal(data,{
        'energy': FloatType(13, 'J')
    })
    
def test_source_import_errors():
    with pytest.raises(Exception) as e_info:
        parse('''
$source file = blocks/nodes.dip
$source {file?books}
        ''')
    assert e_info.value.args[0] == "Requested source does not exists:"
    with pytest.raises(Exception) as e_info:
        parse('''
$source blocks = blocks/nodes.dip
$source {blocks?blocks}
        ''')
    assert e_info.value.args[0] == "Reference source alread exists:"
    
def test_import_query_local():
    data = parse('''
icecream 
  waffle str = 'standard'
  scoops
    strawberry int = 1 #some comment
    chocolate int = 2

bowl
  {?icecream.scoops.*}      # select subnodes from current file
plate {?icecream.waffle}    # select specific node from current file
    ''')
    np.testing.assert_equal(data,{
        'icecream.waffle':            StringType('standard'),
        'icecream.scoops.strawberry': IntegerType(1),
        'icecream.scoops.chocolate':  IntegerType(2),
        'bowl.strawberry':            IntegerType(1),
        'bowl.chocolate':             IntegerType(2),
        'plate.waffle':               StringType('standard'),
    })

def test_injection_local():
    data = parse('''
size1 float = 34 cm       # standard definition
size2 float = {?size1} m  # definition using import with other units
size3 float = {?size2}    # definition using import with same units
size1 = {?size2}          # modifying by import
    ''')
    np.testing.assert_equal(data,{
        'size1': FloatType(3400, 'cm'),
        'size2': FloatType(34, 'm'),
        'size3': FloatType(34, 'm'),
    })

def test_injection_remote():
    data = parse('''
$source query = blocks/query.dip
    
energy float = 34 erg
energy float = {query?energy}  # import with a type
energy = {query?energy} eV     # import value only but set a different unit
energy = {query?energy}        # import both value and unit
    ''')
    np.testing.assert_equal(data,{
        'energy': FloatType(13.0e7, 'erg')     # converted to original units
    })
    with pytest.raises(Exception) as e_info:
        parse('''
        $source query = blocks/query.dip
        
        energy float = {query?*}
        ''')
    assert e_info.value.args[0] == "Path returned invalid number of nodes:"
    assert e_info.value.args[1] == "query?*"

def test_injection_element():
    data = parse('''
sizes float[3] = [34,23.34,1e34] cm      
mysize float[2] = {?sizes}[:2]                # slicing range of values
masses float[2,2] = [[34,23.34],[1,1e34]] cm    
mymass float[2] = {?masses}[:,1]              # slicing multiple range of values
    ''')
    np.testing.assert_equal(data,{
        'sizes': FloatType([3.400e+01, 2.334e+01, 1.000e+34], 'cm'),
        'mysize': FloatType([3.400e+01, 2.334e+01], 'cm'),
        'masses': FloatType([[34,23.34],[1,1e34]], 'cm'),
        'mymass': FloatType([23.34,1e34], 'cm')
    })
    with pytest.raises(Exception) as e_info:
        parse('''
sizes float[3] = [34,23.34,1e34] cm       # standard definition
mysize float = {?sizes}[:2]
        ''')
    assert e_info.value.args[0] == "Array value set to scalar node:"
    
def test_injection_array():
    data = parse('''
$source matrix = blocks/matrix.txt
$source query = blocks/query.dip
    
blocks                                  # block imports into a group node
  matrix1 int[3,4] = {matrix}           # import a text file
  matrix2 int[3,4] = {query?matrix}     # import value of a specific node
  matrix3 float[3,4] = {matrix}         # import a text file
  matrix4 float[3,4] = {query?matrix}   # import value of a specific node
    ''')
    np.testing.assert_equal(data,{
        'blocks.matrix1': IntegerType([[4234,   34,   35,   34],
                                        [ 234,   34,  644,   43],
                                        [ 353, 2356,  234,    3]]),
        'blocks.matrix2': IntegerType([[4234,   34,   35,   34],
                                       [ 234,   34,  644,   43],
                                       [ 353, 2356,  234,    3]]),
        'blocks.matrix3': FloatType([[4234,   34,   35,   34],
                                     [ 234,   34,  644,   43],
                                     [ 353, 2356,  234,    3]]),
        'blocks.matrix4': FloatType([[4234,   34,   35,   34],
                                     [ 234,   34,  644,   43],
                                     [ 353, 2356,  234,    3]]),
    })
    
def test_injection_table():
    data = parse('''
$source table = blocks/table.txt  
$source query = blocks/query.dip
    
blocks                             # block imports into a group node
  table1 table = {table}           # import a text file
  table2 table = {query?table}     # import value of a specific node
    ''')
    np.testing.assert_equal(data,{
        'blocks.table1.x': FloatType([0.234, 1.355, 2.535, 3.255, 4.455], 'm'),
        'blocks.table1.y': FloatType([0.234 , 1.43  , 2.423 , 3.2355, 4.2356], 'm'),
        'blocks.table2.x': FloatType([0.234, 1.355, 2.535, 3.255, 4.455], 'm'),
        'blocks.table2.y': FloatType([0.234 , 1.43  , 2.423 , 3.2355, 4.2356], 'm'),
    })
    
def test_injection_text():
    data = parse('''
$source text = blocks/text.txt
$source query = blocks/query.dip
    
blocks                         # block imports into a group node
  text1 str = {text}           # import a text file
  text2 str = {query?text}     # import value of a specific node
    ''')
    np.testing.assert_equal(data,{
        'blocks.text1': StringType('This is a block text\nwith multiple lines\nthat will be loaded to a\nstring node.\n'),
        'blocks.text2': StringType('This is a block text\nwith multiple lines\nthat will be loaded to a\nstring node.'),
    })

            
if __name__ == "__main__":
    # Specify wich test to run
    test = sys.argv[1] if len(sys.argv)>1 else True

    # Loop through all tests
    for fn in dir(sys.modules[__name__]):
        if fn[:5]=='test_' and (test is True or test==fn[5:]):
            print(f"\nTesting: {fn}\n")
            locals()[fn]()

def test_missing_reference():
    with pytest.raises(Exception) as e_info:
        data = parse('''
        sim
          gravity bool = false  
        @case ("{?gravity}")
          stars int = 30
        @end
        ''')
    assert e_info.value.args[0] == "Missing reference:"
    assert e_info.value.args[1] == "{?gravity}"
  