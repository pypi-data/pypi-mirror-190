from sympy.functions import *
from wiggles.symbols import *
import numpy as np
import sympy.core.numbers as symnum
import sympy.functions as symfun
import pickle

#Exports Wiggles type signal to a file
def export_wiggles(wiggles_obj, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(wiggles_obj, f)

#Imports Wiggles type signal from a file
def import_wiggles(file_path):
    with open(file_path, 'rb') as f:
        wiggles_obj = pickle.load(f)
    return wiggles_obj

def unit_step(n):
    return Heaviside(n)

def unit_impulse(n, sympy_repr = 1):
    out = DiracDelta(n)

    if(sympy_repr==0):
        if type(out) in [symnum.Infinity,symnum.ComplexInfinity,symnum.NegativeInfinity]:
                    out = np.inf
        elif out == symfun.DiracDelta(0):
                    out = 1
        try:
            out = float(out)
        except:
            out = np.nan
    
    return out

def exp(n):
    return exp(n)

def sin(n):
    return symfun.sin(n)

def cos(n):
    return symfun.cos(n)