import argparse
from experiments.Table1 import table_1
from experiments.Table2 import table_2
from experiments.Table3 import table_3
from experiments.Table4 import table_4
from experiments.Table6 import table_6
from experiments.Figure1 import figure_1
from experiments.Figure2 import figure_2
from experiments.Figure4 import figure_4

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--Table1", action="store_true")
    parser.add_argument("--Table2", action="store_true")
    parser.add_argument("--Table3", action="store_true")
    parser.add_argument("--Table4", action="store_true")
    parser.add_argument("--Table6", action="store_true")
    parser.add_argument("--Figure1", action="store_true")
    parser.add_argument("--Figure2", action="store_true")
    parser.add_argument("--Figure4", action="store_true")
    config = parser.parse_args()
    
    if config.Table1:
        print('Table 1')
        table_1()
        print()
    if config.Table2:
        print('Table 2')
        table_2()
        print()
    if config.Table3:
        print('Table 3')
        table_3()
        print()
    if config.Table4:
        print('Table 4')
        table_4()
        print()
    if config.Table6:
        print('Table 6')
        table_6()
        print()
    if config.Figure1:
        print('Figure 1')
        figure_1()
    if config.Figure2:
        print('Figure 2')
        figure_2()
    if config.Figure4:
        print('Figure 4')
        figure_4()

if __name__ == '__main__':
    main()