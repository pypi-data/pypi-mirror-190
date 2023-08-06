# TODO: quote whitespace, line escapes, directives, type for image references, arg type with defaults

from __future__ import annotations

import functools
import json
import signal
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable

DEFAULT_SYNTAX = "docker.io/docker/dockerfile:experimental"
DEFAULT_ESCAPE = "\\"
DEFAULT_BASE_IMAGE = "scratch"
DEFAULT_PLATFORM = "$TARGETPLATFORM"
DEFAULT_MOUNT_SOURCE_PATH = Path("/")
DEFAULT_CACHE_MOUNT_SHARING = "shared"
DEFAULT_SECRET_MOUNT_TARGET_ROOT = Path("/run/secrets/")
DEFAULT_CACHE_MOUNT_MODE = 0o755
DEFAULT_SECRET_MOUNT_MODE = 0o400
DEFAULT_SSH_MOUNT_ID = "default"
# TODO: Is this a literal ${N} that is expanded by docker?
DEFAULT_SSH_MOUNT_TARGET = Path("/run/buildkit/ssh_agent.${N}")
DEFAULT_STOP_SIGNAL = signal.SIGTERM
DEFAULT_HEALTH_CHECK_INTERVAL = 30
DEFAULT_HEALTH_CHECK_TIMEOUT = 30
DEFAULT_HEALTH_CHECK_START_PERIOD = 0
DEFAULT_HEALTH_CHECK_RETRIES = 3


class Renderable(ABC):
    @abstractmethod
    def render(self) -> str:
        """Render this item into the dockerfile."""


class Instruction(Renderable):
    pass


class Mount(Renderable):
    pass


@dataclass
class BindMount(Mount):
    target: Path
    source: Path = DEFAULT_MOUNT_SOURCE_PATH
    from_: str | None = None
    # TODO: Is this confusing that this is ro by default, but cache mounts are rw?
    readwrite: bool = False

    def render(self) -> str:
        parts = ["type=bind", f"target={self.target}", f"source={self.source}"]
        if self.from_:
            parts.append(f"from={self.from_}")
        if self.readwrite:
            parts.append(f"rw")
        return ",".join(parts)


@dataclass
class CacheMount(Mount):
    target: Path
    id_: str | None = None
    readonly: bool = False
    sharing: str = DEFAULT_CACHE_MOUNT_SHARING
    from_: str | None = None
    source: Path = DEFAULT_MOUNT_SOURCE_PATH
    mode: int = DEFAULT_CACHE_MOUNT_MODE
    uid: int = 0
    gid: int = 0

    def render(self) -> str:
        parts = [
            "type=cache",
            f"target={self.target}",
            f"sharing={self.sharing}",
            f"source={self.source}",
            f"mode=0{self.mode:o}",
            f"uid={self.uid}",
            f"gid={self.gid}",
        ]
        if self.from_:
            parts.append(f"from={self.from_}")
        if self.readonly:
            parts.append(f"ro")
        return ",".join(parts)


@dataclass
class TmpfsMount(Mount):
    target: Path
    size: int

    def render(self) -> str:
        parts = [
            "type=tmpfs",
            f"target={self.target}",
            f"size={self.size}",
        ]
        return ",".join(parts)


@dataclass
class SecretMount(Mount):
    id_: str | None = None
    target: Path | None = None
    required: bool = False
    mode: int = DEFAULT_SECRET_MOUNT_MODE
    uid: int = 0
    gid: int = 0

    def render(self) -> str:
        # TODO: Figure out a more ergonomic way to do this
        if not self.id_ and not self.target:
            raise RuntimeError("At least one of id or target must be specified")
        id_ = self.id_ or self.target.name
        target = self.target or DEFAULT_SECRET_MOUNT_TARGET_ROOT / id_
        parts = [
            "type=secret",
            f"id={id_}",
            f"target={target}",
            f"mode=0{self.mode:o}",
            f"uid={self.uid}",
            f"gid={self.gid}",
        ]
        if self.required:
            parts.append("required")
        return ",".join(parts)


