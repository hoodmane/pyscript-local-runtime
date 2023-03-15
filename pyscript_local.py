from pathlib import Path
import tomli
import micropip
from bs4 import BeautifulSoup
from importlib import metadata
import shutil
from pyodide.http import pyfetch
from asyncio import ensure_future, gather

async def download_wheel(url_path, target_path):
    wheel_url = url_path.read_text()
    wheel_name = wheel_url.rpartition("/")[-1]
    url_path.write_text(wheel_name)
    resp = await pyfetch(wheel_url)
    resp_buf = await resp.buffer()
    resp_buf.to_file(open(target_path / wheel_name, "w"))
    

async def process_html(html_file, target_dir):
    target_path = Path(target_dir)
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, features="html.parser")
    config = next(soup.find_all("py-config")[0].children)
    pkgs = tomli.loads(config)['packages']
    await micropip.install(pkgs)
    futs = []
    for d in metadata.distributions():
        url_path = d._path / "PYODIDE_URL"
        if not url_path.exists():
            continue
        futs.append(ensure_future(download_wheel(url_path, target_path)))
    await gather(*futs)

    (target_path / "repodata.json").write_text(micropip.freeze())
    for path in Path("/home/index").glob("*.whl"):
        shutil.copy(path, target_path)


