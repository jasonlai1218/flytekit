import asyncio

from flytekit import FlyteContextManager, logger
from flytekit.sensor.base_sensor import BaseSensor


class FileSensor(BaseSensor):
    def __init__(self, name: str, timeout: int = 600, **kwargs):
        super().__init__(name=name, **kwargs)
        self.timeout = timeout

    async def poke(self, path: str) -> bool:
        file_access = FlyteContextManager.current_context().file_access
        fs = file_access.get_filesystem_for_path(path, asynchronous=True)
        try:
            if file_access.is_remote(path):
                return await asyncio.wait_for(fs._exists(path), timeout=self.timeout)
            return fs.exists(path)
        except asyncio.TimeoutError:
            logger.info(f"Timeout reached while checking for file at {path}")
            return False
