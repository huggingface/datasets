# VAIXLNS Ω∞ — Evolution Intake Contract v0.1

Status: PROPOSED — no runtime enforcement claimed.
Scope: third-party datasets, software, models, protocols, research, agents, and interfaces.
This document is a design contract, not authorization to ingest, redistribute, train on, or publish third-party works.

## Rule
Every intake must be traceable to its original source and license, and evaluated against an existing baseline. "Evolution" means measured improvement, not automatic feature accumulation. Duplicate or worse alternatives may be rejected. Historical identities and source evidence must never be silently deleted.

## Pipeline
1. DISCOVER: locate prior internal implementation and original external source.
2. RIGHTS: capture exact source URI, revision, retrieval date, license text, attribution obligations, data privacy and commercial/redistribution/AI-training rights independently. Unknown rights -> HOLD; retain metadata only where lawful.
3. DECOMPOSE: architecture, interfaces, dependencies, threat surface, tests and assumptions.
4. COMPARE: baseline metrics, competing methods, costs, failure modes, and provenance.
5. SIMULATE: isolate candidate changes; record expected benefit, adverse effects, and rollback.
6. EVOLVE: implement minimal improvement on an isolated branch only.
7. VERIFY: independent functional, security, performance, compatibility, rights checks with reproducible evidence.
8. ADMIT: VX proposal to governance; approval is separate from execution. No merge, release, redistribution, financial transaction, or paid external action without authorization.

## Intake record schema (logical fields)
- intake_id, item_type, source_uri, source_revision, source_owner, retrieval_time, hashes
- origin: ORIGINAL | DERIVED; upstream_relation; license_spdx_or_NOASSERTION; license_text_evidence
- permissions: internal_use, modification, commercial_use, ai_training, redistribution, api_serving (each ALLOW | DENY | UNKNOWN)
- copyright_notices, attribution, notice, share_alike, contract_constraints, privacy_review
- existing_equivalent_ref; baseline_commit; baseline_metrics; proposed_change; hypothesis
- simulation_receipt; tests; evidence_uris; reviewer; decision; rollback_plan
- maturity: PROPOSED | IMPLEMENTED | VERIFIED (independent of rights decision)
- rights_decision: ALLOW | CONDITIONAL | HOLD | DENY

## Fail-closed gates
- Missing source or unclear relevant rights -> HOLD for affected operations.
- Legal approval must not be inferred from Apache licensing of a loader or from a public dataset listing.
- No VERIFIED without commit-pinned tests and independently reviewable evidence.
- No silent deletion, promotion of inferred history to canonical, or modification of protected project.genome / Ω.000.
- No merge to main or publication automatically; external spending ceiling 0 SAR.

## Quality metrics
- Data: provenance coverage, validation error rate, duplicate rate, retrieval latency.
- Code/server: p50/p95 latency, throughput, failure rate, reproducibility, security regressions.
- Models/agents: task success, calibration, evidence validity, cost per task, safety regressions.
- Progress is accepted only with improvement against an explicit baseline and no breach of guardrails.

## Initial verification plan (NOT_RUN)
- Check every intake has source and immutable evidence references.
- Reject redistribution if redistribution rights are UNKNOWN or DENY.
- Reject commercial use if commercial rights are UNKNOWN or DENY.
- Require attributed license/NOTICE propagation where applicable.
- Require separate policy approval and CI proof before release.
- Confirm protected paths remain byte-identical and branch isolation maintained.

## Integration
This is a proposed adapter into existing VAIXLNS Ω / VX governance, not a fifth sovereign system. Reuse existing indexes and evidence formats before adding new storage. 
