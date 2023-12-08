import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    result = pd.DataFrame()

    target_df = pd.read_csv('data/train_scores.csv')
    for index in range(9):
        path = f'datasets/engineered_train_logs_{index}.csv'
        feature_df = pd.read_csv(path)
        ids = feature_df['id'].unique().tolist()
        target_df = target_df[target_df['id'].isin(ids)]

        X = feature_df.drop(['id'], axis=1)
        Y = target_df.drop(['id'], axis=1)

        # split data set
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        rf = RandomForestClassifier(n_estimators=200)
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



