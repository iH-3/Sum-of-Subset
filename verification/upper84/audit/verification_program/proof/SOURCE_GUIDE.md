# Proof and verification source guide

Paths below are relative to the `verification_program` folder.

- `proof/report.tex`: standalone source of the accompanying English PDF. The main text gives the common lemmas and proof organization; the appendices contain the detailed stratum arguments
- `README.md`: Python and Windows instructions, result semantics, and the human-proof boundary
- `COVERAGE_MAP.json`: each report lemma/stratum mapped to executable checks or a written-proof dependency
- `SOURCE_MAP.json` and `data/chapter_provenance.json`: original mathematical source identities and the explicitly documented portable transcriptions. Hashes establish provenance only
- `foundations/proof/STRUCTURAL86.md`: retained structural derivation and its mathematical inputs
- `foundations/source/structural/foundations/general_lemmas_source.tex`: general mathematical statements and references
- `foundations/source/structural/foundations/nonap_defect.md`: non-AP finite-to-infinite reduction
- `foundations/proof/dense_holes_direct_defects.tex`: dense finite-to-infinite/profile/direct-defect arguments
- `foundations/proof/endpoint_bridge_correction.txt`: corrected endpoint-bridge statement and proof
- `foundations/COVERAGE.json`, `foundations/SOURCE_MAP.json`, and `foundations/README.md`: exact finite domains, source transformations, and methods
- `data/arithmetic.json`, `data/fixed_cover_certificate.json`, `data/p4_seeds.json`, `data/p3_appendix.json`, and `data/z5_appendix.json`: readable exact arithmetic inputs
- `sample_results/full/coverage.json` and `sample_results/full/verification_log.txt`: an actual full executable run
- `TEST_REPORT.json`: isolation, optimization, negative-input and static Windows-launcher tests

The program does not formalize every analytical statement or reproduce the proofs of all published general inputs. A successful run certifies the precise executable statements listed in its coverage output. Historical status wording in retained foundation excerpts does not replace the current consolidated argument.
