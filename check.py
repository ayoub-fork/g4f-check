# https://github.com/3571303/g4f-check
# License: AGPL-3.0


import sys
import g4f
import threading
import time

def process_provider(pname, results):
    try:
        print(f"[TRYING]:  {pname}")
        start_time = time.time()
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            provider=getattr(getattr(getattr(sys.modules[__name__], "g4f"), "Provider"), pname),
            messages=[{"role": "user", "content": "Hello"}],
        )
        end_time = time.time()
        results.append((pname, end_time - start_time))
        print(f"[WORKING]: {pname}, Time taken: {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"[BROKEN]:  {pname}, Error: {str(e)}")

providers = g4f.Provider.__all__

results = []
threads = []
for pname in providers:
    thread = threading.Thread(target=process_provider, args=(pname, results))
    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()


# Display a summary of working providers
print("====== WORKING PROVIDERS ======")
for pname, time_taken in results:
    print(f"{pname:<20} {time_taken:.2f}s")
