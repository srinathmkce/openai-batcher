from openai_batcher.batch import process_batch
from datasets import load_dataset


dataset = load_dataset("stanfordnlp/imdb")
train_df = dataset["train"].to_pandas()
system_promt = """
your task is to analyze the sentiment of the review and classify it as Positive or Negative. DO not add any explaination
"""
print(train_df.columns)
process_batch(system_prompt=system_promt,batch_user_prompts=train_df["text"],start_index=0,end_index=25,batch_size=5)
