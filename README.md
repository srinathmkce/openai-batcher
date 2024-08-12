# OpenAI Batcher

OpenAI Batcher is a Python package designed to process batches of user prompts using OpenAI's API. It allows for efficient batch processing and monitoring of jobs.

## Installation

To install the package, clone the repository and install the dependencies:

```bash
git clone https://github.com/srinathmkce/openai-batcher
cd openai_batcher
pdm install
```
Alternatively, you can install the package directly using pip:

```bash
pip install openai_batcher
```
## Usage

Here's an example of how to use the process_batch function from the package:

```bash
from openai_batcher.batch import process_batch
from datasets import load_dataset

# Load dataset
dataset = load_dataset("stanfordnlp/imdb")
train_df = dataset["train"].to_pandas()

# Define system prompt
system_prompt = """
your task is to analyze the sentiment of the review and classify it as Positive or Negative. DO not add any explanation
"""

# Process batch
process_batch(
    system_prompt=system_prompt,
    batch_user_prompts=train_df["text"],
    start_index=0,
    end_index=25,
    batch_size=5
)
```

## Development
To develop this package inside a development container, use the provided devcontainer.json and Dockerfile.

Using Dev Container Open the project in Visual Studio Code.Install the Remote - Containers extension.Reopen the project in the container. Building the Docker Image To build the Docker image manually, run:


```bash
docker build -t openai-batcher .
```
