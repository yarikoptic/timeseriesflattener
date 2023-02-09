"""This module contains functions for handling dataframes with multiindex columns."""
from typing import List, Optional

import pandas as pd

from timeseriesflattener.feature_spec_objects import TemporalSpec


class ColumnHandler:
    """Class for handling dataframes with multiindex columns."""

    @staticmethod
    def rename_value_column(
        df: pd.DataFrame,
        output_spec: TemporalSpec,
    ) -> pd.DataFrame:
        """Renames the value column to the column name specified in the output_spec.
        Handles the case where the output_spec has a multiindex.

        Args:
            output_spec (TemporalSpec): Output specification
            df (pd.DataFrame): Dataframe with value column
        """
        if isinstance(df["value"], pd.DataFrame):
            df = ColumnHandler._rename_multi_index_dataframe(output_spec, df)
        else:
            df = df.rename(columns={"value": output_spec.get_col_str()})
        return df

    @staticmethod
    def _rename_multi_index_dataframe(
        output_spec: TemporalSpec,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Renames a multiindex dataframe to the column names specified in the
        output_spec.

        Args:
            output_spec (TemporalSpec): Output specification
            df (pd.DataFrame): Dataframe with value column as multiindex
        """
        feature_names = df["value"].columns
        col_names = [
            output_spec.get_col_str(additional_feature_name=feature_name)
            for feature_name in feature_names
        ]
        feature_col_name_mapping = dict(zip(feature_names, col_names))
        # level=1 means that the column names are in the second level of the multiindex
        df = df.rename(columns=feature_col_name_mapping, level=1)
        return df

    @staticmethod
    def replace_na_in_spec_col_with_fallback(
        df: pd.DataFrame,
        output_spec: TemporalSpec,
    ) -> pd.DataFrame:
        """Adds fallback to value columns in df. If the value column is a multiindex,
        adds fallback to all columns in the multiindex. Otherwise, adds fallback to the
        single value column.

        Args:
            df (pd.DataFrame): Dataframe with value column
            output_spec (TemporalSpec): Output specification
        """
        if "value" in df.columns and isinstance(df["value"], pd.DataFrame):
            df["value"] = df["value"].fillna(output_spec.fallback)
        else:
            df[output_spec.get_col_str()] = df[output_spec.get_col_str()].fillna(
                output_spec.fallback,
            )
        return df

    @staticmethod
    def flatten_multiindex(df: pd.DataFrame) -> pd.DataFrame:
        """Checks if dataframe has multiindex columns and flattens them if it does.
        In this case, flattening means stripping the first level of the multiindex.

        Args:
            df (pd.DataFrame): Dataframe to (potentially) flatten"""
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(1)
        return df

    @staticmethod
    def get_value_col_str_name(
        df: Optional[pd.DataFrame] = None,
        output_spec: Optional[TemporalSpec] = None,
    ) -> List[str]:
        """Returns the name of the value column in df. If df has a multiindex,
        returns a list of all column names in the 'value' multiindex.

        Args:
            df (pd.DataFrame): Dataframe to get value column name from.
            output_spec (TemporalSpec): Output specification"""
        if df is not None or output_spec is not None:
            return (
                df["value"].columns.tolist()  # type: ignore
                if isinstance(df.columns, pd.MultiIndex)  # type: ignore
                else [output_spec.get_col_str()]  # type: ignore
            )
        else:
            raise ValueError("Either df or output_spec must be provided.")