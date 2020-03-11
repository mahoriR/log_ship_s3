from collections import namedtuple
from pathlib import Path
from datetime import datetime, timedelta

FileNamePathDir=namedtuple('FileNamePathDir', ('name', 'path', 'dir'))

def find_files_in_dir(base_dir_abs_path_str:str, days_since_last_modified:int, current_datetime=None) -> FileNamePathDir:
    """
    returns list of files that were not modified in days_since_last_modified num days
    """
    if not current_datetime:
        current_datetime=datetime.now()
    ts_cutoff = (current_datetime.now()-timedelta(days=days_since_last_modified)).timestamp()
    filtered_files=filter(lambda f: (f.is_file() and (f.stat().st_mtime < ts_cutoff)), Path(base_dir_abs_path_str).iterdir())
    return [FileNamePathDir(f.name, str(f), base_dir_abs_path_str) for f in filtered_files]
