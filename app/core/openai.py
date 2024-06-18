import time
from openai import OpenAI
from app.settings import OPENAI_API_KEY

client : OpenAI = OpenAI(api_key=OPENAI_API_KEY)


def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
        print("Pending..")
    print("complete")