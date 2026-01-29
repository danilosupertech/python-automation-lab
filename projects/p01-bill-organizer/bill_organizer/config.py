from dataclasses import dataclass
from typing import Dict, List

@dataclass(frozen=True)
class Rules:
    """Filename-based matching rules."""
    suppliers: Dict[str, List[str]]

DEFAULT_RULES = Rules(
    suppliers={
        "edp": ["edp", "energia", "electricidade"],
        "meo": ["meo", "telecom", "fibra", "internet"],
        "aguas": ["agua", "águas", "aguas", "smas"],
        "condominio": ["condominio", "condomínio", "quota", "admin"],
        "outros": [],
    }
)
