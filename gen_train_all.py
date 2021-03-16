
from  first_preprocessing import preprocess
from gen_train import  gen_train
import  extractGSPC_all
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
    extractGSPC_all.extract_all()
    year_month_dict = {}
    for f in all_files:
        y_m = re.search("([0-9]{4})\-([0-9]{2})(?=\.csv)", f)
        y,m = y_m.group(1),y_m.group(2)

        if y not in year_month_dict:
            year_month_dict[y] = set()
        
        year_month_dict[y].add(m)
    for y,m_list in year_month_dict.items():
        n_y = str(int(y)+1)
        print(n_y)
        for m in m_list:
            n_m = str(int(m)+1)
            # print(n_m)
            if n_m in m_list:
                cur_filename = y + '-' + m + '.csv'
                n_filename = y + '-' + n_m + '.csv'
                
                gen_train(cur_filename,n_filename)
            elif  m=='12' and n_y in year_month_dict and '1' in year_month_dict[n_y]:
                cur_file_path = prep_dir.joinpath( y + '-' + m + '.csv').as_posix()
                n_file_path = prep_dir.joinpath( n_y + '-' + '1' + '.csv').as_posix()
                gen_train(cur_file_path,cur_file_path) 
if __name__ == '__main__':

    gen_all()