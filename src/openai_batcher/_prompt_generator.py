import os
import json
from openai_batcher.config import (
    INPUT_DIR,
    MODEL_NAME,
    TEMPERATURE,
    RESPONSE_FORMAT,
    MESSAGE_FORMAT,
)
import logging
from typing import List, Dict, Any

log = logging.getLogger(__name__)


def _write_prompts_to_file(file_name: str, prompt_list: List[Dict[str, Any]]) -> None:
    """
    Write prompts to a file.
    Args:
        file_name (str): The name of the file to write the prompts to.
        prompt_list (List[Dict[str, Any]]): A list of prompts to write to the file.
    Returns:
        None
    """
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)

    batch_file_path = os.path.join(INPUT_DIR, file_name)
    with open(batch_file_path, "w") as file:
        for prompt in prompt_list:
            file.write(json.dumps(prompt) + "\n")
    log.info(f"Prompts written to {batch_file_path}")


def _generate_prompt(batch_ids: List[str], batch_user_prompts: List[str], system_prompt: str) -> List[Dict[str, Any]]:
    """
    Generate a list of prompt dictionaries based on the given batch_ids, batch_user_prompts, and system_prompt.
    Args:
        batch_ids (List[str]): The list of batch IDs.
        batch_user_prompts (List[str]): The list of user prompts for each batch.
        system_prompt (str): The system prompt.
    Returns:
        List[Dict[str, Any]]: A list of prompt dictionaries, where each dictionary represents a prompt with the following keys:
            - "custom_id" (str): The custom ID for the task.
            - "method" (str): The HTTP method for the request.
            - "url" (str): The URL for the request.
            - "body" (Dict[str, Any]): The body of the request, containing the model, temperature, response format, and messages.
    Raises:
        AssertionError: If the length of batch_ids and batch_user_prompts is not the same.
    """
    assert len(batch_ids) == len(
        batch_user_prompts
    ), "batch_ids and batch_user_prompts must have the same length."

    prompt_list = []
    for index, user_prompt in enumerate(batch_user_prompts):
        prompt_dict = {
            "custom_id": f"task-{batch_ids[index]}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": MODEL_NAME,
                "temperature": TEMPERATURE,
                "response_format": RESPONSE_FORMAT,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            },
        }
        if MESSAGE_FORMAT:
            prompt_dict["body"]["message_format"] = MESSAGE_FORMAT
        prompt_list.append(prompt_dict)
    return prompt_list
