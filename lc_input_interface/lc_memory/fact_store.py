# lc_memory/fact_store.py

from typing import Dict, List, Set, Optional
from uuid import uuid4, UUID
from datetime import datetime

from lc_memory.schema import Fact


class FactStore:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.facts: Dict[UUID, Fact] = {}
        self.by_subject: Dict[str, Set[UUID]] = {}
        self.by_provenance: Dict[str, Set[UUID]] = {}
        self.by_state: Dict[str, Set[UUID]] = {}
        self.by_predicate: Dict[str, Set[UUID]] = {}

    def add_fact(self, subject, predicate, object, **metadata) -> UUID:
        fact_id = uuid4()
        valid_from = metadata.get("valid_from", datetime.utcnow())
        provenance = metadata.get("provenance")
        source = metadata.get("source", "FactStore")

        fact = Fact(
            id=fact_id,
            subject=subject,
            predicate=predicate,
            object=object,
            state="active",
            session_id=self.session_id,
            valid_from=valid_from,
            source=source,
            provenance=provenance,
            replaces=[],
            replaced_by=[],
            metadata=metadata
        )

        self.facts[fact_id] = fact
        self.by_subject.setdefault(subject, set()).add(fact_id)
        if provenance:
            self.by_provenance.setdefault(provenance, set()).add(fact_id)
        self.by_state.setdefault(fact.state, set()).add(fact_id)
        self.by_predicate.setdefault(predicate, set()).add(fact_id)
        return fact_id

    def get_facts(self, subject=None, predicate=None, state=None, provenance=None) -> List[Fact]:
        result_ids = set(self.facts.keys())
        if subject:
            result_ids &= self.by_subject.get(subject, set())
        if predicate:
            result_ids &= self.by_predicate.get(predicate, set())
        if state:
            result_ids &= self.by_state.get(state, set())
        if provenance:
            result_ids &= self.by_provenance.get(provenance, set())
        return [self.facts[fid] for fid in result_ids]

    def overwrite_fact(self, old_id, subject, predicate, object, justification, **metadata):
        new_id = self.add_fact(subject, predicate, object, **metadata)
        new_fact = self.facts[new_id]

        old_fact = self.facts[old_id]
        old_fact.state = "superseded"
        old_fact.replaced_by.append(new_id)
        new_fact.replaces.append(old_id)

        self.by_state["active"].discard(old_id)
        self.by_state.setdefault("superseded", set()).add(old_id)
        return new_id

    def get_lineage(self, fact_id) -> Dict:
        fact = self.facts[fact_id]
        return {
            "replaces": fact.replaces,
            "replaced_by": fact.replaced_by,
            "state": fact.state
        }

    def resolve_contradictions(self, subject, predicate=None) -> List[Fact]:
        candidates = self.get_facts(subject=subject)
        if predicate:
            candidates = [f for f in candidates if f.predicate == predicate]
        return [f for f in candidates if f.state != "superseded"]

    def delete_facts_by_provenance(self, provenance_tag: str):
        ids_to_delete = self.by_provenance.get(provenance_tag, set()).copy()
        for fid in ids_to_delete:
            fact = self.facts.pop(fid, None)
            if not fact:
                continue
            self.by_subject.get(fact.subject, set()).discard(fid)
            self.by_state.get(fact.state, set()).discard(fid)
            self.by_predicate.get(fact.predicate, set()).discard(fid)
        self.by_provenance.pop(provenance_tag, None)

    def export_session(self, session_id) -> List[Fact]:
        if session_id != self.session_id:
            return []
        return list(self.facts.values())
