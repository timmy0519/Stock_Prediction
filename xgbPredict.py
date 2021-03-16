
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler,OneHotEncoder
from xgboost import XGBClassifier, XGBRegressor
import pathlib
import glob
from sklearn.metrics import accuracy_score,precision_score,median_absolute_error,mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.base import TransformerMixin, BaseEstimator
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pickle import dump,load

def xgbPredict():
    dir_path = pathlib.Path('train/')
    csv_path = dir_path.joinpath('*.csv')


    all_files = glob.glob(csv_path.as_posix())
    df=None
    for f in all_files:
        if  df is None:
            df = pd.read_csv(f)
        else:
            df = pd.concat([df,pd.read_csv(f)])
    # df = df.drop(['market cap','volume','operating cash flow'],axis=1)

    # With all features
    numerical_cols = df.select_dtypes('number').columns.drop('trend_sp')
    id_feature = ['Stock_code']
    categorical_cols = df.select_dtypes(exclude = ['number','boolean']).columns.drop(['Stock_code'])
    target_feature = ['trend_sp']

    X = df.drop(target_feature + id_feature,axis=1)
    y = df[target_feature]

    preprocessor = load(open('model/preprocessor.pkl', 'rb'))
    X_test = preprocessor.transform(X)

    model = XGBRegressor()
    model.load_model('model/xgboost_0311.json')

    y_test_hat = model.predict(X_test)

    k=30

    topK = df.iloc[y_test_hat.argsort()[-k:]]
    print("The mean of top {} predicted profit against GSPC is {:.2f}%".format(k,topK.trend_sp.mean()) )
    topK.Stock_code.to_csv('predictions/pred.csv',index=False,header=False)

if __name__ == '__main__':
    xgbPredict()