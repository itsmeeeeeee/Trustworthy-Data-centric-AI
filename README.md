# Trustworthy-Data-centric-AI

This repository is a modified version of the following repository: https://github.com/protagolabs/seq2seq_llm_evaluation. Many scripts have been adapted for this project.

# The project is structured as follows:

data: This folder hosts all the data. There are 100 sampels for task Summersation und Simplification and the json datei for human evaluation. The result could be find at data/outputs/agreggated
main: The folder hosting the main code in the subfolders below.
text_generation: This folder contains the modules to prompt the LLMs to generate the main outputs to be evaluated for two three tasks, text summarisation, simplification
data_processing: This folder contains all utils  modules used for data preprocessing.  merge_outputs.py should be run after running the files in the text_generation folder and before running the files in the automatic_evaluation folder. 
automatic_evaluation: This folder contains the code used to reproduce the automatic metrics results.

human_and_gpt4_evaluation: This folder contains the code used to prompt GPT-4 to evaluate LLMs outputs, 
instructions_to_human_reviewers_and_gpt4: This subfolder contains the instructions given to human reviewers, and the prompts used for GPT-4 model-to-model evaluation. The instructions to human reviewers are reported in html files. 
