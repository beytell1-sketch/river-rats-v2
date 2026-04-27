"""Tests for mass-labelling dispatch + collect scripts (Phase 11A).

Per `MAIN_TERMINAL_MASS_LABELLING_RESOLUTION_2026-04-27.md` directive
asking ml-architect mini-review on:
  - ref_id transformation handles both schemas
  - consensus computes plurality correctly
  - retry / null-handling logic bounds cost

These tests cover the deterministic helpers — Agent-tool dispatch is
out of scope for unit testing and verified end-to-end at PR open time.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile

import pytest

_REPO = os.path.join(os.path.dirname(__file__), '..', '..')


def _load(module_name: str):
    """Load a script under scripts/ as a module (scripts/ is not on sys.path)."""
    path = os.path.join(_REPO, 'scripts', f'{module_name}.py')
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope='module')
def dispatch():
    return _load('dispatch_mass_labelling')


@pytest.fixture(scope='module')
def collect():
    return _load('collect_mass_labels')


# ===========================================================================
# ref_id transformation
# ===========================================================================

class TestComputeRefId:
    """compute_ref_id covers all 3 corpus record schemas."""

    def test_pilot_record_uses_source_situation_id(self, dispatch):
        rec = {
            'pilot_hand_id': 'PILOT_001',
            'source_situation_id': 'd6066_BB_flop',
            'deal_id': 6066,
            'hero_position': 'BB',
            'street': 'flop',
        }
        assert dispatch.compute_ref_id(rec) == 'd6066_BB_flop'

    def test_mode_a_record_falls_back_to_deal_pos_street(self, dispatch):
        rec = {
            'pilot_hand_id': 'PILOT_186',
            'source_situation_id': None,
            'deal_id': 521,
            'hero_position': 'BB',
            'street': 'flop',
        }
        assert dispatch.compute_ref_id(rec) == 'd521_BB_flop'

    def test_mode_b_record_falls_back_to_pilot_hand_id(self, dispatch):
        rec = {
            'pilot_hand_id': 'PILOT_101',
            'hero_position': 'CO',
            'street': 'flop',
        }
        assert dispatch.compute_ref_id(rec) == 'PILOT_101'

    def test_record_with_none_source_situation_falls_through(self, dispatch):
        rec = {
            'pilot_hand_id': 'PILOT_220',
            'source_situation_id': None,
            'deal_id': 999,
            'hero_position': 'CO',
            'street': 'turn',
        }
        assert dispatch.compute_ref_id(rec) == 'd999_CO_turn'

    def test_record_with_no_id_fields_raises(self, dispatch):
        rec = {'hero_position': 'CO', 'street': 'flop'}
        with pytest.raises(ValueError):
            dispatch.compute_ref_id(rec)

    def test_full_corpus_yields_distinct_ref_ids(self, dispatch):
        """Smoke test on the actual 494-hand corpus."""
        path = os.path.join(_REPO, 'data',
                            'corpus_revision_500_hand_2026-04-27.jsonl')
        if not os.path.exists(path):
            pytest.skip(f'corpus not present: {path}')
        with open(path) as f:
            records = [json.loads(line) for line in f if line.strip()]
        ref_ids = [dispatch.compute_ref_id(r) for r in records]
        assert len(ref_ids) == 494
        assert len(set(ref_ids)) == 494, (
            f"non-unique ref_ids: {len(ref_ids) - len(set(ref_ids))} dups"
        )


# ===========================================================================
# Consensus aggregation
# ===========================================================================

class TestConsensus:
    """Plurality consensus with null-vote handling."""

    def test_unanimous_passes_through(self, collect):
        result = collect.consensus(['BET'] * 5)
        assert result['consensus_action'] == 'BET'
        assert result['consensus_confidence'] == 1.0
        assert result['valid_vote_count'] == 5

    def test_plurality_majority(self, collect):
        result = collect.consensus(['BET', 'BET', 'BET', 'CHECK', 'CALL'])
        assert result['consensus_action'] == 'BET'
        assert result['consensus_confidence'] == 0.6  # 3/5

    def test_null_votes_excluded_from_tally(self, collect):
        # 3 BET + 1 CHECK + 1 null → BET 3/4 = 0.75
        result = collect.consensus(['BET', 'BET', 'BET', 'CHECK', None])
        assert result['consensus_action'] == 'BET'
        assert result['consensus_confidence'] == 0.75
        assert result['vote_count'] == 5
        assert result['valid_vote_count'] == 4

    def test_all_null_returns_no_consensus(self, collect):
        result = collect.consensus([None] * 5)
        assert result['consensus_action'] is None
        assert result['consensus_confidence'] == 0.0
        assert result['valid_vote_count'] == 0

    def test_empty_returns_no_consensus(self, collect):
        result = collect.consensus([])
        assert result['consensus_action'] is None
        assert result['consensus_confidence'] == 0.0
        assert result['vote_count'] == 0

    def test_tie_resolved_alphabetically(self, collect):
        # 2 BET + 2 CHECK + 1 null → tie at 2/4; alphabetical -> BET
        result = collect.consensus(['BET', 'BET', 'CHECK', 'CHECK', None])
        assert result['consensus_action'] == 'BET'
        assert result['consensus_confidence'] == 0.5

    def test_tie_three_way(self, collect):
        # BET CHECK CALL null null → 1/2 each on all 3; alphabetical -> BET
        result = collect.consensus(['BET', 'CHECK', 'CALL', None, None])
        assert result['consensus_action'] == 'BET'

    def test_minority_winner_when_majority_are_null(self, collect):
        # 1 RAISE + 4 nulls → RAISE 1/1 = 1.0
        result = collect.consensus(['RAISE', None, None, None, None])
        assert result['consensus_action'] == 'RAISE'
        assert result['consensus_confidence'] == 1.0
        assert result['valid_vote_count'] == 1


# ===========================================================================
# Per-labeller file loader
# ===========================================================================

class TestLoadLabellerFile:
    """Tolerance + validation behaviour for messy labeller output."""

    def _write(self, dirpath: str, labels: list) -> str:
        path = os.path.join(dirpath, 'labels_v3_2_labeller_1.json')
        with open(path, 'w') as f:
            json.dump({
                'lane': 'labeller_1',
                'model': 'claude-sonnet-4-6',
                'protocol_version': 'v3.2',
                'protocol': 'prompts/gto_labeller_v3.2.md',
                'total_labels': len(labels),
                'labels': labels,
            }, f)
        return path

    def test_well_formed_file_loads_all(self, collect, tmp_path):
        labels = [
            {'ref_id': 'r1', 'action': 'BET', 'confidence': 'HIGH',
             'reasoning': 'x'},
            {'ref_id': 'r2', 'action': 'CHECK', 'confidence': 'MEDIUM',
             'reasoning': 'y'},
        ]
        path = self._write(str(tmp_path), labels)
        result = collect._load_labeller_file(path)
        assert set(result.keys()) == {'r1', 'r2'}
        assert result['r1']['action'] == 'BET'
        assert result['r1']['confidence'] == 'HIGH'

    def test_invalid_action_coerced_to_null(self, collect, tmp_path):
        labels = [
            {'ref_id': 'r1', 'action': 'shove', 'confidence': 'HIGH',
             'reasoning': 'x'},
        ]
        path = self._write(str(tmp_path), labels)
        result = collect._load_labeller_file(path)
        assert result['r1']['action'] is None

    def test_explicit_null_action_preserved(self, collect, tmp_path):
        labels = [
            {'ref_id': 'r1', 'action': None, 'confidence': 'LOW',
             'reasoning': 'refusal'},
        ]
        path = self._write(str(tmp_path), labels)
        assert collect._load_labeller_file(path)['r1']['action'] is None

    def test_lowercase_action_uppercased(self, collect, tmp_path):
        labels = [{'ref_id': 'r1', 'action': 'bet', 'confidence': 'high',
                   'reasoning': ''}]
        path = self._write(str(tmp_path), labels)
        result = collect._load_labeller_file(path)
        assert result['r1']['action'] == 'BET'
        assert result['r1']['confidence'] == 'HIGH'

    def test_invalid_confidence_coerced_low(self, collect, tmp_path):
        labels = [{'ref_id': 'r1', 'action': 'BET', 'confidence': 'OK',
                   'reasoning': ''}]
        path = self._write(str(tmp_path), labels)
        assert collect._load_labeller_file(path)['r1']['confidence'] == 'LOW'

    def test_missing_ref_id_skipped(self, collect, tmp_path):
        labels = [
            {'ref_id': 'r1', 'action': 'BET', 'confidence': 'HIGH',
             'reasoning': ''},
            {'action': 'CHECK', 'confidence': 'MEDIUM', 'reasoning': ''},
        ]
        path = self._write(str(tmp_path), labels)
        result = collect._load_labeller_file(path)
        assert set(result.keys()) == {'r1'}


# ===========================================================================
# End-to-end collect on a tiny fixture
# ===========================================================================

class TestCollectIntegration:

    def test_collect_aggregates_5_labellers_on_2_hand_fixture(
            self, collect, tmp_path):
        # Tiny corpus: 2 records.
        corpus_path = tmp_path / 'corpus.jsonl'
        records = [
            {'pilot_hand_id': 'PILOT_001',
             'source_situation_id': 'd1_CO_flop',
             'deal_id': 1, 'hero_position': 'CO', 'street': 'flop',
             'feat_dict': {'spr': 5.0}},
            {'pilot_hand_id': 'PILOT_101',
             'hero_position': 'BTN', 'street': 'turn',
             'feat_dict': {'spr': 3.0}},
        ]
        with open(corpus_path, 'w') as f:
            for r in records:
                f.write(json.dumps(r) + '\n')

        # 5 labeller files: BET wins consensus on PILOT_001;
        # PILOT_101 has a tie + 1 null.
        labels_per_labeller = {
            1: [
                {'ref_id': 'd1_CO_flop', 'action': 'BET',
                 'confidence': 'HIGH', 'reasoning': 'a'},
                {'ref_id': 'PILOT_101', 'action': 'CHECK',
                 'confidence': 'HIGH', 'reasoning': 'a'},
            ],
            2: [
                {'ref_id': 'd1_CO_flop', 'action': 'BET',
                 'confidence': 'HIGH', 'reasoning': 'b'},
                {'ref_id': 'PILOT_101', 'action': 'CHECK',
                 'confidence': 'MEDIUM', 'reasoning': 'b'},
            ],
            3: [
                {'ref_id': 'd1_CO_flop', 'action': 'BET',
                 'confidence': 'MEDIUM', 'reasoning': 'c'},
                {'ref_id': 'PILOT_101', 'action': 'CALL',
                 'confidence': 'MEDIUM', 'reasoning': 'c'},
            ],
            4: [
                {'ref_id': 'd1_CO_flop', 'action': 'CHECK',
                 'confidence': 'LOW', 'reasoning': 'd'},
                {'ref_id': 'PILOT_101', 'action': 'CALL',
                 'confidence': 'LOW', 'reasoning': 'd'},
            ],
            5: [
                {'ref_id': 'd1_CO_flop', 'action': 'BET',
                 'confidence': 'HIGH', 'reasoning': 'e'},
                {'ref_id': 'PILOT_101', 'action': None,
                 'confidence': 'LOW', 'reasoning': 'refusal'},
            ],
        }
        for n, labels in labels_per_labeller.items():
            path = tmp_path / f'labels_v3_2_labeller_{n}.json'
            with open(path, 'w') as f:
                json.dump({
                    'lane': f'labeller_{n}',
                    'model': 'claude-sonnet-4-6',
                    'protocol_version': 'v3.2',
                    'protocol': 'prompts/gto_labeller_v3.2.md',
                    'total_labels': len(labels),
                    'labels': labels,
                }, f)

        out_path = tmp_path / 'out.jsonl'
        stats = collect.collect(
            corpus_path=str(corpus_path),
            labels_dir=str(tmp_path),
            output_path=str(out_path),
            num_labellers=5,
        )

        with open(out_path) as f:
            rows = [json.loads(line) for line in f]
        assert len(rows) == 2

        row1 = rows[0]
        assert row1['ref_id'] == 'd1_CO_flop'
        assert len(row1['labels']) == 5
        assert row1['consensus_action'] == 'BET'  # 4/5
        assert row1['consensus_confidence'] == 0.8
        assert row1['valid_vote_count'] == 5

        row2 = rows[1]
        assert row2['ref_id'] == 'PILOT_101'
        # CHECK 2 + CALL 2 + null → tie alphabetical → CALL
        assert row2['consensus_action'] == 'CALL'
        assert row2['consensus_confidence'] == 0.5  # 2/4
        assert row2['valid_vote_count'] == 4
        assert row2['vote_count'] == 5

        assert stats['refusal_rate'] == 1 / 10  # 1 refusal across 10 total
        assert stats['no_consensus'] == 0

    def test_collect_handles_missing_labeller_file(
            self, collect, tmp_path):
        corpus_path = tmp_path / 'corpus.jsonl'
        with open(corpus_path, 'w') as f:
            f.write(json.dumps({
                'pilot_hand_id': 'PILOT_001',
                'source_situation_id': 'd1_CO_flop',
                'deal_id': 1, 'hero_position': 'CO', 'street': 'flop',
                'feat_dict': {},
            }) + '\n')

        # Only labellers 1, 2, 3 produce output; 4 and 5 are missing.
        for n in (1, 2, 3):
            with open(tmp_path / f'labels_v3_2_labeller_{n}.json', 'w') as f:
                json.dump({
                    'lane': f'labeller_{n}', 'model': 'x',
                    'protocol_version': 'v3.2',
                    'protocol': 'prompts/gto_labeller_v3.2.md',
                    'total_labels': 1,
                    'labels': [{
                        'ref_id': 'd1_CO_flop', 'action': 'BET',
                        'confidence': 'HIGH', 'reasoning': '',
                    }],
                }, f)

        out_path = tmp_path / 'out.jsonl'
        stats = collect.collect(
            corpus_path=str(corpus_path),
            labels_dir=str(tmp_path),
            output_path=str(out_path),
            num_labellers=5,
        )
        with open(out_path) as f:
            row = json.loads(f.readline())
        assert row['vote_count'] == 3  # only 3 of 5 labellers produced output
        assert row['valid_vote_count'] == 3
        assert row['consensus_action'] == 'BET'
        assert stats['missing_per_labeller'] == [0, 0, 0, 1, 1]


# ===========================================================================
# Dispatch prepare smoke test
# ===========================================================================

class TestDispatchPrepare:

    def test_prepare_writes_briefs_and_manifest(self, dispatch, tmp_path):
        corpus_path = tmp_path / 'corpus.jsonl'
        protocol_path = tmp_path / 'protocol.md'
        out_dir = tmp_path / 'briefs'

        records = [
            {
                'pilot_hand_id': 'PILOT_001',
                'source_situation_id': 'd1_CO_flop',
                'deal_id': 1, 'hero_position': 'CO', 'street': 'flop',
                'hero_cards': ['As', 'Ks'], 'board': ['7c', '4d', '2h'],
                'villain_positions': ['BB'], 'num_opponents': 1,
                'pot': 10.0, 'to_call': 0, 'facing_bet': False,
                'feat_dict': {'raw_equity': 0.65, 'spr': 5.0},
                'prior_actions': ['preflop: CO raise'],
            },
            {
                'pilot_hand_id': 'PILOT_101',
                'hero_position': 'BTN', 'street': 'turn',
                'hero_cards': ['Qh', 'Jh'], 'board': ['Th', '9h', '2c', '3d'],
                'villain_positions': ['BB'], 'num_opponents': 1,
                'pot': 20.0, 'to_call': 5, 'facing_bet': True,
                'feat_dict': {'raw_equity': 0.55, 'spr': 3.0},
                'prior_actions': ['preflop: BTN raise', 'flop: BTN bet'],
            },
        ]
        with open(corpus_path, 'w') as f:
            for r in records:
                f.write(json.dumps(r) + '\n')
        protocol_path.write_text("# v3.2 protocol stub\n")

        manifest = dispatch.prepare(
            corpus_path=str(corpus_path),
            protocol_path=str(protocol_path),
            num_labellers=5,
            output_dir=str(out_dir),
        )

        assert manifest['num_labellers'] == 5
        assert manifest['total_hands'] == 2
        assert len(manifest['briefs']) == 5
        assert manifest['ref_ids'] == ['d1_CO_flop', 'PILOT_101']

        for n in range(1, 6):
            brief_path = out_dir / f'labeller_{n}_brief.md'
            assert brief_path.exists()
            text = brief_path.read_text()
            assert 'v3.2 protocol stub' in text
            assert '--- HAND: d1_CO_flop ---' in text
            assert '--- HAND: PILOT_101 ---' in text
            assert f'labels_v3_2_labeller_{n}.json' in text

        assert (out_dir / 'manifest.json').exists()

    def test_prepare_rejects_collisions(self, dispatch, tmp_path):
        corpus_path = tmp_path / 'corpus.jsonl'
        protocol_path = tmp_path / 'protocol.md'
        protocol_path.write_text("stub")
        # Two records that compute_ref_id will return the same value for.
        records = [
            {'pilot_hand_id': 'PILOT_001', 'hero_position': 'CO',
             'street': 'flop', 'feat_dict': {}},
            {'pilot_hand_id': 'PILOT_001', 'hero_position': 'CO',
             'street': 'turn', 'feat_dict': {}},
        ]
        with open(corpus_path, 'w') as f:
            for r in records:
                f.write(json.dumps(r) + '\n')

        with pytest.raises(RuntimeError, match='ref_id collisions'):
            dispatch.prepare(
                corpus_path=str(corpus_path),
                protocol_path=str(protocol_path),
                num_labellers=5,
                output_dir=str(tmp_path / 'briefs'),
            )
