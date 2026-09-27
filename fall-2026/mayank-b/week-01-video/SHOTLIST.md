# SHOTLIST — typed work order

| Beat | Pattern | Type | Visual (what moves) |
|---|---|---|---|
| B00 | ClaudeComposerAsk | BOOKEND | question types; output = real stdout of run_temperature.py (not a Claude reply) |
| B01 | BrutalistHesitantWriter | BOOKEND | "how creative the model is" typed, deleted, retyped as "how concentrated the choices are" |
| B01A | TcNextWord (new, v5) | SHOW | 'The capital of France is ___'; four candidate tokens with unnumbered score bars (ILLUSTRATIVE stamp); 'chance?' column; softmax label; 'Paris' drops into the blank |
| B02 | TcScoresToOdds (v6 table) | SHOW | softmax in three moves: score → MOVE 1 weight e^z (2.72/7.39/20.09) → MOVE 2 total 30.19 → MOVE 3 weight ÷ total with bars (9.0/24.5/66.5%); formula labelled top = your weight, bottom = everyone's total |
| B03 | TcTemperatureDial (v6 table) | SHOW | 'z ÷ T' column; T slides 1 → 0.5 → 2 and every cell recomputes live (2,4,6 → 7.39/54.60/403.43 → 1.6/11.7/86.7%; 0.5,1,1.5 → 1.65/2.72/4.48 → 18.6/30.7/50.6%); dashed T=1 bars; zoom caption; rank badges |
| B04 | TcRatio (new) | SHOW | ratio identity; gap = 2; ratio bars/counters 54.60× / 7.39× / 2.72× |
| B05 | TcCode (new) | SHOW | verbatim function; divide line + T ≤ 0 guard highlighted; inputs vs never-inputs |
| B06 | TcSampleCounts (new) | SHOW | 2×1000 real seed-7 draws fill grids in draw order, counters tick, then sort by outcome |
| B07 | TcWrongAnswer (new) | SHOW | CONSTRUCTED stamp; answer key; T 1→0.5 shrinks correct bar, grows wrong one; "not an input" |
| B08 | TcBoundary (new) | SHOW | claims sort into SHOWN / NOT SHOWN; both NOT SHOWN items in red (v6) |
| BVDT | ClaudeVerdictArtifact | BOOKEND | recap artifact, labelled "Recap written by the author, not a Claude response" |
| BOUT | ClaudeTitleOutro | BOOKEND | locked title outro |
