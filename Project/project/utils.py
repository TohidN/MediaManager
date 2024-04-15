def get_or_create_dir(path):
    from pathlib import Path

    Path(path).mkdir(parents=True, exist_ok=True)


def download(url, path):
    # Download with progressbar
    import math
    import requests
    from tqdm.auto import tqdm

    r = requests.get(url, stream=True, allow_redirects=True)
    total_size = int(r.headers.get("content-length", 0))
    block_size = 1024
    with open(path, "wb") as f:
        for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size // block_size), unit="KB", unit_scale=True, desc=f"Downloading `{url}`"):
            f.write(data)


def download_clean(url, path):
    # Clean download
    import requests

    r = requests.get(url, allow_redirects=True)
    open(path, "wb").write(r.content)


    
def get_file_lines_count(file_path):
    import mmap
    with open(file_path, "r+") as fp:
        buf = mmap.mmap(fp.fileno(), 0)
        lines = 0
        while buf.readline():
            lines += 1
        return lines