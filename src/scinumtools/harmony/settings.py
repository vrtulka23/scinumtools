
HALFTONES = 12

NOTES = {"C":0,"D":2,"E":4,"F":5,"G":7,"A":9,"B":11}

ACCIDENTALS = {
    "b": {
        "name": "flat"
    },
    "#": {
        "name": "sharp"
    }
}

SCALES = {
    "major": {
        "asc":  [0,2,4,5,7,9,11], "desc": [11,9,7,5,4,2,0],
    },
    "natural_minor": {
        "asc":  [0,2,3,5,7,8,10],  "desc": [10,8,7,5,3,2,0],
    },
    "harmonic_minor": {
        "asc":  [0,2,3,5,7,8,11],  "desc": [11,8,7,5,3,2,0],
    },
    "melodic_minor": {
        "asc":  [0,2,3,5,7,9,11], "desc": [10,8,7,5,3,2,0],
    },
}

CHORD_TRIADS = {
    "M": {
        "name": "major",
        "notes": [0,4,7],
    },
    "m": {
        "name": "minor",
        "notes": [0,3,7],
    },
    "+": {
        "name": "augmented",
        "notes": [0,4,8],
    },
    "o": {
        "name": "diminished",
        "notes": [0,3,6],
    },
    "*": {
        "name": "half-diminished",
        "notes": [0,3,6],
    }
}

CHORD_SEVENTHS = {
    "7": {
        "name": "minor seveth",
        "note": 10,
    },
    "M7": {
        "name": "major seventh",
        "note": 11,
    },
}

a="""
Cm{M7}
"""
