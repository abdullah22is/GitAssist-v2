"""Risk level definitions for Git commands."""

from enum import Enum


class RiskLevel(Enum):
    SAFE = 0
    CAUTION = 1
    DANGEROUS = 2
    BLOCKED = 3


def risk_to_string(level: RiskLevel) -> str:
    """Return a human-readable string for a risk level."""
    mapping = {
        RiskLevel.SAFE: "SAFE",
        RiskLevel.CAUTION: "CAUTION",
        RiskLevel.DANGEROUS: "DANGEROUS",
        RiskLevel.BLOCKED: "BLOCKED",
    }
    return mapping.get(level, "UNKNOWN")