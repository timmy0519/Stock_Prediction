from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler,OneHotEncoder
from xgboost import XGBClassifier
import pathlib
import glob
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.base import TransformerMixin, BaseEstimator
import pandas as pd
import matplotlib.pyplot as plt

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
numerical_cols = df.select_dtypes('number').columns
id_feature = ['Stock_code']
categorical_cols = df.select_dtypes(exclude = ['number','boolean']).columns.drop(['Stock_code'])
target_feature = ['trend_sp']

X = df.drop(target_feature + id_feature,axis=1)
y = df[target_feature]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

class Debug(BaseEstimator, TransformerMixin):

    def transform(self, X):
        print(X.shape)
        display(pd.DataFrame(X))
#         self.shape = shape
        # what other output you want
        return X

    def fit(self, X, y=None, **fit_params):
        return self

# Preprocessing for numerical data
numerical_transformer =  Pipeline(steps=[
#     ('imputer', SimpleImputer(strategy='median')),
    ('std', StandardScaler())
])
# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant',fill_value='nan')),
    ('oe', OrdinalEncoder())
])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

model = XGBClassifier()

# Bundle preprocessing and modeling code in a pipeline
my_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
#                               ("debug", Debug()),
                              ('model', model)
                             ])

X_train_after = preprocessor.fit_transform(X_train)
X_test_after = preprocessor.transform(X_test)

model.fit(X_train_after,y_train)

y_train_hat = model.predict(X_train_after)
y_test_hat = model.predict(X_test_after)

print(accuracy_score(y_train, y_train_hat))
print(accuracy_score(y_test, y_test_hat))


from sklearn.inspection import permutation_importance
perm_importance = permutation_importance(model, X_test_after, y_test)

sorted_idx = perm_importance.importances_mean.argsort()
plt.figure(figsize=(6,8))
plt.barh(X.columns[sorted_idx], perm_importance.importances_mean[sorted_idx])
plt.xlabel("Permutation Importance")

plt.barh(X.columns, model.feature_importances_)

filtered_features = X.columns[sorted_idx][6:]
filtered_features

filtered_features = ['Price per Earnings ratio', 'total cash per dollar', 'sector',
       'debt equity ratio', 'missing', 'quarterly revenue growth',
       'total cash per share', 'earnings per shares', 'stock 52 week change',
       'earnings per dollar', 'price per sale', 'revenue per share',
       'return on equity', 'industry', 'volume', 'return on assets',
       'market cap']