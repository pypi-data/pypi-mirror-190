import concurrent.futures
from tqdm import tqdm
from brevettiai.io import io_tools


def _download_file(source, callback, io, **kwargs):
    content = io.read_file(source, **kwargs)
    if callback is not None:
        return callback(source, content)
    else:
        return content


def load_files(paths, callback, io=io_tools, monitor=True, tqdm_args=None, **kwargs):
    """Download multiple files at once"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(_download_file, src, callback=callback, io=io, **kwargs) for src in paths]

        if monitor:
            futures = tqdm(futures, **(tqdm_args or {}))

        for f in futures:
            yield f.result()
