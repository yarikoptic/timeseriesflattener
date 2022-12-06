"""Test that feature spec objects work as intended."""
import pandas as pd
import pytest

from timeseriesflattener.feature_spec_objects import (
    AnySpec,
    check_that_col_names_in_kwargs_exist_in_df,
)


def test_anyspec_init():
    """Test that AnySpec initialises correctly."""
    values_loader_name = "synth_predictor_float"

    spec = AnySpec(
        values_loader=values_loader_name,
        prefix="test",
    )

    assert isinstance(spec.values_df, pd.DataFrame)
    assert spec.feature_name == values_loader_name


def test_loader_kwargs():
    """Test that loader kwargs are passed correctly."""
    spec = AnySpec(
        values_loader="synth_predictor_float",
        prefix="test",
        loader_kwargs={"n_rows": 10},
    )

    assert len(spec.values_df) == 10


def test_anyspec_incorrect_values_loader_str():
    """Raise error if values loader is not a key in registry."""
    with pytest.raises(ValueError, match=r".*in registry.*"):
        AnySpec(values_loader="I don't exist", prefix="test")


def test_that_col_names_in_kwargs_exist_in_df():
    """Raise error if col name specified which is not in df."""
    # Create a sample dataframe
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})

    # Test valid column names
    data = {"col_name_1": "A", "col_name_2": "B", "values_df": df}
    check_that_col_names_in_kwargs_exist_in_df(data=data, df=df)

    # Test invalid column names
    data = {"col_name_1": "A", "col_name_2": "D", "values_df": df}
    with pytest.raises(ValueError, match="D is not in df"):
        check_that_col_names_in_kwargs_exist_in_df(data=data, df=df)