from extractGSPC import extract
import pathlib
import glob
import re

def extract_all():
    streamFolder = pathlib.Path('./streamData')
    raw_tsv_path = streamFolder.joinpath('*.tsv')

    years = [y.split('/')[1] for y in glob.glob(str(streamFolder)+'/*')  if re.search(r'[0-9]{4}$',y)] 
    y_m = {}
    for y in years:
        for m in glob.glob(str(streamFolder.joinpath(y))+'/*'):
            if not re.search('[0-9]{2}',m):
                continue
            else:
                if y not in y_m:
                    y_m[y] = []
                y_m[y].append(m.split('/')[-1])
            
    for y, ms in y_m.items():
        for m in ms:
            print(y,m)
            extract(y, m)
            
    
if __name__ == '__main__':
    extract_all()