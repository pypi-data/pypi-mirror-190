#!/usr/bin/env python
# coding: utf-8
"""Identity custom transformer.
"""

import os
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin, OneToOneFeatureMixin


class Identity(OneToOneFeatureMixin, TransformerMixin, BaseEstimator):
    """Identity transformer.

    Parameters
    ----------
    columns: list or None,
        List of column Names to be returned by the identity function;
    """

    def __init__(self, columns:list=None):
        self.columns = columns
    
    def fit(self, X: pd.DataFrame, y=None):
        """Fit transformer by checking X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Input array.

        y : Ignored
            Not used, present here for API consistency by convention.

        Returns
        -------
        self : object
            Identity transformer class instance.
        """
        return self

    def transform(self, X):
        """Identity Transformation of X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Input array.

        Returns
        -------
        X_out : array-like, shape (n_samples, n_features)
            Transformed input.
        """
        if self.columns is not None:
            return X[self.columns]
        
        return X

    def inverse_transform(self, X):
        """Transform X using the inverse function.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Input array.

        Returns
        -------
        X_out : array-like, shape (n_samples, n_features)
            Transformed input.
        """
        return X
    
    def get_feature_names_out(self, input_features=None):
        """Get output feature names for transformation.

        Parameters
        ----------
        input_features : array-like of str or None, default=None
            Input features.
            - If columns is an array-like, then columns is returned.

            - If columns is None, then:
                - If `input_features` is `None`, then `feature_names_in_` is
                used as feature names in. If `feature_names_in_` is not defined,
                then the following input feature names are generated:
                `["x0", "x1", ..., "x(n_features_in_ - 1)"]`.
                - If `input_features` is an array-like, then `input_features` must
                match `feature_names_in_` if `feature_names_in_` is defined.

        Returns
        -------
        feature_names_out : ndarray of str objects
            Same as input features.
        """
        if self.columns is not None:
            return np.asarray(self.columns, dtype=object)
        
        return super(__class__, self).get_feature_names_out(input_features)
