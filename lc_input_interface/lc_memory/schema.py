# lc_memory/schema.py

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional, Literal
from uuid import UUID, uuid4
from datetime import datetime


class Fact(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    subject: str
    predicate: str
    object: str
    state: Literal["active", "superseded", "contradicted", "uncertain"]
    session_id: str
    valid_from: datetime = Field(default_factory=datetime.utcnow)
    valid_until: Optional[datetime] = None
    source: str
    provenance: Optional[str] = None
    justification: Optional[str] = None
    replaces: List[UUID] = Field(default_factory=list)
    replaced_by: List[UUID] = Field(default_factory=list)

    # --- Field Validators ---

    @field_validator("subject", "predicate", "object")
    @classmethod
    def non_empty_strings(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("must be a non-empty string")
        return v

    @field_validator("replaces", "replaced_by", mode="before")
    @classmethod
    def ensure_uuid_list(cls, v):
        if not isinstance(v, list):
            raise TypeError("must be a list of UUIDs")
        for item in v:
            if not isinstance(item, UUID):
                raise ValueError("each item must be a valid UUID")
        return v

    # --- Model-level Validator ---

    @model_validator(mode="after")
    def check_validity_range(self) -> Fact:
        if self.valid_until and self.valid_until < self.valid_from:
            raise ValueError("valid_until must be after or equal to valid_from")
        return self

    # --- Methods ---

    @classmethod
    def from_dict(cls, data: dict) -> Fact:
        return cls(**data)

    def to_dict(self) -> dict:
        return self.model_dump()

    def mark_superseded(self, replacement_id: UUID):
        self.state = "superseded"
        self.replaced_by.append(replacement_id)

    def mark_contradicted(self, conflicting_id: UUID):
        self.state = "contradicted"
        self.replaced_by.append(conflicting_id)

    def is_active(self) -> bool:
        return self.state == "active"
