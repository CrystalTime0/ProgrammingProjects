import time
from rich.progress import track

for i in track(range(50), description="Processing..."):
    time.sleep(0.01)  # Simulate work being done