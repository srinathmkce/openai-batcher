import pandas as pd
import logging
import os
from openai_batcher.interface import _initialize_openai
from openai_batcher.validation import _validate_openai_key, _validate_data_types
from openai_batcher.prompt_generator import _write_prompts_to_file, _generate_prompt, _create_input_output_directory
from openai_batcher.interface import _upload_batch_file_to_openai, _start_batch_execution
from openai_batcher.config import INPUT_DIR
from openai_batcher.monitor import _wait_until_job_is_finished
from typing import Union
from openai import OpenAI
from tqdm import tqdm

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

    client = _initialize_openai()
    _create_input_output_directory()

    for start in tqdm(range(start_index, end_index, batch_size)):
        end = min(start + batch_size, end_index)

        logging.info(f"Processing batch from {start} to {end}...")
        batch_file_name = f"batch_{start}_{end}.jsonl"
        batch_file_path  = os.path.join(INPUT_DIR, batch_file_name)

        batch_prompts = _generate_prompt(
            batch_ids=batch_ids[start:end],
            batch_user_prompts=batch_user_prompts[start:end],
            system_prompt=system_prompt,
        )
        _write_prompts_to_file(batch_file_path=batch_file_path, prompt_list=batch_prompts)
        batch_file = _upload_batch_file_to_openai(client=client, batch_file_path=batch_file_path)
        batch_job = _start_batch_execution(client=client, batch_id=batch_file.id)
        _wait_until_job_is_finished(client=client, job_id=batch_job.id, output_file_name=batch_file_name)
        