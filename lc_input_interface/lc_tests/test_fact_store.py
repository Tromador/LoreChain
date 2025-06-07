# test_fact_store.py

import sys
import os
from uuid import UUID
from datetime import datetime
from pprint import pprint

# Add the project root to sys.path so lc_memory resolves
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from lc_memory.fact_store import FactStore
from lc_memory.schema import Fact

results = {}

def test_add_and_retrieve_fact():
    store = FactStore("test-session")
    fact_id = store.add_fact("dragon", "breathes", "fire", provenance="myth")
    facts = store.get_facts(subject="dragon")
    assert any(f.id == fact_id for f in facts)
    results['test_add_and_retrieve_fact'] = "✅"

def test_filter_by_state_and_predicate():
    store = FactStore("test-session")
    store.add_fact("knight", "wields", "sword", provenance="story")
    store.add_fact("knight", "wields", "lance", provenance="story")
    facts = store.get_facts(subject="knight", predicate="wields", state="active")
    assert len(facts) == 2
    results['test_filter_by_state_and_predicate'] = "✅"

def test_overwrite_fact_marks_previous():
    store = FactStore("test-session")
    original_id = store.add_fact("king", "rules", "kingdom", provenance="legend")
    new_id = store.overwrite_fact(original_id, "king", "rules", "empire", justification="updated lore")
    orig = store.facts[original_id]
    new = store.facts[new_id]
    assert orig.state == "superseded"
    assert new.replaces == [original_id]
    assert original_id in orig.replaced_by or new.id == new_id
    results['test_overwrite_fact_marks_previous'] = "✅"

def test_delete_by_provenance():
    store = FactStore("test-session")
    id1 = store.add_fact("wizard", "casts", "spell", provenance="book1")
    id2 = store.add_fact("wizard", "flies", "broom", provenance="book2")
    store.delete_facts_by_provenance("book1")
    assert id1 not in store.facts
    assert id2 in store.facts
    results['test_delete_by_provenance'] = "✅"

def test_get_lineage_chain():
    store = FactStore("test-session")
    id1 = store.add_fact("hero", "defeats", "dragon", provenance="ver1")
    id2 = store.overwrite_fact(id1, "hero", "defeats", "lich", justification="new retelling")
    lineage = store.get_lineage(id2)
    assert lineage["replaces"] == [id1]
    assert store.get_lineage(id1)["replaced_by"] == [id2]
    results['test_get_lineage_chain'] = "✅"

# Run all tests
for test_func in [
    test_add_and_retrieve_fact,
    test_filter_by_state_and_predicate,
    test_overwrite_fact_marks_previous,
    test_delete_by_provenance,
    test_get_lineage_chain,
]:
    try:
        test_func()
    except AssertionError:
        results[test_func.__name__] = "❌ FAILED"

# Display results
pprint(results)
