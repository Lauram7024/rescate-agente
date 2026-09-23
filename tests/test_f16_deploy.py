import re
from pathlib import Path

DOCKERFILE = Path(__file__).resolve().parent.parent / "Dockerfile"


def test_dockerfile_listo_para_cloud():
    d = DOCKERFILE.read_text(encoding="utf-8")
    assert not re.search(r"sk-[A-Za-z0-9-]{20,}", d), "hay un secreto en la imagen"
    assert re.search(r"^\s*HEALTHCHECK\s", d, re.M), "falta HEALTHCHECK"
    users = re.findall(r"^\s*USER\s+(\S+)", d, re.M)
    assert users and users[-1] not in ("root", "0"), "el contenedor corre como root"
