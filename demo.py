from pathlib import Path
from yggdrasil.utils.files import FileProperties

file1 = Path("demo.py")
file2 = Path("demo2.py")

fp = FileProperties(file1)
print(fp)


