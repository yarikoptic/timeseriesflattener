import time

import numpy as np

import psycopmlutils.loaders  # noqa

from wasabi import msg

from psycopmlutils.timeseriesflattener import (
    create_feature_combinations,
    FlattenedDataset,
)


if __name__ == "__main__":
    PREDICTOR_LIST = create_feature_combinations(
        [
            {
                "predictor_df": "hba1c",
                "lookbehind_days": [90, 180, 365, 730],
                "resolve_multiple": ["latest", "mean"],
                "fallback": np.nan,
                "source_values_col_name": "val",
                "new_col_name": "hba1c",
            }
        ]
    )

    print(PREDICTOR_LIST)

    prediction_times = psycopmlutils.loaders.LoadVisits.physical_visits_to_psychiatry()
    event_times = psycopmlutils.loaders.LoadDiagnoses.t2d_times()

    msg.info("Initialising flattened dataset")
    flattened_df = FlattenedDataset(prediction_times_df=prediction_times, n_workers=32)

    # Predictors
    msg.info("Adding predictors")
    start_time = time.time()

    flattened_df.add_temporal_predictors_from_list_of_argument_dictionaries(
        predictors=PREDICTOR_LIST,
    )

    end_time = time.time()
    msg.good(f"Finished adding predictors, took {end_time - start_time}")
