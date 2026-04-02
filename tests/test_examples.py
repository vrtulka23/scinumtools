import sys
import os
import pytest
import numpy as np
sys.path.insert(0, 'src')
import subprocess

@pytest.fixture
def test_path():
    return "examples"

def test_examples_n_body(test_path):

    # set path to the example
    dirTest = f"{test_path}/n_body"

    # run example
    result = subprocess.run([
        "python3", "main.py", "--pytest"
    ],capture_output=True, text=True, cwd=dirTest)

    # test the last trajectory    
    assert result.stdout=="[-12.71853804  -1.20024228]\n"

def test_examples_elmag_force(test_path):

    # set path to the example
    dirTest = f"{test_path}/elmag_force"

    # run example
    result = subprocess.run([
        "python3", "simulation.py", "--init", "--docs"
    ],capture_output=True, text=True, cwd=dirTest)

    # check if files were created
    assert os.path.isfile(f"{dirTest}/config.h")
    assert os.path.isfile(f"{dirTest}/documentation.pdf")

def test_examples_dip_example(test_path):

    # set path to the example
    dirTest = f"{test_path}/dip_example"

    # run example
    result = subprocess.run([
        "python3", "main.py"
    ],capture_output=True, text=True, cwd=dirTest)

    # test the output
    assert result.stdout == "Number of spheres: Quantity(2.450e+02)\nTotal mass:        Quantity(1.275e+01 kg)\n"
