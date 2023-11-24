import subprocess
import sys
from functools import wraps
from typing import Callable, Optional

from flytekit.loggers import logger
from .constants import NO_ACTIVITY_TIMEOUT


def jupyter(
    _task_function: Optional[Callable] = None,
    no_activity_timeout: Optional[int] = NO_ACTIVITY_TIMEOUT,
    token: Optional[str] = "",
    port: Optional[int] = 8888,
    enable: Optional[bool] = True,
    notebook_dir: Optional[str] = "/root",
    pre_execute: Optional[Callable] = None,
    post_execute: Optional[Callable] = None,
):
    def wrapper(fn):
        if not enable:
            return fn

        @wraps(fn)
        def inner_wrapper(*args, **kwargs):
            print("jupyter decorator start")
            # 0. Executes the pre_execute function if provided.
            if pre_execute is not None:
                pre_execute()
                logger.info("Pre execute function executed successfully!")

            # 1. Launches and monitors the Jupyter Notebook server.
            # Run the function in the background
            logger.info("Start the jupyter notebook server...")
            cmd = f"jupyter notebook --port {port} --NotebookApp.token={token}"
            if notebook_dir:
                cmd += f" --notebook-dir={notebook_dir}"

            if no_activity_timeout:
                cmd += f" --NotebookApp.shutdown_no_activity_timeout={no_activity_timeout}"

            process = subprocess.Popen(cmd, shell=True)

            # 3. Wait for the process to finish
            process.wait()

            # 4. Exit after subprocess has finished
            if post_execute is not None:
                post_execute()
                logger.info("Post execute function executed successfully!")
            sys.exit()

        return inner_wrapper

    # for the case when the decorator is used without arguments
    if _task_function is not None:
        return wrapper(_task_function)
    # for the case when the decorator is used with arguments
    else:
        return wrapper
