from uuid import UUID, uuid4
from datetime import datetime, timedelta
from pydantic import ValidationError

from lc_memory.schema import Fact


def test_fact_creation_defaults():
    print("Test: Fact creation with defaults...")
    fact = Fact(
        subject="Nyxie",
        predicate="is",
        object="a cat",
        state="active",
        session_id="sess-001",
        source="unit_test",
        provenance="manual"
    )
    assert isinstance(fact.id, UUID)
    assert fact.valid_from is not None
    assert fact.is_active() is True
    print("✅ Passed")


def test_fact_serialization_roundtrip():
    print("Test: Fact serialization roundtrip...")
    fact = Fact(
        subject="Test Subject",
        predicate="has",
        object="an object",
        state="active",
        session_id="sess-002",
        source="unit_test",
        provenance="manual"
    )
    data = fact.to_dict()
    fact2 = Fact.from_dict(data)
    assert fact == fact2
    print("✅ Passed")


def test_fact_state_transitions():
    print("Test: Fact state transitions...")
    fact = Fact(
        subject="Entity",
        predicate="exists",
        object="true",
        state="active",
        session_id="sess-003",
        source="unit_test",
        provenance="manual"
    )
    replacement_id = uuid4()
    fact.mark_superseded(replacement_id)
    assert fact.state == "superseded"
    assert replacement_id in fact.replaced_by

    contradiction_id = uuid4()
    fact.mark_contradicted(contradiction_id)
    assert fact.state == "contradicted"
    assert contradiction_id in fact.replaced_by
    print("✅ Passed")


def test_fact_from_invalid_data_raises():
    print("Test: Invalid fact input raises error...")

    try:
        Fact(
            subject="",
            predicate="is",
            object="invalid",
            state="active",
            session_id="sess-004",
            source="test",
            provenance="test"
        )
        raise AssertionError("Expected ValidationError for empty subject")
    except ValidationError as e:
        assert "non-empty string" in str(e)

    try:
        Fact(
            subject="Valid",
            predicate="is",
            object="wrong",
            state="active",
            session_id="sess-005",
            source="test",
            provenance="test",
            valid_from=datetime.utcnow(),
            valid_until=datetime.utcnow() - timedelta(days=1)
        )
        raise AssertionError("Expected ValidationError for date range")
    except ValidationError as e:
        assert "valid_until must be after" in str(e)

    print("✅ Passed")


if __name__ == "__main__":
    test_fact_creation_defaults()
    test_fact_serialization_roundtrip()
    test_fact_state_transitions()
    test_fact_from_invalid_data_raises()
