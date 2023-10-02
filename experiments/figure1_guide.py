BATCHES = [[
        [('ContexDistort', 'layer12'),  ('ContexDistort', 'layer11'),    ('ContexDistort', 'layer10')],
        [('OrderedNeurons', 'seed17'),   ('NeuralPCFG', 'seed3435'),     ('ContexDistort', 'layer10')],
    ],[
        [('OrderedNeurons', 'seed31'),   ('OrderedNeurons', 'seed17'),   ('OrderedNeurons', 'Kim')],
        [('OrderedNeurons', 'seed31'),   ('ContexDistort', 'layer12'),  ('NeuralPCFG', 'seed3435')],
    ],[
        [('CompoundPCFG', 'seed3435'),    ('CompoundPCFG', 'seed1234'),    ('CompoundPCFG', 'Kim')],
        [('CompoundPCFG', 'seed3435'),    ('DIORA', 'Drozdov-MLPsoftmax'), ('S-DIORA', 'seed315')],
    ],[
        [('DIORA', 'Drozdov-MLPsoftmax'),    ('DIORA', 'seed35'),    ('DIORA', 'seed74')],
        [('CompoundPCFG', 'seed3435'),       ('S-DIORA', 'seed75'),  ('DIORA', 'seed74')],
    ],[
        [('S-DIORA', 'seed1943591871'),   ('S-DIORA', 'seed75'),  ('S-DIORA', 'seed315')],
        [('CompoundPCFG', 'seed1234'),    ('S-DIORA', 'seed75'),  ('DIORA', 'seed35')],
    ],[
        [('ConTest', 'id0'),         ('ConTest', 'id2'),        ('ConTest', 'CaoParsed')],
        [('CompoundPCFG', 'Kim'),    ('S-DIORA', 'seed315'),    ('ConTest', 'CaoParsed')],
    ],[
        [('NeuralPCFG', 'seed3435'),     ('NeuralPCFG', 'seed1234'),       ('NeuralPCFG', 'Kim')],
        [('ContexDistort', 'layer11'),  ('OrderedNeurons', 'Kim'),         ('NeuralPCFG', 'Kim')],
  ],
]

MODEL_RENAMING = {
    'OrderedNeurons': 'Ordered Neurons',
    'NeuralPCFG': 'Neural PCFG',
    'CompoundPCFG': 'Compound PCFG',
    'DIORA': 'DIORA',
    'S-DIORA': 'S-DIORA',
    'ConTest': 'ConTest',
    'ContexDistort': 'ContexDistort',
}