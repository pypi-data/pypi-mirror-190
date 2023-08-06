#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 09:04:18 2023

@author: reececalvin
"""

from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn import metrics
import seaborn as sns
import numpy as np

def random_forest(dfs, feature_lists, y_val, plt_max_depth = 30):
    
    models = []
    
    for df,feature_list in zip(dfs, feature_lists):
        
        max_depth = plt_max_depth

        x_feat_list = feature_list

        df_standard = df[x_feat_list]/df[x_feat_list].std()

        df_standard[y_val] = df[y_val]

        sample = df_standard.sample(frac=.25)

        # extract data from dataframe
        x = sample.loc[:, x_feat_list].values
        y = sample.loc[:, y_val].values

        rf_clf = RandomForestClassifier(max_depth=max_depth, n_estimators=100)

        rf_clf.fit(x, y)

        sns.set()

        plot_feat_import(x_feat_list, rf_clf.feature_importances_)

        training_df = df_standard.sample(frac=0.3)

        # The remaining data is the testing data
        testing_df = df_standard.drop(training_df.index)


        X = training_df[x_feat_list]
        Y = training_df[y_val]

        x = testing_df[x_feat_list]
        y_true = testing_df[y_val]

        ac_scores = {}
        best_depth = 0
        best_ac = 0
        
        for depth in range(10,70,5):
            rf_clf = RandomForestClassifier(max_depth=max_depth, n_estimators=100)
            rf_clf.fit(X, Y)
            y_pred = rf_clf.predict(x)

            ac_score = metrics.accuracy_score(y_true, y_pred)

            ac_scores[depth] = ac_score
            
            if ac_score > best_ac:
                best_depth = depth
            
        rf_clf = RandomForestClassifier(max_depth=best_depth, n_estimators=100)
        rf_clf.fit(X, Y)
        
        models.append((rf_clf, ac_scores))
        
    return models


def plot_feat_import(feat_list, feat_import, sort=True, limit=None):
    """ plots feature importances in a horizontal bar chart
    
    Args:
        feat_list (list): str names of features
        feat_import (np.array): feature importances (mean gini reduce)
        sort (bool): if True, sorts features in decreasing importance
            from top to bottom of plot
        limit (int): if passed, limits the number of features shown
            to this value    
    """
    
    if sort:
        # sort features in decreasing importance
        idx = np.argsort(feat_import).astype(int)
        feat_list = [feat_list[_idx] for _idx in idx]
        feat_import = feat_import[idx] 
        
    if limit is not None:
        # limit to the first limit feature
        feat_list = feat_list[:limit]
        feat_import = feat_import[:limit]
    
    # plot and label feature importance
    plt.barh(feat_list, feat_import)
    plt.gcf().set_size_inches(5, len(feat_list) / 2)
    plt.xlabel('Feature importance\n(Mean decrease in Gini across all Decision Trees)')