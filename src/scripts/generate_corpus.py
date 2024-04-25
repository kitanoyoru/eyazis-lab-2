import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import openai
from openai import OpenAI, OpenAIError

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PATH_TO_DATA = os.path.join(CURRENT_DIR, "..", "data")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

num_prompts = 100
num_threads = 8

prompt = (
    "Можешь написать небольшой рассказ про какое-либо животное (где-то 15 предложений)?"
)


def execute(prompt_id: int) -> None:
    try:
        completion = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        response_content = completion.choices[0].message.content

        filename = f"story_{prompt_id}.txt"
        with open(os.path.join(PATH_TO_DATA, filename), "w+") as file:
            file.write(response_content)

        logging.info(f"Prompt {prompt_id}: Response saved to {filename}")

    except OpenAIError as e:
        logging.error(f"Error in generating data for Prompt {prompt_id}: {str(e)}")


if __name__ == "__main__":
    logging.info(
        f"Starting data generation for {num_prompts} prompts using {num_threads} threads."
    )

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for id in range(num_prompts):
            futures.append(executor.submit(execute, prompt_id=id))
        for future in as_completed(futures):
            future.result()

    logging.info("Data generation completed.")