@dataclass
class SshMount(Mount):
    id_: str = DEFAULT_SSH_MOUNT_ID
    target: Path | None = None
    required: bool = False
    mode: int = DEFAULT_SECRET_MOUNT_MODE
    uid: int = 0
    gid: int = 0

    def render(self) -> str:
        # TODO: Figure out a more ergonomic way to do this
        target = self.target or DEFAULT_SSH_MOUNT_TARGET
        parts = [
            "type=ssh",
            f"id={self.id_}",
            f"target={target}",
            f"mode=0{self.mode:o}",
            f"uid={self.uid}",
            f"gid={self.gid}",
        ]
        if self.required:
            parts.append("required")
        return ",".join(parts)


class Network(Enum):
    DEFAULT = "default"
    NONE = "none"
    HOST = "host"


class Security(Enum):
    INSECURE = "insecure"
    SANDBOX = "sandbox"


@dataclass
class RunInstruction(Instruction):
    mounts: list(Mount) = field(default_factory=list)
    network: Network = Network.DEFAULT
    security: Security = Security.SANDBOX
    command: str | list(str) = field(default_factory=list)

    def render(self) -> str:
        parts = ["RUN"]
        parts.extend(f"--mount={mount.render()}" for mount in self.mounts)
        parts.append(f"--network={self.network.value}")
        parts.append(f"--security={self.network.value}")
        if isinstance(self.command, str):
            parts.append(self.command)
        else:
            parts.append(json.dumps(self.command))
        return " ".join(parts)


@dataclass
class CmdInstruction(Instruction):
    command: str | list(str) = field(default_factory=list)

    def render(self) -> str:
        parts = ["CMD"]
        if isinstance(self.command, str):
            parts.append(self.command)
        else:
            # TODO: Is this the right escape?
            parts.append(json.dumps(self.command))
        return " ".join(parts)


@dataclass
class LabelInstruction(Instruction):
    labels: dict(str, str) = field(default_factory=dict)

    def render(self) -> str:
        if not self.labels:
            return ""
        parts = ["LABEL"]
        parts.extend(f"{key}={value}" for key, value in self.labels.items())
        return " ".join(parts)


class Protocol(Enum):
    TCP = "tcp"
    UDP = "udp"


@dataclass
class ExposeInstruction(Instruction):
    port: int
    protocol: Protocol = Protocol.TCP

    def render(self) -> str:
        return f"{self.port}/{self.protocol.value}"


@dataclass
class EnvInstruction(Instruction):
    env: dict(str, str) = field(default_factory=dict)

    def render(self) -> str:
        if not self.env:
            return ""
        parts = ["ENV"]
        parts.extend(f"{key}={value}" for key, value in self.env.items())
        return " ".join(parts)


@dataclass
class AddInstruction(Instruction):
    # TODO: Add labs features (checksum, git)
    src: str | Path
    dest: Path
    # TODO: Make consistent with mount uid/gid?
    user: str | int = 0
    group: str | int = 0
    link: bool = False

    def render(self) -> str:
        parts = ["ADD", f"--chown={self.user}:{self.group}"]
        if self.link:
            parts.append("--link")
        parts.extend([f"{self.src}", f"{self.dest}"])
        return " ".join(parts)


@dataclass
class CopyInstruction(Instruction):
    src: str | Path
    dest: Path
    from_: str | None = None
    user: str | int = 0
    group: str | int = 0
    link: bool = False

    def render(self) -> str:
        parts = ["ADD", f"--chown={self.user}:{self.group}"]
        if self.from_:
            parts.append(f"--from={self.from_}")
        if self.link:
            parts.append("--link")
        parts.extend([f"{self.src}", f"{self.dest}"])
        return " ".join(parts)


@dataclass
class EntrypointInstruction(Instruction):
    entrypoint: str | list(str) = field(default_factory=list)

    def render(self) -> str:
        parts = ["ENTRYPOINT"]
        if isinstance(self.entrypoint, str):
            parts.append(self.entrypoint)
        else:
            # TODO: Is this the right escape?
            parts.append(json.dumps(self.entrypoint))
        return " ".join(parts)


@dataclass
class VolumeInstruction(Instruction):
    volumes: str | list(str) = field(default_factory=list)

    def render(self) -> str:
        parts = ["VOLUME"]
        if isinstance(self.volumes, str):
            parts.append(self.volumes)
        else:
            # TODO: Is this the right escape?
            parts.append(json.dumps(self.volumes))
        return " ".join(parts)


@dataclass
class UserInstruction(Instruction):
    user: int | str
    group: int | str | None

    def render(self) -> str:
        parts = ["USER"]
        if self.group is None:
            parts.append(f"{self.user}")
        else:
            parts.append(f"{self.user}:{self.group}")
        return " ".join(parts)


