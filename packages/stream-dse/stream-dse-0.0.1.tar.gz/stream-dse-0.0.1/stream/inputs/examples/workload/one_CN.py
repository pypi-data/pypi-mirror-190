workload = {
    23: {  # conv5_3
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 512, 'C': 512, 'OY': 1, 'OX': 7, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': []},
        'constant_operands': ['W', 'I'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'},
        'padding': {'IY': (1, 1), 'IX': (1, 1)}
    },
    24: {  # conv5_3
        'operator_type': 'Conv',
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][iy][ix]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B': 1, 'K': 512, 'C': 512, 'OY': 1, 'OX': 7, 'FY': 3, 'FX': 3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [23]},
        'constant_operands': ['W'],
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'G'}},
        'memory_operand_links': {'O': 'O', 'W': 'I2', 'I': 'I1'},
        'padding': {'IY': (1, 1), 'IX': (1, 1)}
    }
}
