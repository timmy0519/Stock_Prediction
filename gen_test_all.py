
from  first_preprocessing import preprocess
import pathlib
import glob
import re
import argparse
def gen_all(folder):
    raw_dir = pathlib.Path(folder + '/htmlData/raw/')
    raw_csv_path = raw_dir.joinpath('*.csv')
    prep_dir = pathlib.Path(folder+ '/htmlData/preprocessed/')
    all_files = glob.glob(raw_csv_path.as_posix())
    for f in all_files:
        preprocess(str(raw_dir),pathlib.Path(f).name)

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--folder",
                        type=str,
                        help="train data")

    ARGS = PARSER.parse_args()
    gen_all(ARGS.folder)