@dataclass
class WorkdirInstruction(Instruction):
    workdir: Path

    def render(self) -> str:
        parts = ["WORKDIR", f"{self.workdir}"]
        return " ".join(parts)


@dataclass
class ArgInstruction(Instruction):
    name: str
    default_value: str | None = None

    def render(self) -> str:
        parts = ["ARG"]
        if self.default_value is None:
            parts.append(f"{self.name}")
        else:
            parts.append(f"{self.name}={self.default_value}")
        return " ".join(parts)


@dataclass
class OnBuildInstruction(Instruction):
    inner: Instruction

    def render(self) -> str:
        parts = ["ONBUILD", self.inner.render()]
        return " ".join(parts)


@dataclass
class StopSignalInstruction(Instruction):
    signal: int | str | signal.signal = DEFAULT_STOP_SIGNAL

    def render(self) -> str:
        parts = ["STOPSIGNAL", f"{self.signal}"]
        return " ".join(parts)


@dataclass
class HealthCheckInstruction(Instruction):
    command: str | list(str) | None
    interval: int = DEFAULT_HEALTH_CHECK_INTERVAL
    timeout: int = DEFAULT_HEALTH_CHECK_TIMEOUT
    start_period: int = DEFAULT_HEALTH_CHECK_START_PERIOD
    retries: int = DEFAULT_HEALTH_CHECK_RETRIES

    def render(self) -> str:
        if self.command is None:
            parts = ["HEALTHCHECK", "NONE"]
        else:
            parts = [
                "HEALTHCHECK",
                f"--interval={self.interval}",
                "--timeout={self.timeout}",
                "--start-period=${self.start_period}",
                "--retries={self.retries}",
                "CMD",
            ]
            if isinstance(self.command, str):
                parts.append(self.command)
            else:
                # TODO: Is this the right escape?
                parts.append(json.dumps(self.command))
        return " ".join(parts)


@dataclass
class ShellInstruction(Instruction):
    shell: str | list(str) = field(default_factory=list)

    def render(self) -> str:
        parts = ["SHELL"]
        if isinstance(self.shell, str):
            parts.append(self.shell)
        else:
            # TODO: Is this the right escape?
            parts.append(json.dumps(self.shell))
        return " ".join(parts)


@dataclass
class Stage(Renderable):
    from_: str = DEFAULT_BASE_IMAGE
    platform: str = DEFAULT_PLATFORM
    alias: str | None = None
    instructions: list(Instruction) = field(default_factory=list)

    def _from_instruction(self) -> str:
        parts = ["FROM", f"--platform={self.platform}", self.from_]
        if self.alias:
            parts.extend(["AS", self.alias])
        return " ".join(parts)

    def render(self) -> str:
        parts = [self._from_instruction()]
        parts.extend(inst.render() for inst in self.instructions)
        return "\n".join(parts)


@dataclass
class Image(Renderable):
    stages: dict(str, Stage | tuple[Stage, Callable[[Stage], None]]) = field(
        default_factory=dict
    )
    syntax: str = DEFAULT_SYNTAX
    escape: str = DEFAULT_ESCAPE
    directives: dict(str, str) = field(default_factory=dict)
    build_args: list[ArgInstruction] = field(default_factory=list)

    default_stage: str | None = None

    def render(self) -> str:
        parts = [f"# syntax={self.syntax}", f"# escape={self.escape}"]
        # TODO: Escapes
        parts.extend(f"# {name}={value}" for name, value in self.directives.items())
        parts.extend(inst.render() for inst in self.build_args)
        # TODO: Topographical sort of images
        for stage in self.stages.values():
            if isinstance(stage, Stage):
                parts.append(stage.render())
            else:
                stage, func = stage
                func(stage)
                parts.append(stage.render())
        return "\n".join(parts)

    def stage(
        self,
        from_: str = DEFAULT_BASE_IMAGE,
        platform: str = DEFAULT_PLATFORM,
        alias: str | None = None,
    ):
        def wrapper(func):
            stage = Stage(from_=from_, platform=platform, alias=alias)
            # TODO: Check for conflicting aliases, maybe introduce mapping to deconflict
            self.stages[func.__name__] = (stage, func)
            self.default_stage = func.__name__

        return wrapper
