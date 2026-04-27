"""Corpus revision scenario families for Blueprint v3.

Each module exports: generate_scenarios(forbidden_fingerprints: set) -> list[dict]

Scenario families (9 total):
  1. pfa_scenarios           — PFA c-bet decisions (Rule 4 pattern)
  2. facing_initial_bet_scenarios — initial-bet response (CALL/RAISE/FOLD)
  3. bac_scenarios           — bet-and-call sandwich (MW-30 pattern)
  4. magg_scenarios          — multi-street aggression (river; villain_aggression_count=2)
  5. nfd_scenarios           — nut-FD facing bet (KB §1.7 pattern)
  6. monster_facing_bet_scenarios — set/monster facing initial bet (MW-33 pattern)
  7. rule11_boundary_scenarios — Rule 11 threshold boundary (>=3 board textures)
  8. donk_bet_defence_scenarios  — NEW: IP hero vs OOP donk (Module 8)
  9. sb_hero_scenarios       — NEW: SB-as-hero sandwich (Module 9)

Blueprint: review/comms/BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3_2026-04-27.md
"""
