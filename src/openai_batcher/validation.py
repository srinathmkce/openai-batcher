import os
import pandas as pd
from typing import Union


def _validate_openai_key():
    """
    Validates the OPENAI_API_KEY environment variable.
    """
    if not os.environ["OPENAI_API_KEY"]:
        raise ValueError(
            "OPENAI_API_KEY is not set. Please set it using `export OPENAI_API_KEY=your-key`"
        )


def _validate_data_types(
    system_prompt: str,
    batch_user_prompts: Union[list, pd.Series],
    start_index: int,
    end_index: int,
    batch_size: int,
    batch_ids: Union[str, list, pd.Series] = "auto",
):
    """
    Validates the data types of the input parameters.
    """
    if not isinstance(system_prompt, str):
        raise ValueError("system_prompt must be a string.")

    if not isinstance(batch_user_prompts, (list, pd.Series)):
        raise ValueError("user_prompt must be a list, or pandas Series.")

    if not isinstance(start_index, int):
        raise ValueError("start_index must be an integer.")

    if not isinstance(end_index, int):
        raise ValueError("end_index must be an integer.")

    if not isinstance(batch_size, int):
        raise ValueError("batch_size must be an integer.")

    if not isinstance(batch_ids, (str, list, pd.Series)):
        raise ValueError("batch_ids must be a string, list, or pandas Series.")
