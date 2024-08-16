import os
import getpass
from openai_batcher.batch import process_batch
from datasets import load_dataset

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

dataset = load_dataset("stanfordnlp/imdb")
train_df = dataset["train"].to_pandas()
train_df.shape

system_prompt = """
your task is to analyze the sentiment of the review and classify it as Positive or Negative. DO not add any explanation.
JSON:{"sentiment": String // Positive or Negative} 
"""
process_batch(
    system_prompt=system_prompt,
    batch_user_prompts=train_df["text"],
    start_index=0,
    end_index=25,
    batch_size=5
)