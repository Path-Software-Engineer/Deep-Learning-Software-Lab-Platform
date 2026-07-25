"""Resources shared by every bounded context."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class StrictResource(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ErrorItemResource(StrictResource):
    field: str | None = None
    message: str


class ErrorResource(StrictResource):
    code: str
    message: str
    details: list[ErrorItemResource] = Field(default_factory=list)


class ErrorEnvelope(StrictResource):
    error: ErrorResource


class HealthResource(StrictResource):
    status: str
    service: str
    version: str
    artifact: str


class ModuleResource(StrictResource):
    id: str
    name: str
    description: str
    path: str
    status: str
    sprint: int


class ModulesResource(StrictResource):
    modules: list[ModuleResource]


def validation_details(errors: Sequence[Any]) -> list[ErrorItemResource]:
    return [
        ErrorItemResource(
            field=".".join(str(part) for part in error.get("loc", []) if part != "body") or None,
            message=str(error["msg"]),
        )
        for error in errors
    ]
