
from  first_preprocessing import preprocess
import pathlib
import glob
import re
def gen_all():
    raw_dir = pathlib.Path('htmlData/raw/')
    raw_csv_path = raw_dir.joinpath('*.csv')
    prep_dir = pathlib.Path('htmlData/preprocessed/')