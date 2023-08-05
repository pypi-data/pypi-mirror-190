import sys
from dqfit.model import DQIModel

def main(in_dir: str, out_dir: str, context: list) -> None:
    print(sys.argv)
    
    # """Command line utility"""
    model = DQIModel(in_dir, out_dir, context)
    model.fit()
    # # model.index
    model.results.to_json(out_dir, orient='records')

if __name__ == "__main__":
    print("Useage: python -m main.py [in_dir] [out] [context]")
    in_dir = sys.argv[0]
    out_dir = sys.argv[1]
    context = sys.argv[2]
    main("synthea_100.zip", ".",['COLE'])