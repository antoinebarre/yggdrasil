



from pathlib import Path

from yggdrasil.utils.files.handling import delete_folder
from yggdrasil.markdown.fake_report import create_markdown_report

target_dir = Path("work/temp_md")
filename = "fake_report.md"

# delete the target directory if it exists
if target_dir.exists():
    delete_folder(target_dir)

# # create the fake report
md = create_markdown_report(target_dir / filename)
print(md)