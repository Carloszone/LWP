import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

if __name__ == '__main__':
    result = pd.DataFrame()

    target_df = pd.read_csv('data/train_scores.csv')
    for index in range(9):
        print('index: ', index)
        path = f'datasets/engineered_train_logs_{index}.csv'
        feature_df = pd.read_csv(path)
        ids = feature_df['id'].unique().tolist()

        X = feature_df.drop(['id'], axis=1)
        Y = target_df[target_df['id'].isin(ids)]['score']

        print('X shape: ', X.shape)
        print('Y shape: ', Y.shape)

        # split data set
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)

        rf = RandomForestRegressor(n_estimators=200)
        rf.fit(X_train, Y_train)

        # get importance
        importance = rf.feature_importances_

        # add importance to result
        result[f'importance_{index}'] = importance

    # calculate mean importance
    result['mean_importance'] = result.mean(axis=1)

    # add feature name
    result['feature_name'] = X.columns

    # save reuslt
    result.to_csv('feature_importance.csv', index=False)



