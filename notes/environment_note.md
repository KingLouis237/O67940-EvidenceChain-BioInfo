# Environment note

The conda environment used for this re-analysis was exported to `environment.yml`.

This file records the software packages available in the `methods_bioinfo` environment. It helps make the workflow more reproducible because another user can inspect or recreate a similar environment.

The export was created with:

`conda env export --no-builds > environment.yml`

## 2026-11-06 environment refresh

The `methods_bioinfo` environment snapshot was refreshed after the O58212 functional-anchor audit.

The previous tracked environment snapshot was preserved as `metadata/environment_before_2026-11-06_refresh.yml`.

The current environment was exported with `conda env export --no-builds`.

The machine-specific `prefix:` line was removed from `environment.yml` to keep the file portable.

`pypdf==6.21.4` was installed specifically during the O58212 functional-anchor audit because no PDF text-extraction library or `pdftotext` executable was available in the existing environment. It was used to produce the page-marked text derivative of the 2008 supporting-information PDF.

Other differences relative to the previous environment snapshot, including `mmseqs2`, `aria2`, `c-ares`, `libssh2`, and updated certificate packages, reflect accumulated environment changes and are not attributed specifically to the O58212 audit.
