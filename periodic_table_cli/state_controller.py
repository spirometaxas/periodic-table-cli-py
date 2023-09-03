class SelectModes:
    ELEMENT = 'element'
    FAMILY  = 'family'
    SHELL   = 'shell'
    SEARCH  = 'search'

class DisplayModes:
    STANDARD          = { 'name': 'standard'                                                       }
    FAMILIES          = { 'name': 'families'                                                       }
    SHELLS            = { 'name': 'shells'                                                         }
    STATES            = { 'name': 'states',            'key': 'standardState'                      }
    ATOMIC_MASS       = { 'name': 'atomicMass',        'key': 'atomicMass',        'isMeter': True }
    PROTONS           = { 'name': 'protons',           'key': 'numberofProtons',   'isMeter': True }
    NEUTRONS          = { 'name': 'neutrons',          'key': 'numberOfNeutrons',  'isMeter': True }
    ELECTRONS         = { 'name': 'electrons',         'key': 'numberofElectrons', 'isMeter': True }
    VALENCE_ELECTRONS = { 'name': 'numberofValence',   'key': 'numberofValence'                    }
    VALENCY           = { 'name': 'valency',           'key': 'valency'                            }
    ATOMIC_RADIUS     = { 'name': 'atomicRadius',      'key': 'atomicRadius',      'isMeter': True }
    DENSITY           = { 'name': 'density',           'key': 'density',           'isMeter': True }
    ELECTRONEGATIVITY = { 'name': 'electronegativity', 'key': 'electronegativity', 'isMeter': True }
    IONIZATION_ENERGY = { 'name': 'ionizationEnergy',  'key': 'ionizationEnergy',  'isMeter': True }
    ELECTRON_AFFINITY = { 'name': 'electronAffinity',  'key': 'electronAffinity',  'isMeter': True }
    MELTING_POINT     = { 'name': 'meltingPoint',      'key': 'meltingPoint',      'isMeter': True }
    BOILING_POINT     = { 'name': 'boilingPoint',      'key': 'boilingPoint',      'isMeter': True }
    SPECIFIC_HEAT     = { 'name': 'specificHeat',      'key': 'specificHeat',      'isMeter': True }
    RADIOACTIVE       = { 'name': 'radioactive',       'key': 'radioactive'                        }
    OCCURRENCE        = { 'name': 'occurrence',        'key': 'occurrence'                         }
    YEAR              = { 'name': 'yearDiscovered',    'key': 'yearDiscovered',    'isMeter': True }

class Layout:

    PeriodicTable = [
        [   1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   2 ],
        [   3,   4,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   5,   6,   7,   8,   9,  10 ],
        [  11,  12,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  13,  14,  15,  16,  17,  18 ],
        [  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29,  30,  31,  32,  33,  34,  35,  36 ],
        [  37,  38,  39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54 ],
        [  55,  56,   0,  72,  73,  74,  75,  76,  77,  78,  79,  80,  81,  82,  83,  84,  85,  86 ],
        [  87,  88,   0, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118 ],
        [   0,   0,  57,  58,  59,  60,  61,  62,  63,  64,  65,  66,  67,  68,  69,  70,  71,   0 ],
        [   0,   0,  89,  90,  91,  92,  93,  94,  95,  96,  97,  98,  99, 100, 101, 102, 103,   0 ],
    ]

    FamiliesTable = [ 
        { 'key': 'Alkali metal', 'index': 0 }, { 'key': 'Alkaline earth metal', 'index': 1 }, { 'key': 'Transition metal', 'index': 2 }, { 'key': 'Post-transition metal', 'index': 3 },
        { 'key': 'Metalloid',    'index': 4 }, { 'key': 'Nonmetal',             'index': 5 }, { 'key': 'Halogen',          'index': 6 }, { 'key': 'Noble gas',             'index': 7 },
        { 'key': 'Lanthanide',   'index': 8 }, { 'key': 'Actinide',             'index': 9 },
    ]

    ShellsTable = [
        { 'key': 's-shell', 'index': 0 }, { 'key': 'p-shell', 'index': 1 }, { 'key': 'd-shell', 'index': 2 }, { 'key': 'f-shell', 'index': 3 },
    ]

    PanelData = [
        { 'key': 'atomicNumber',          'name': 'Atomic Number'     },
        { 'key': 'symbol',                'name': 'Symbol'            },
        { 'key': 'standardState',         'name': 'State'             },
        { 'key': 'atomicMass',            'name': 'Atomic Mass'       },
        { 'key': 'numberofProtons',       'name': 'Protons'           },
        { 'key': 'numberOfNeutrons',      'name': 'Neutrons'          },
        { 'key': 'numberofElectrons',     'name': 'Electrons'         },
        { 'key': 'numberofValence',       'name': 'Valence Electrons' },
        { 'key': 'valency',               'name': 'Valency'           },
        { 'key': 'atomicRadius',          'name': 'Atomic Radius'     },
        { 'key': 'density',               'name': 'Density'           },
        { 'key': 'electronegativity',     'name': 'Electronegativity' },
        { 'key': 'ionizationEnergy',      'name': 'Ionization Energy' },
        { 'key': 'electronAffinity',      'name': 'Electron Affinity' },
        { 'key': 'meltingPoint',          'name': 'Melting Point'     },
        { 'key': 'boilingPoint',          'name': 'Boiling Point'     },
        { 'key': 'specificHeat',          'name': 'Specific Heat'     },
        { 'key': 'radioactive',           'name': 'Radioactive'       },
        { 'key': 'occurrence',            'name': 'Occurrence'        },
        { 'key': 'yearDiscovered',        'name': 'Year'              },
        { 'key': 'electronConfiguration', 'name': 'Electron Config'   },
        { 'key': 'oxidationStates',       'name': 'Oxidation States'  },
    ]

    SearchConfig = {
        'MAX_SEARCH_LENGTH':  36,
        'MAX_SEARCH_RESULTS': 23,
    }