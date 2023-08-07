#!/usr/bin/env python
# coding: utf-8
"""Fill NA custom transformer.
"""

import os
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class ToDatetime(TransformerMixin, BaseEstimator):
    """Fill Na records with a given value. 

    Parameters
    ----------
    columns : list
        List of column names.
    
    errors : str, {‘ignore’, ‘raise’, ‘coerce’}, default ‘raise’
        - If 'raise', then invalid parsing will raise an exception.
        - If 'coerce', then invalid parsing will be set as NaT.
        - If 'ignore', then invalid parsing will return the input.
    """

    def __init__(
        self,
        columns: list,
        errors='coerce'
    ):
        self._feature_names_out = columns
        self.errors = errors
    
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
            ToDatetime transformer class instance.
        """
        return self

    def transform(self, X):
        """Transform X using the forward function.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Input array.

        Returns
        -------
        X_out : array-like, shape (n_samples, n_features)
            Transformed input.
        """
        return self._transform(X)

    def inverse_transform(self, X):
        """[NOT IMPLEMENTED] Transform X using the inverse function.

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

        This method is only defined if `feature_names_out` is not None.

        Parameters
        ----------
        input_features : Ignored
            Not used, present here for API consistency by convention.

        Returns
        -------
        feature_names_out : ndarray of str objects
            Transformed feature names.
        """
        return np.asarray(
            self._feature_names_out, 
            dtype=object
        )

    def _transform(self, X):
        res = dict()
        for c in self._feature_names_out:
            res[c] = pd.to_datetime(X[c], errors=self.errors, utc=True)

        return pd.DataFrame(data=res)

    def __sklearn_is_fitted__(self):
        """Return True since FunctionTransfomer is stateless."""
        return True
