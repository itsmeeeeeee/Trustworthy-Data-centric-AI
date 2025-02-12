"""
This script is used to generate the outputs for all OpenAI models except ChatGPT, for all three NLP tasks:
text summarisation, simplification and grammatical error correction. To generate outputs using ChatGPT,
see main/text_generation/chatgpt.py
"""
import os
import json
import time
import argparse
from datetime import datetime
import openai
import pandas as pd
import pytz

openai.api_key = os.getenv("OPENAI_API_KEY")

models_to_run = [
    "text-davinci-003",
    # "text-davinci-001",
    "davinci-instruct-beta",
    # "curie-instruct-beta"
]

advanced_simplification_prompts = [
    # Prompt A: Generate two different simplified versions, then pick the best
    (
        "Generate TWO different simplified versions of the text below. "
        "Then pick the one that is simpler and clearer. "
        "**Important:** Output only your final chosen version.\n\n"
        "Original text: [...]"
    ),
    # Prompt B: Two-step approach (detect problematic terms, then rewrite)
    (
        "Step 1: Identify any difficult words or phrases in the text.\n"
        "Step 2: Replace them with simpler alternatives and rewrite the text in short sentences."
        "**Important:** Provide only the simplified text.\n\n"
        "Text to simplify: [...]"
    ),
    # Iterative Refinement (Self-Reflection)
    ("Step 1: Rewrite the text below in a simpler and clearer way, while preserving its meaning.\n"
    "Step 2: Analyze your simplified text and identify any remaining complex words or unclear structures.\n"
    "Step 3: Improve the simplification by making it even more accessible. Ensure sentences are short, direct, and free of jargon.\n"
    "**Important:** Output only the final refined version.\n\n"
    "Text to simplify: [...]"),

    # Audience-Specific Simplificatio

    ("Rewrite the text below so that it is easily understandable for a 8-year-old children.\n"
    "Ensure that:\n"
    "- Sentences are short and direct.\n"
    "- Difficult words are replaced with simple alternatives.\n"
    "- The overall meaning remains the same.\n\n"
    "**Important:** Output only the final refined version.\n\n"
    "Text to simplify: [...]"

),
    # Explain & Rewrite (Chain-of-Thought Simplification)
   ("Step 1: Identify the challenging words, phrases, or sentence structures in the text and explain why they might be difficult to understand.\n"
    "Step 2: Rewrite the text in simpler language while ensuring that the original meaning is preserved.\n"
    "Step 3: Verify that the rewritten version is clear and easy to understand.\n"
    "**Important:** Provide only the final, simplified version.**\n\n"
    "Text to simplify: [...]"
)
]



advanced_summarisation_prompts = [
    
    (
        "Provide a structured summary of the following text. Follow these steps internally but output only the final summary:\n\n"
        "Step 1: Identify a suitable title based on the text.\n"
        "Step 2: Extract the three most important key points.\n"
        "Step 3: Generate a concise summary in 1-2 sentences using the key points.\n\n"
        "**Important:** Do not include the title or key points in the output. Only return the final summary.\n\n"
        "Text: [...]"
    ),
    
    (
        "Summarize the following text in 2-3 sentences while keeping the key information intact.\n"
        "**Output only the final summary, without explanations or bullet points.**\n\n"
        "Text: [...]"
    ),

    (
        "Generate a highly concise summary of the following text in a **single sentence** while preserving its main idea.\n"
        "**Return only the final summary sentence, without any additional text.**\n\n"
        "Text: [...]"
    )
]


