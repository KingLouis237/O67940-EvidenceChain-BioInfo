import json
from pathlib import Path

# Input and output paths
input_path = Path("data/O67940_uniprot_record.json")
output_path = Path("results/uniprot_O67940_record_summary.txt")

# Load UniProt JSON record
with input_path.open() as f:
    record = json.load(f)

# Basic identifiers
accession = record.get("primaryAccession", "NA")
entry_type = record.get("entryType", "NA")
uni_prot_id = record.get("uniProtkbId", "NA")

# Protein name
protein_description = record.get("proteinDescription", {})
recommended_name = protein_description.get("recommendedName", {})
protein_name = (
    recommended_name.get("fullName", {}).get("value")
    or protein_description.get("submissionNames", [{}])[0].get("fullName", {}).get("value", "NA")
)

# Organism
organism = record.get("organism", {})
organism_name = organism.get("scientificName", "NA")
taxon_id = organism.get("taxonId", "NA")

# Sequence
sequence = record.get("sequence", {})
length = sequence.get("length", "NA")
mol_weight = sequence.get("molWeight", "NA")
crc64 = sequence.get("crc64", "NA")

# Protein existence
protein_existence = record.get("proteinExistence", "NA")

# Collect database cross-references
xrefs = record.get("uniProtKBCrossReferences", [])

def collect_xrefs(database_name):
    """Return all cross-reference IDs for a given database."""
    return [x.get("id", "NA") for x in xrefs if x.get("database") == database_name]

interpro = collect_xrefs("InterPro")
pfam = collect_xrefs("Pfam")
alphafold = collect_xrefs("AlphaFoldDB")
pdb = collect_xrefs("PDB")
go = collect_xrefs("GO")
eggnog = collect_xrefs("eggNOG")
kegg = collect_xrefs("KEGG")

# Comments, especially function comments if present
comments = record.get("comments", [])
function_comments = [
    c for c in comments
    if c.get("commentType") == "FUNCTION"
]

# Write clean summary
with output_path.open("w") as out:
    out.write("UniProt full record summary for O67940_AQUAE\n")
    out.write("=" * 55 + "\n\n")

    out.write(f"Accession: {accession}\n")
    out.write(f"UniProt ID: {uni_prot_id}\n")
    out.write(f"Entry type: {entry_type}\n")
    out.write(f"Protein name: {protein_name}\n")
    out.write(f"Organism: {organism_name}\n")
    out.write(f"Taxon ID: {taxon_id}\n")
    out.write(f"Protein existence: {protein_existence}\n")
    out.write(f"Sequence length: {length}\n")
    out.write(f"Molecular weight: {mol_weight}\n")
    out.write(f"CRC64: {crc64}\n\n")

    out.write("Cross-references\n")
    out.write("-" * 20 + "\n")
    out.write(f"InterPro: {', '.join(interpro) if interpro else 'None found'}\n")
    out.write(f"Pfam: {', '.join(pfam) if pfam else 'None found'}\n")
    out.write(f"AlphaFoldDB: {', '.join(alphafold) if alphafold else 'None found'}\n")
    out.write(f"PDB: {', '.join(pdb) if pdb else 'None found'}\n")
    out.write(f"GO: {', '.join(go) if go else 'None found'}\n")
    out.write(f"eggNOG: {', '.join(eggnog) if eggnog else 'None found'}\n")
    out.write(f"KEGG: {', '.join(kegg) if kegg else 'None found'}\n\n")

    out.write("Function comments\n")
    out.write("-" * 20 + "\n")
    if function_comments:
        for c in function_comments:
            out.write(json.dumps(c, indent=2))
            out.write("\n")
    else:
        out.write("No UniProt FUNCTION comment found.\n")

print(f"Summary written to {output_path}")
