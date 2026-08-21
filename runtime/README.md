# Runtime skill isolation

`skill-index.yaml` declares the projection policy. The actual safety boundary
is `scripts/build_runtime_skill_views.sh`: each runtime receives a distinct
immediate-child skill directory. Do not point a runtime at the catalog root.

The catalog may retain imported upstream content for provenance, but imports
must be copied into the catalog rather than symlinked to Pi, DSH, or another
runtime checkout.

`runtime-skill-guard` is an audit aid. It cannot be the primary enforcement
mechanism because a model-level skill is evaluated after its host has built a
catalog. Enforce compatibility with runtime roots first.
