from dataclasses import dataclass


@dataclass
class ControlRow:
    control_id: str
    control_name: str
    answer: bool
    verdict: str | None
    compliant: bool
    observations: str | None


@dataclass
class GroupData:
    id: str
    name: str
    criticality: str | None
    rows: list[ControlRow]
