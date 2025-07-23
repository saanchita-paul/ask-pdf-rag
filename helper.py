import os
import time

# clean old logs
def cleanup_old_logs(directory: str, max_age_seconds: int = 3600):
    now = time.time()
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            file_age = now - os.path.getmtime(filepath)
            if file_age > max_age_seconds:
                try:
                    os.remove(filepath)
                    print(f"Deleted old log: {filename}")
                except Exception as e:
                    print(f"Error deleting {filename}: {e}")