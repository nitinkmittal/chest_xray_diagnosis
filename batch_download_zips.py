#!/usr/bin/env python3
# Download the 56 zip files in Images_png in batches
import urllib.request
from tqdm import tqdm
import os

from chest_xray_diagnosis import get_root_path

PROJECT_PATH = get_root_path()
SAVE_PATH = "data/xrays"

# create directory
os.makedirs(os.path.join(PROJECT_PATH, SAVE_PATH), exist_ok=True)

# URLs for the zip files
links = [
    "https://nihcc.box.com/shared/static/vfk49d74nhbxq3nqjg0900w5nvkorp5c.gz",
    "https://nihcc.box.com/shared/static/i28rlmbvmfjbl8p2n3ril0pptcmcu9d1.gz",
    "https://nihcc.box.com/shared/static/f1t00wrtdk94satdfb9olcolqx20z2jp.gz",
    "https://nihcc.box.com/shared/static/0aowwzs5lhjrceb3qp67ahp0rd1l1etg.gz",
    "https://nihcc.box.com/shared/static/v5e3goj22zr6h8tzualxfsqlqaygfbsn.gz",
    "https://nihcc.box.com/shared/static/asi7ikud9jwnkrnkj99jnpfkjdes7l6l.gz",
    "https://nihcc.box.com/shared/static/jn1b4mw4n6lnh74ovmcjb8y48h8xj07n.gz",
    "https://nihcc.box.com/shared/static/tvpxmn7qyrgl0w8wfh9kqfjskv6nmm1j.gz",
    "https://nihcc.box.com/shared/static/upyy3ml7qdumlgk2rfcvlb9k6gvqq2pj.gz",
    "https://nihcc.box.com/shared/static/l6nilvfa9cg3s28tqv1qc1olm3gnz54p.gz",
    "https://nihcc.box.com/shared/static/hhq8fkdgvcari67vfhs7ppg2w6ni4jze.gz",
    "https://nihcc.box.com/shared/static/ioqwiy20ihqwyr8pf4c24eazhh281pbu.gz",
]

for idx, url in enumerate(links):
    path = os.path.join(PROJECT_PATH, SAVE_PATH, f"images_{idx+1:02d}.tar.gz")
    print(
        f"Downloading {idx+1}/{len(links)}, "
        f"filename: {os.path.basename(path)}"
    )
    urllib.request.urlretrieve(url, path)  # download the zip file

print("Download complete. Please check the checksums")
