import multiprocessing
import subprocess
import sys
import time
from functools import wraps
from typing import Callable, Optional

from flytekit.loggers import logger

from .constants import DEFAULT_UP_SECONDS


def execute_command(cmd):
    """
    Execute a command in the shell.
    """

    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logger.info(f"cmd: {cmd}")
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise RuntimeError(f"Command {cmd} failed with error: {stderr}")
    logger.info(f"stdout: {stdout}")
    logger.info(f"stderr: {stderr}")


def jupyter(
    _task_function: Optional[Callable] = None,
    server_up_seconds: Optional[int] = DEFAULT_UP_SECONDS,
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
            # 0. Executes the pre_execute function if provided.
            if pre_execute is not None:
                pre_execute()
                logger.info("Pre execute function executed successfully!")

            # 1. Launches and monitors the Jupyter Notebook server.
            # Run the function in the background
            logger.info(f"Start the server for {server_up_seconds} seconds...")
            cmd = f"jupyter notebook --port {port} --NotebookApp.token={token}"
            if notebook_dir:
                cmd += f" --notebook-dir={notebook_dir}"
            child_process = multiprocessing.Process(target=execute_command, kwargs={"cmd": cmd})

            child_process.start()
            time.sleep(server_up_seconds)

            # 2. Terminates the server after server_up_seconds
            logger.info(f"{server_up_seconds} seconds passed. Terminating...")
            if post_execute is not None:
                post_execute()
                logger.info("Post execute function executed successfully!")
            child_process.terminate()
            child_process.join()
            sys.exit(0)

        return inner_wrapper

    # for the case when the decorator is used without arguments
    if _task_function is not None:
        return wrapper(_task_function)
    # for the case when the decorator is used with arguments
    else:
        return wrapper
