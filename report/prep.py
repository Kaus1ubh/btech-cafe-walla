"""Write report_word.html: report.html with each <img> given its true height.
Word's HTML import keeps an image's original pixel height when only width is set."""
import pathlib, re
from PIL import Image

here = pathlib.Path(__file__).parent
src = (here / "report.html").read_text(encoding="utf-8")

def fix(m):
    path, width = m.group(1), int(m.group(2))
    w, h = Image.open(here / path).size
    return f'<img src="{path}" width="{width}" height="{round(width * h / w)}">'

out = re.sub(r'<img src="([^"]+)" width="(\d+)">', fix, src)
(here / "report_word.html").write_text(out, encoding="utf-8")
print("images sized:", len(re.findall(r"<img ", out)))
