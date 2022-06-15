import asyncio


class LockStack:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._stack = []

    async def append(self, item: any):
        async with self._lock:
            self._stack.append(item)

    async def pop_all(self):
        async with self._lock:
            r, self._stack[:] = self._stack[:], []
        return r

    def length(self):
        return len(self._stack)
