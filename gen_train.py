# coding: utf-8

import pandas as pd
import matplotlib as plt
import pathlib
import fastai
import pathlib
import argparse

def gen_train(x,y,targetBool=False):
    folder_path = pathlib.Path('htmlData/preprocessed')
    filename = x
    file_path = folder_path.joinpath(filename)
    data = pd.read_csv(file_path)

    gspc_folder = pathlib.Path('./streamData/filtered')
    gspc_data =  pd.read_csv(gspc_folder.joinpath(filename))

    numeric_features = data.select_dtypes('number').columns
    id_feature = ['Stock_code']
    cat_features = data.select_dtypes(exclude = 'number').columns.drop(['Stock_code'])

    n_filename = y
    n_file_path = folder_path.joinpath(n_filename)
    n_data = pd.read_csv(n_file_path)

    n_gspc_path = gspc_folder.joinpath(n_filename)
    n_gspc_data =  pd.read_csv(n_gspc_path)

    gspc_change_percentage = (n_gspc_data.iloc[0]['PRICE'] - gspc_data.iloc[0]['PRICE']) / gspc_data.iloc[0]['PRICE'] * 100

    # merged_data = pd.merge(left=data,right=n_data.loc[:,['Stock_code','current price']],how='left',left_on='Stock_code',right_on='Stock_code')
    merged_data = pd.merge(left=data,right=n_data.loc[:,['Stock_code','current_price','sp_average_change']],how='left',left_on='Stock_code',right_on='Stock_code')
## predict actual price change
    # target_var = 'price_change'
    # merged_data[target_var] = merged_data['current price_y'] - merged_data['current price_x']

    # merged_data = merged_data.drop('current price_y',axis=1,errors='ignore')
    # merged_data.rename({'current price_x': 'current_price'},axis=1,inplace=True)

    # merged_data[target_var] = merged_data[target_var].fillna(-merged_data['current_price'])

    # target_var = 'trend'
    # merged_data[target_var] = (merged_data['current price_y'] - merged_data['current price_x'])>0

    # merged_data = merged_data.drop('current price_y',axis=1,errors='ignore')
    # merged_data.rename({'current price_x': 'current_price'},axis=1,inplace=True)

    # merged_data[target_var] = merged_data[target_var].fillna(False)

    target_var = 'trend_sp'
    merged_data['price_change_percentage'] = (merged_data['current_price_y'] - merged_data['current_price_x']) /  merged_data['current_price_x'] *100.
    # merged_data['trend_sp'] = (merged_data['price_change_percentage'] > merged_data['sp_average_change_y']) & (merged_data['sp_average_change_y']>0)
    if targetBool:
        merged_data['trend_sp'] = ((merged_data['price_change_percentage'] > (gspc_change_percentage)) & (merged_data['price_change_percentage']>0))
    else:
        merged_data['trend_sp'] = merged_data['price_change_percentage'] - (gspc_change_percentage)
        merged_data['trend_sp'] = merged_data['trend_sp'].round(2)
    merged_data = merged_data.drop(['current_price_y','sp_average_change_y','sp_average_change_x','price_change_percentage'],axis=1,errors='ignore')
    merged_data.rename({'current_price_x': 'current_price'},axis=1,inplace=True)

    if not target_var:
        merged_data[target_var] = merged_data[target_var].fillna(False)
    else:
        # merged_data[target_var] = merged_data[target_var].fillna(-100.)
        merged_data.dropna(axis=0,subset=[target_var],inplace=True)
    merged_data = merged_data[merged_data.current_price > merged_data.current_price.quantile(0.1)]

    target_folder = pathlib.Path('./').joinpath('train')
    if not target_folder.exists():
        target_folder.mkdir()
    file_path = target_folder.joinpath(filename)

    merged_data.to_csv(file_path.as_posix(),index=False)



if __name__ == '__main__':
    # create parser and handle arguments
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("-x",
                        type=str,
                        help="train data")
    PARSER.add_argument("-y",
                        type=str,
                        help="the next month of the train data")
    # parse the arguments
    ARGS = PARSER.parse_args()
    gen_train(ARGS.x,ARGS.y)