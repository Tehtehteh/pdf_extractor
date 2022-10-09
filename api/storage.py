import os
from typing import Protocol, BinaryIO, runtime_checkable
from uuid import uuid4


@runtime_checkable
class IStorage(Protocol):
    def save(self, binary_io: bytes, file_name: str) -> str:
        ...

    def get(self, file_uri: str) -> BinaryIO:
        ...


class LocalStorage(IStorage):

    def __init__(self, **kwargs):
        self.local_dir: str = kwargs['local_dir']

    def save(self, binary_io: bytes, file_name: str) -> str:
        file_uuid = uuid4()
        target_file_name = os.path.join(self.local_dir, f'{str(file_uuid)}_{file_name}')
        with open(target_file_name, 'wb') as handle:
            handle.write(binary_io)
        return target_file_name

    def get(self, file_uri: str) -> BinaryIO:
        with open(file_uri, 'rb') as handle:
            return handle
