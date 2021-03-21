import argparse
import pandas as pd
import matplotlib as plt
import pathlib
import numpy as np
import pathlib 
from sklearn.impute import SimpleImputer
def preprocess(pathname, filename):
    pathname = pathname 
    filename = filename
    data = pd.read_csv(pathlib.Path(pathname,filename))
    data.columns = data.columns.str.split().str.join('_')
    data.columns = data.columns.str.replace('&','')
    data.drop('free_cash_flow',axis=1,inplace=True)
    features = data.columns.drop('Stock_code')
    int_feature = ['market_cap','volume','operating_cash_flow','total_cash_per_dollar' ,\
               'book_value_per_dollar',	'earnings_per_dollar'	,'revenue_per_dollar']
    cat_feature = ['sector','industry']
    # drop missing Stock_code
    data.dropna(subset=['Stock_code'],inplace=True)

    
    data['missing'] = data.isna().sum(axis=1).astype('int')
    cont_feature = features.drop(cat_feature)
    float_feature = [ 'price_per_sale', 'price_per_book',\
        'return_on_assets', 'return_on_equity', 'revenue_per_share',\
        'quarterly_revenue_growth', 'total_cash_per_share', 'debt_equity_ratio',\
        'book_value_per_share', \
        'Price_per_Earnings_ratio', 'earnings_per_shares',  'price_to_free_cash_flow',\
        'sp_52_week_change', 'stock_52_week_change']
    


    KMB_cols = ['market_cap','operating_cash_flow','volume']
    def transformKMB(x,cols,inplace= True):
        for col in cols:
            if x[col].dtypes !='object':
                return x[col]
            # x[col] = x[col].fillna(0)
            
    #         print(x[col].isna().any())
            temp = x[col].str.extract('([+-]?[0-9]*[.]?[0-9]+)([MKB]?)')
    #         temp[0]  = temp[0].fillna(0)
            temp[0] = temp[0].astype('float')
            def helper(x):
                symb = {'K':1 , 'M':1000, 'B':1000000}
            #     print(x.shape)
                return x[0]*symb[x[1]] if x[1] in symb else x[0]
            if inplace:
                x[col] = temp.apply(helper,axis=1)
                x[col] = x[col].fillna(0).astype(int)
            else:
                return temp.apply(helper,axis=1)

    transformKMB(data,KMB_cols)

    percentage_rows =['return_on_assets','return_on_equity','quarterly_revenue_growth','sp_52_week_change','stock_52_week_change']
    def transformPer(x,cols,inplace=True):
        for col in cols:
            if x[col].dtypes !='object':
                continue

            num_sym = x[col].str.extract('([+-]?[0-9]*[.]?[0-9]+)([MKB]?)')
            num_sym[0] = num_sym[0].astype('float')
            def helper(x):
                symb = {'K':1 , 'M':1000, 'B':1000000}
                return x[0]*symb[x[1]] if x[1] in symb else x[0]
            
            if inplace:
                x[col] = num_sym.apply(helper,axis=1)
            else:
                x[col+'per'] = num_sym.apply(helper,axis=1)


    transformPer(data,percentage_rows)

    # not sure which features contain comma, and therefore we include all features
    comma_rows = cont_feature
    def transformComma(x,cols,inplace = True):
        for col in cols:
            if x[col].dtypes !='object':
                continue
            if inplace:
                x[col] = x[col].str.replace(',' ,'')
            else:
                return x[col].str.replace(',' ,'')

    transformComma(data,features)
    
    #data['sp_average_change']  = data['sp_52_week_change'] ** (1/12)
    # data.drop(columns=['sp_52_week_change'])

    data[float_feature] = data[float_feature].astype('float64')
    # data[int_feature] = data[int_feature].fillna(0)
    # data.dropna(subset=int_feature,inplace=True)
    data[int_feature] = data[int_feature].astype('int64')

    # Missing values for cont_feature
    
    # imputer = SimpleImputer(missing_values=np.nan, strategy='median')
    # imputer = imputer.fit(data[cont_feature])
    # data[ cont_feature] = imputer.transform(data[cont_feature])
    


    folder = pathlib.Path(pathname)
    target_folder = folder.joinpath('../preprocessed')
    if not target_folder.exists():
        target_folder.mkdir()
    file_path = target_folder.joinpath(filename)

    data.to_csv(file_path.as_posix(),index=False)

if __name__ == '__main__':
    # create parser and handle arguments
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--fname",
                        type=str,
                        help="filename")
    PARSER.add_argument("--folder",
                        type=str,
                        default='./raw/',
                        help="folder of the file")
    # parse the arguments
    ARGS = PARSER.parse_args()
    preprocess(ARGS.folder,ARGS.fname)