advanced_gec_prompts = [
    # Prompt A: Two-step correction (correct, then refine)
    (
        "Perform a two-step grammar correction:\n"
        "1) Correct all obvious grammar/spelling mistakes.\n"
        "2) Re-check the sentence and refine if needed.\n"
       "**Important:** Only return the final corrected version..\n\n"
        "Input sentence: [...]"
    ),
    # Prompt B: Another two-pass approach with emphasis on fluency
    (
        "First pass: fix grammatical errors.\n"
        "Second pass: ensure the sentence is fluent and natural in standard English.\n"
        "**Important:** Return the final corrected version only.\n\n"
        "Sentence: [...]"
    ),
   (
      "Step 1: Identify and list any grammar, spelling, or fluency errors in the sentence.\n"
      "Step 2: Explain why each mistake is incorrect and how it can be improved.\n"
      "Step 3: Rewrite the corrected sentence in standard English with natural fluency.\n"
      "**Important:** Return only the final corrected version.\n\n, without any additional text.\n\n"
      "Sentence: [...]"),

   ( 
       "Perform a multi-level correction of the following sentence:\n"
        "1) Fix all grammatical, spelling, and punctuation mistakes.\n"
        "2) Improve clarity by simplifying complex structures.\n"
        "3) Enhance precision by removing unnecessary words or ambiguity.\n"
        "**Important:** Provide only the final improved version.\n\n"
        "Sentence: [...]")


]


temperatures = [0, 0.5, 0.7]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", "--task", help="The task to use. Can be 'Summarisation', 'Simplification' or 'GEC'.",
        choices=["Summarisation", "Simplification", "GEC"], required=True
    )
    args = parser.parse_args()
    TASK = args.task  # change task as appropriate
    time_now = datetime.now(pytz.timezone('Europe/London')).strftime('%Y-%m-%dT%H:%M:%S')
    if TASK == 'Simplification':
        #with open('data/100_sample/simplification_texts.csv', 'r') as f:
            #inputs = f.readlines()
            #inputs = [i.strip("\n") for i in inputs]
        df = pd.read_csv('data/100_sample/simplification_texts.csv')
        inputs = df['displayed_text']
        prompts = advanced_simplification_prompts
    elif TASK == 'Summarisation':
        df = pd.read_csv('data/100_sample/summarisation_texts.csv')
        inputs = df['displayed_text']
      
        # inputs_1506 = df['article_trunc1506']
        prompts = advanced_summarisation_prompts
    elif TASK == 'GEC':
        df = pd.read_csv('data/100_sample/gec_texts.csv')
        inputs = df['displayed_text']
        #with open('data/100_sample/gec_texts.csv', 'r') as f:
            #inputs = f.readlines()
            #inputs = [i.strip("\n") for i in inputs]
        prompts = advanced_gec_prompts
    else:
        raise ValueError(f"TASK should be 'Summarisation', 'Simplification' or 'GEC'. Got '{TASK}' instead.")

    results = {"model": [], "prompt": [], "temperature": [], "input": [], "original_input": [], "output": []}

    total_requests = 0
    for i, text_input in enumerate(inputs):
        print(f"INFERENCE ON SAMPLE {i} OF {len(inputs)}")
        for model_name in models_to_run:
            for prompt in prompts:
                for temperature in temperatures:
                    results['model'].append(model_name)
                    results['prompt'].append(prompt)
                    results['temperature'].append(temperature)
                    text = prompt.replace("[...]", text_input)
                    results['input'].append(text)
                    results['original_input'].append(text_input)
                    inference_not_done = True
                    while inference_not_done:
                        try:
                           
                            client = openai.OpenAI() 
                            response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                            {"role": "system", "content": "You are ChatGPT."},
                            {"role": "user", "content": text},
                            ],
                        temperature=temperature
                        )
                            inference_not_done = False
                        except Exception as e:  # pragmatic catch all exception is not ideal, but works well for now as
                            # we don't know which error OpenAI API will throw (it is still unstable and can throw many
                            # different errors). We retry after 10 minutes as often the OpenAI server will start
                            # working again
                            print(f"Waiting 10 minutes, current time: "
                                  f"{datetime.now(pytz.timezone('Europe/London')).isoformat()}")
                            print(f"Error was: {e}")
                            time.sleep(600)
                    results["output"].append(response.choices[0].message.content.strip("\n"))
                    total_requests += 1
                    if total_requests % 18 == 0:
                        time.sleep(150)  # to avoid reaching rate limit
        with open(f"data/outputs/models_output/output_openai_{TASK.lower()}_end.json", "w") as f:
            json.dump(results, f)
    df = pd.DataFrame.from_dict(results)
    df.to_csv(f"data/outputs/models_output/output_openai_{TASK.lower()}_end.csv", index=False)
