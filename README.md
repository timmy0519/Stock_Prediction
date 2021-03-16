# Stock Prediction

## Workflow for generating training data
![Alt text](https://g.gravizo.com/svg?digraph%20di%20{%20raw[label=%22html_raw%22]%20first[label=%22html_preprocessed%22]%20gen_train[label=%22gen_train%22]%20g_raw[label=%22gspc_raw%22]%20g[label=%22gspc_preprocessed%22]%20raw-%3Efirst%20first-%3Egen_train%20g_raw-%3Eg%20g-%3Egen_train%20gen_train-%3Etrain%20})
<details> 
<summary></summary>
custom_mark10
digraph di{
    raw[label="html_raw"];
    first[label="html_preprocessed"];
    gen_train[label="gen_train"];
    g_raw[label="gspc_raw"];
    g[label="gspc_preprocessed"];
    raw->first;
    first->gen_train;
    g_raw->g;
    g->gen_train;
    gen_train->train;
}
custom_mark10
</details>

Raw data should be placed to the corresponding "raw" folder and the folder structure should be created beforehand.

### Folder structure

- htmlData
    - raw
    - preprocessed (intermediate folder for gen_train_all)
- streamData
    - raw 
    - filtered (intermediate folder for gen_train_all)
- train (data after gen_train_all, which is ready to train and predict)
- predictions(list of top 30 stock code after calling xgbPredict.py)
- *.py 

### Command to execute
```bash
python gen_train_all.py # produce ready to train data from **/raw to train/
python xgbPredict.py # produce preds.csv in predictions/
```
