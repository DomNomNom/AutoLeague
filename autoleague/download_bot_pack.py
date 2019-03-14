import urllib.request
import zipfile
import tempfile
import shutil

from pathlib import Path

from autoleague.paths import WorkingDir


def download_bot_pack(
        working_dir: WorkingDir,
        download_url: str="https://drive.google.com/uc?export=download&id=1OOisnGpxD48x_oAOkBmzqNdkB5POQpiV"
    ):
    """
    Ensures that the bots in the working directory are up to date with the RLBot .
    See https://docs.google.com/document/d/10uCWwHDQYJGMGeoaW1pZu1KvRnSgm064oWL2JVx4k4M/edit?usp=sharing
    To learn how the bot pack file is hosted and maintained.
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        zip_path = Path(tmpdirname) / "RLBotPack.zip"
        urllib.request.urlretrieve(download_url, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            shutil.rmtree(working_dir.bot_pack)
            zip_ref.extractall(working_dir.bot_pack)
