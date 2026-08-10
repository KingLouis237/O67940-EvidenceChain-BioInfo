# External tool compatibility

## MMseqs2

Redundancy clustering uses a project-local MMseqs2 binary rather than the Conda executable.

The `methods_bioinfo` Conda environment contains:

- package: `mmseqs2`
- package version: `18.8cc5c`

However, running the Conda executable on this host produced:

`Illegal instruction (core dumped)`

The host is x86_64 with an Intel Core i7-3612QM and exposes SSE2 and SSE4.1 but not AVX2.

The exact compilation requirement of the failing Conda binary was not established, so the failure is documented conservatively as a CPU/build compatibility problem.

The canonical project binary is therefore the official SSE4.1 Linux asset from the fixed MMseqs2 release:

- release tag: `18-8cc5c`
- reported commit: `8cc5ce367b5638c4306c2d7cfc652dd099a4643f`
- archive SHA256: `0ece6a6af8f5d198bccabc98cb5fddfc9212ce04bb332e486bfdcc468c0d7b08`
- executable SHA256: `0930c12e79b78d5f3546adac8cd7e302a1a0a308b30edb8178f7466f3855ec4f`

Reinstallation is handled by:

`scripts/05_evolutionary_active_site_context/setup_mmseqs2_sse41.sh`

Workflow scripts call this binary by its explicit project-local path rather than relying on whichever `mmseqs` executable appears first in `$PATH`.
