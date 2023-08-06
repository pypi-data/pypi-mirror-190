from typing import List

from beam.base import AbstractDataLoader
from beam.serializer import VolumeConfiguration
from beam.types import MountType


class MountManager(AbstractDataLoader):
    def __init__(self) -> None:
        self.persistent_volumes: List[VolumeConfiguration] = []
        self.shared_volumes: List[VolumeConfiguration] = []

    def PersistentVolume(self, name: str, app_path: str, **_):
        self.persistent_volumes.append(
            VolumeConfiguration(
                name=name,
                local_path=None,
                app_path=app_path,
                mount_type=MountType.Persistent,
            )
        )

    def SharedVolume(self, name: str, app_path: str, **_):
        self.shared_volumes.append(
            VolumeConfiguration(
                name=name,
                local_path=None,
                app_path=app_path,
                mount_type=MountType.Shared,
            )
        )

    def dumps(self):
        return [
            *[pv.validate_and_dump() for pv in self.persistent_volumes],
            *[sv.validate_and_dump() for sv in self.shared_volumes],
        ]

    def from_config(self, mounts: List[dict]):
        if mounts is None:
            return

        for m in mounts:
            if m.get("mount_type") == MountType.Persistent:
                self.PersistentVolume(**m)

            elif m.get("mount_type") == MountType.Shared:
                self.SharedVolume(**m)
