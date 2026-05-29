# Step 3 — PAE JSON structure check

## Aim

Before summarizing the AlphaFold Predicted Aligned Error (PAE) file, the JSON structure was inspected manually using a small Python command. This was done to avoid assuming the internal format of the file.

## Why this check matters

JSON files are structured data files. However, different APIs and databases may store similar information in slightly different layouts. For example, a JSON file may contain a dictionary at the top level, or it may contain a list with one dictionary inside it.

If a script assumes the wrong structure, it may fail or, worse, silently extract the wrong information. Therefore, the workflow first checks the structure of the PAE JSON before writing a summary script.

## Command used

```bash
python - << 'PY'
import json
from pathlib import Path

path = Path("data/alphafold/AF-O67940-F1-predicted_aligned_error_v6.json")

with path.open() as f:
    data = json.load(f)

print("Top-level type:", type(data))
if isinstance(data, list):
    print("List length:", len(data))
    first = data[0]
    print("First element keys:", first.keys())
elif isinstance(data, dict):
    print("Dictionary keys:", data.keys())
PY

## Observed output

```text
Top-level type: <class 'list'>
List length: 1
First element keys: dict_keys(['predicted_aligned_error', 'max_predicted_aligned_error'])

## Observed output

```text
Top-level type: <class 'list'>
List length: 1
First element keys: dict_keys(['predicted_aligned_error', 'max_predicted_aligned_error'])
