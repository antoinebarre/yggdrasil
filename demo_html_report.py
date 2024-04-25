from pathlib import Path
from yggdrasil.html.fake_report import create_fake_report

from yggdrasil.utils.files import delete_folder


target_dir = Path("work/temp")
filename = "fake_report.html"

# delete the target directory if it exists
if target_dir.exists():
    delete_folder(target_dir)

# # create the fake report
md = create_fake_report(target_dir / filename)
