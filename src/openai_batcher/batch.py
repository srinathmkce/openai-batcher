import pandas as pd
import logging
from openai_batcher._validation import _validate_openai_key, _validate_data_types
from openai_batcher._prompt_generator import _write_prompts_to_file, _generate_prompt
from typing import Union

# Configure logging
logging.basicConfig(
    filename="batch_processor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def process_batch(
    system_prompt: str,
    batch_user_prompts: Union[list, pd.Series],
    start_index: int,
    end_index: int,
    batch_size: int,
    batch_ids: Union[str, list, pd.Series] = "auto",
) -> None:
    """
    Processes the batch of user prompts.
    Args:
        system_prompt (str): The system prompt.
        batch_user_prompts (Union[list, pd.Series]): The batch of user prompts.
        start_index (int): The start index of the batch.
        end_index (int): The end index of the batch.
        batch_size (int): The batch size.
        batch_ids (Union[str, list, pd.Series], optional): The batch IDs. Defaults to "auto".
    Returns:
        None: This function does not return anything.
    """
    _validate_openai_key()
    _validate_data_types(
        system_prompt, batch_user_prompts, start_index, end_index, batch_size, batch_ids
    )

    if isinstance(batch_ids, str) and batch_ids == "auto":
        batch_ids = [f"{i}" for i in range(len(batch_user_prompts))]

    for start in range(start_index, end_index, batch_size):
        end = min(start + batch_size, end_index)

        logging.info(f"Processing batch from {start} to {end}...")
        batch_file_name = f"batch_{start}_{end}.jsonl"

        batch_prompts = _generate_prompt(
            batch_ids=batch_ids[start:end],
            batch_user_prompts=batch_user_prompts[start:end],
            system_prompt=system_prompt,
        )
        _write_prompts_to_file(file_name=batch_file_name, prompt_list=batch_prompts)


if __name__ == "__main__":
    import os

    system_prompt = "Translate the following English sentences to French."
    batch_user_prompts = ["Hello, how are you?", "What is your name?", "Where are you from?"]
    start_index = 0
    end_index = len(batch_user_prompts)
    batch_size = 2
    os.environ["OPENAI_API_KEY"] = "your-key"
    process_batch(system_prompt, batch_user_prompts, start_index, end_index, batch_size)
