import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Union


@dataclass
class DownloadConfig:
    """Configuration for our cached path manager.

    Attributes:
        cache_dir (:obj:`str` or :obj:`Path`, optional): Specify a cache directory to save the file to (overwrite the
            default cache dir).
        force_download (:obj:`bool`, default ``False``): If True, re-dowload the file even if it's already cached in
            the cache dir.
        resume_download (:obj:`bool`, default ``False``): If True, resume the download if incompletly recieved file is
            found.
        proxies (:obj:`dict`, optional):
        user_agent (:obj:`str`, optional): Optional string or dict that will be appended to the user-agent on remote
            requests.
        extract_compressed_file (:obj:`bool`, default ``False``): If True and the path point to a zip or tar file,
            extract the compressed file in a folder along the archive.
        force_extract (:obj:`bool`, default ``False``): If True when extract_compressed_file is True and the archive
            was already extracted, re-extract the archive and override the folder where it was extracted.
        delete_extracted (:obj:`bool`, default ``False``): Whether to delete (or keep) the extracted files.
        use_etag (:obj:`bool`, default ``True``): Whether to use the ETag HTTP response header to validate the cached files.
        num_proc (:obj:`int`, optional): The number of processes to launch to download the files in parallel.
        max_retries (:obj:`int`, default ``1``): The number of times to retry an HTTP request if it fails.
        use_auth_token (:obj:`str` or :obj:`bool`, optional): Optional string or boolean to use as Bearer token
            for remote files on the Datasets Hub. If True, will get token from ~/.huggingface.
        ignore_url_params (:obj:`bool`, default ``False``): Whether to strip all query parameters and #fragments from
            the download URL before using it for caching the file.
        download_desc (:obj:`str`, optional): A description to be displayed alongside with the progress bar while downloading the files.
    """

    cache_dir: Optional[Union[str, Path]] = None
    force_download: bool = False
    resume_download: bool = False
    local_files_only: bool = False
    proxies: Optional[Dict] = None
    user_agent: Optional[str] = None
    extract_compressed_file: bool = False
    force_extract: bool = False
    delete_extracted: bool = False
    use_etag: bool = True
    num_proc: Optional[int] = None
    max_retries: int = 1
    use_auth_token: Optional[Union[str, bool]] = None
    ignore_url_params: bool = False
    download_desc: Optional[str] = None

    def copy(self) -> "DownloadConfig":
        return self.__class__(**{k: copy.deepcopy(v) for k, v in self.__dict__.items()})
