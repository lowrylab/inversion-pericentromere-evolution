# Audit summary

The clean repository was assembled from the corrected maintenance baseline and
Arm B directories after auditing the wider `slim-inversion-agent` tree. The
older full-genome ICE branch, duplicate templates, handoff notes, decision
logs, and prior analyses are separated under `archive/`.

The current baseline model hash is
`f49e03a9d63ef8ac10697aded0a8916eb0bdc735b9bf75d0a597d5f30f3aa9df`. The
current Arm B model hash is
`71124f228b292f5324b054540e45d6cf07d15ce0c316909c68a543574783ca70`.

The completed baseline contains 700 successful runs and compact derived output.
Arm B has a passed local production-model smoke test and a complete 300-task
manifest, but no MSU HPCC jobs were launched from the audit environment. The
repository therefore reports HPCC validation and production completion as
pending rather than inferring them from local preparation.

