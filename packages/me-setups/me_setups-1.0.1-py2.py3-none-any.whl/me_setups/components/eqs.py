from __future__ import annotations

import subprocess
from io import TextIOWrapper

from me_setups.components import tools
from me_setups.components.comp import Component
from me_setups.components.tools import OSType


PROMPTS = {
    OSType.LINUX: b"# ",
    OSType.VOIS: b"VOiS>>",
    OSType.UBOOT: b"EyeQ5 # ",
}


class EyeQ5(Component):
    def __init__(
        self,
        name: str,
        port: str,
        os_type: OSType = OSType.LINUX,
        log_file: TextIOWrapper | None = None,
    ) -> None:
        super().__init__(name, port, log_file)
        self.os_type = os_type

    @property
    def chip(self) -> int:
        return int(self.name[-2])

    @property
    def mid(self) -> int:
        return int(self.name[-1])

    @property
    def prompt(self) -> bytes:
        return PROMPTS[self.os_type]

    @property
    def ip(self) -> str:
        ip = tools.get_eq_ip(self.name, self.os_type)
        assert ip
        return ip

    def run_ssh_cmd(
        self,
        cmd: str,
        timeout: float = 5,
    ) -> subprocess.CompletedProcess[str]:
        assert self.os_type == OSType.LINUX
        _cmd = [
            "ssh",
            "-o",
            "StrictHostKeyChecking=no",
            "-E",
            "/dev/null",
            f"root@{self.ip}",
        ]
        _cmd.append(cmd)
        self.logger.debug(f"[serial] running cmd: {' '.join(_cmd)!r}")
        return subprocess.run(
            _cmd,
            capture_output=True,
            timeout=timeout,
            text=True,
        )
