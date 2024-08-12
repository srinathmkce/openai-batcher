from openai import OpenAI
import logging
log = logging.getLogger(__name__)

def _initialize_openai():
    log.info("Initializing OpenAI client")
    client = OpenAI()
    return client


def _upload_batch_file_to_openai(client, batch_file_path):
    log.info(f"Uploading batch file to OpenAI: {batch_file_path}")
    batch_file = client.files.create(file=open(batch_file_path, "rb"), purpose="batch")
    return batch_file

def _start_batch_execution(client, batch_id):
    log.info(f"Starting batch execution for file: {batch_id}")
    batch_job = client.batches.create(
      input_file_id=batch_id,
      endpoint="/v1/chat/completions",
      completion_window="24h"
    )
    return batch_job