Data that are preprocessed and ready for training.

1. Text to number format
2. 1,000 -> 1000
3. Missing values for Continuous variables are preprocessed
4. Missing values for Categorical var not preprocessed 
    (xgboost and fastai lib have different ways to handle)  