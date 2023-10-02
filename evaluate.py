from KimEval import sentence_level_f1
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", required=True)
    parser.add_argument("--pred", required=True)
    config = parser.parse_args()

    f1 = sentence_level_f1(
        ref=open(config.ref).readlines(),
        pred=open(config.pred).readlines(),
    )
    print(f"Average sentence level F1: {f1}")

    
if __name__ == '__main__':
    main()