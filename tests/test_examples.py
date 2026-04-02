import sys
import os
import pytest
import numpy as np
sys.path.insert(0, 'src')
import subprocess

@pytest.fixture
def test_path():
    return "examples/"

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
    
