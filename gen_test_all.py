
from  first_preprocessing import preprocess
import pathlib
import glob
import re
def gen_all():
    raw_dir = pathlib.Path('htmlData/raw/')
    raw_csv_path = raw_dir.joinpath('*.csv')
    prep_dir = pathlib.Path('htmlData/preprocessed/')
    all_files = glob.glob(raw_csv_path.as_posix())
    for f in all_files:
        preprocess(str(raw_dir),pathlib.Path(f).name)

if __name__ == '__main__':

    gen_all()