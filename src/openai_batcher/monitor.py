import time
import os
import logging
from openai_batcher.config import OUTPUT_DIR, WAIT_TIME_IN_SECONDS

log = logging.getLogger(__name__)

def _fetch_results(client, job_id, output_file_name):
    """
    Fetches the results of a job from the OpenAI client and writes it to a file.

    Args:
        client (OpenAI.Client): The OpenAI client object.
        job_id (str): The ID of the job.
        output_file_name (str): The name of the output file.

    Returns:
        None
    """
    result_file_id = client.batches.retrieve(batch_id=job_id).output_file_id
    if not result_file_id:
        log.error(f"Output file ID not found for job: {job_id}")
        return 
    result = client.files.content(result_file_id).content
    result_file_path = os.path.join(OUTPUT_DIR, f"output_{output_file_name}")
    log.info(f"Writing to file: {result_file_path}")
    with open(result_file_path, 'wb') as file:
        file.write(result)


#TODO: Rewrite this code using polling
def _wait_until_job_is_finished(client, job_id, output_file_name):
    """
    Waits until the specified job is finished.

    Args:
        client: The client object used to interact with the API.
        job_id: The ID of the job to monitor.
        output_file_name: The name of the file associated with the job.

    Returns:
        None
    """
    while True:
        status = client.batches.retrieve(batch_id=job_id).status
        log.info(f"Job Status: {status}")
        if status == "failed" or status == "error":
            log.error(f"Error with the batch - {output_file_name}")
            print(f"Issue with the batch - {output_file_name}")
            return
        elif status == "completed":
            log.info(f"Batch completed and fetching results")
            _fetch_results(client=client, job_id=job_id, output_file_name=output_file_name)
            return
        elif status == "in_progress":
            log.info(f"Batch execution for {output_file_name} is in progress. Sleeping for 30 seconds")
            time.sleep(WAIT_TIME_IN_SECONDS)
        #TODO - Add more status checks
        # else:
        #     log.error(f"Unknown status: {status}")
        #     return
    return 
    