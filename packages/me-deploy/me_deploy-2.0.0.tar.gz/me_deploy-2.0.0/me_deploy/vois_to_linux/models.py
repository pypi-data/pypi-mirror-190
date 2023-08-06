from __future__ import annotations

import pathlib
from dataclasses import dataclass
from typing import Any


@dataclass
class Component:
    version: str
    hash: str
    signature: str
    type: str
    id: str
    filename: str


@dataclass
class FotaManifest:
    FOTA_version: str
    components: list[Component]
    manifest_version: int

    def __init__(
        self,
        *,
        FOTA_version: str,
        components: list[Any],
        manifest_version: int,
    ) -> None:
        self.FOTA_version = FOTA_version
        self.components = [Component(**d) for d in components]
        self.manifest_version = manifest_version


@dataclass
class Action:
    part: str
    hash: str
    offset: str
    action: str
    file_name: str
    type: str
    file_type: int | None = None
    protocol: str | None = None


@dataclass
class AgentManifest:
    FOTA_version: str
    actions: list[Action]
    manifest_version: int

    def __init__(
        self,
        *,
        FOTA_version: str,
        actions: list[Any],
        manifest_version: int,
    ) -> None:
        self.FOTA_version = FOTA_version
        self.actions = [Action(**d) for d in actions]
        self.manifest_version = manifest_version


@dataclass
class Args:
    eqs: list[str]
    mcu_type: str
    tftp_folder: pathlib.Path
    log_folder: pathlib.Path
    zip_image_path: pathlib.Path
    board_name: str
    board_rev: str
