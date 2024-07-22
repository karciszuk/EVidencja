from pathlib import Path
import os

print(Path(os.path.abspath(__file__)).stem)