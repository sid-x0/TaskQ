import time


def execute(payload: dict):
    seconds = payload["seconds"]

    print(f"Sleeping for {seconds} seconds...")

    time.sleep(seconds)

    print(" Sleep complete.")