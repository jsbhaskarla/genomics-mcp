"""
AlphaFold DB Wrapper - Query protein structures
"""

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ProteinStructure:
    gene_name: str
    protein_name: str
    uniprot_id: str
    pdb_ids: List[str]
    domains: List[str]
    binding_sites: List[str]
    length_amino_acids: int
    organism: str
    plddt_score: float
    has_alphafold_model: bool
    
    def to_dict(self):
        return {
            'gene_name': self.gene_name,
            'protein_name': self.protein_name,
            'uniprot_id': self.uniprot_id,
            'pdb_ids': self.pdb_ids,
            'domains': self.domains,
            'binding_sites': self.binding_sites,
            'length_amino_acids': self.length_amino_acids,
            'organism': self.organism,
            'plddt_score': self.plddt_score,
            'has_alphafold_model': self.has_alphafold_model
        }


class AlphaFoldWrapper:
    """Wrapper for AlphaFold protein structures"""
    
    def __init__(self):
        self.proteins = self._load_proteins()
    
    def _load_proteins(self) -> List[ProteinStructure]:
        """Load protein structures"""
        return [
            ProteinStructure(
                gene_name='TP53',
                protein_name='Tumor protein p53',
                uniprot_id='P04637',
                pdb_ids=['1TUP', '2AC0', '1OLG', '4HIE'],
                domains=['DNA-binding domain', 'Tetramerization domain', 'Regulatory domain'],
                binding_sites=['DNA binding', 'p53BP1 binding', 'MDM2 binding'],
                length_amino_acids=393,
                organism='Homo sapiens',
                plddt_score=87.5,
                has_alphafold_model=True
            ),
            ProteinStructure(
                gene_name='BRCA1',
                protein_name='Breast cancer type 1 susceptibility protein',
                uniprot_id='P38398',
                pdb_ids=['1JM7', '1N5O', '3K0H'],
                domains=['RING domain', 'Coiled-coil 1', 'Coiled-coil 2', 'BRCT 1', 'BRCT 2'],
                binding_sites=['BARD1 binding', 'RAD51 binding', 'Chromatin binding'],
                length_amino_acids=1863,
                organism='Homo sapiens',
                plddt_score=76.2,
                has_alphafold_model=True
            ),
            ProteinStructure(
                gene_name='BRCA2',
                protein_name='Breast cancer type 2 susceptibility protein',
                uniprot_id='P51431',
                pdb_ids=['1MIU', '3E8F', '3K0L'],
                domains=['DNA-binding domain', 'Tower domain', 'OB-fold 1', 'OB-fold 2'],
                binding_sites=['RAD51 binding', 'ssDNA binding', 'dsDNA binding'],
                length_amino_acids=3418,
                organism='Homo sapiens',
                plddt_score=71.8,
                has_alphafold_model=True
            ),
            ProteinStructure(
                gene_name='EGFR',
                protein_name='Epidermal growth factor receptor',
                uniprot_id='P00533',
                pdb_ids=['1IVO', '2M20', '3NPQ', '5XZY'],
                domains=['Extracellular domain', 'Transmembrane domain', 'Intracellular kinase domain'],
                binding_sites=['EGF binding', 'Kinase active site', 'ATP binding'],
                length_amino_acids=1210,
                organism='Homo sapiens',
                plddt_score=85.4,
                has_alphafold_model=True
            ),
            ProteinStructure(
                gene_name='PTEN',
                protein_name='Phosphatase and tensin homolog',
                uniprot_id='P60484',
                pdb_ids=['1D5R', '2AUQ', '3ZZM'],
                domains=['Phosphatase domain', 'C2 domain', 'PDZ-binding motif'],
                binding_sites=['Phospholipid binding', 'Substrate binding', 'Protein-protein interaction'],
                length_amino_acids=403,
                organism='Homo sapiens',
                plddt_score=82.1,
                has_alphafold_model=True
            ),
        ]
    
    def lookup(self, gene_name: str) -> Optional[ProteinStructure]:
        """Look up protein by gene name"""
        for protein in self.proteins:
            if protein.gene_name.upper() == gene_name.upper():
                return protein
        return None
    
    def get_by_uniprot(self, uniprot_id: str) -> Optional[ProteinStructure]:
        """Get protein by UniProt ID"""
        for protein in self.proteins:
            if protein.uniprot_id == uniprot_id:
                return protein
        return None
    
    def get_by_pdb(self, pdb_id: str) -> Optional[ProteinStructure]:
        """Get protein by PDB ID"""
        for protein in self.proteins:
            if pdb_id in protein.pdb_ids:
                return protein
        return None
    
    def list_available_genes(self) -> List[str]:
        """List all available genes"""
        return [p.gene_name for p in self.proteins]
    
    def get_domains_for_gene(self, gene_name: str) -> Optional[List[str]]:
        """Get domains for a gene"""
        protein = self.lookup(gene_name)
        return protein.domains if protein else None


if __name__ == '__main__':
    wrapper = AlphaFoldWrapper()
    tp53 = wrapper.lookup('TP53')
    if tp53:
        print(f"{tp53.gene_name}: {tp53.protein_name}")
        print(f"Domains: {', '.join(tp53.domains)}")
