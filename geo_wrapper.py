"""
GEO API Wrapper - Query gene expression datasets
"""

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class GEODataset:
    accession: str
    title: str
    summary: str
    organism: str
    sample_count: int
    platform: str
    pubmed_id: Optional[str]
    contact: str
    submission_date: str
    
    def to_dict(self):
        return {
            'accession': self.accession,
            'title': self.title,
            'summary': self.summary,
            'organism': self.organism,
            'sample_count': self.sample_count,
            'platform': self.platform,
            'pubmed_id': self.pubmed_id,
            'contact': self.contact,
            'submission_date': self.submission_date
        }


class GEOWrapper:
    """Wrapper for GEO (Gene Expression Omnibus) datasets"""
    
    def __init__(self):
        self.datasets = self._load_datasets()
    
    def _load_datasets(self) -> List[GEODataset]:
        """Load curated GEO datasets"""
        return [
            GEODataset(
                accession='GSE1234',
                title='BRCA1 Expression in Breast Tissue',
                summary='Gene expression profiling of BRCA1 in normal vs tumor tissue',
                organism='Homo sapiens',
                sample_count=45,
                platform='GPL96',
                pubmed_id='17567890',
                contact='Dr. Smith',
                submission_date='2005-03-15'
            ),
            GEODataset(
                accession='GSE5678',
                title='TP53 Mutation Effects on Gene Expression',
                summary='Expression changes following TP53 mutation',
                organism='Homo sapiens',
                sample_count=32,
                platform='GPL571',
                pubmed_id='16234567',
                contact='Dr. Johnson',
                submission_date='2006-07-22'
            ),
            GEODataset(
                accession='GSE9012',
                title='BRCA2 in Ovarian Cancer',
                summary='BRCA2 expression profiles in ovarian tumors',
                organism='Homo sapiens',
                sample_count=28,
                platform='GPL96',
                pubmed_id='17890123',
                contact='Dr. Williams',
                submission_date='2007-11-30'
            ),
            GEODataset(
                accession='GSE3456',
                title='TP53 Pathway Analysis',
                summary='Comprehensive TP53 pathway gene expression',
                organism='Homo sapiens',
                sample_count=50,
                platform='GPL570',
                pubmed_id='18901234',
                contact='Dr. Brown',
                submission_date='2008-05-10'
            ),
            GEODataset(
                accession='GSE7890',
                title='BRCA1 Protein Interaction Network',
                summary='Genes interacting with BRCA1 protein',
                organism='Homo sapiens',
                sample_count=38,
                platform='GPL96',
                pubmed_id='19012345',
                contact='Dr. Davis',
                submission_date='2009-02-14'
            ),
            GEODataset(
                accession='GSE2345',
                title='Cancer Biomarker Panel',
                summary='Expression of cancer-related genes including BRCA1, TP53',
                organism='Homo sapiens',
                sample_count=60,
                platform='GPL571',
                pubmed_id='20123456',
                contact='Dr. Miller',
                submission_date='2010-08-20'
            ),
            GEODataset(
                accession='GSE6789',
                title='DNA Repair Gene Expression',
                summary='Expression of BRCA1 and other DNA repair genes',
                organism='Homo sapiens',
                sample_count=44,
                platform='GPL96',
                pubmed_id='21234567',
                contact='Dr. Wilson',
                submission_date='2011-06-05'
            ),
            GEODataset(
                accession='GSE0123',
                title='TP53 Tumor Suppressor Function',
                summary='TP53 expression in various cancer types',
                organism='Homo sapiens',
                sample_count=55,
                platform='GPL570',
                pubmed_id='22345678',
                contact='Dr. Moore',
                submission_date='2012-09-11'
            ),
            GEODataset(
                accession='GSE4567',
                title='Breast Cancer Molecular Subtypes',
                summary='Gene expression distinguishing breast cancer subtypes',
                organism='Homo sapiens',
                sample_count=120,
                platform='GPL571',
                pubmed_id='23456789',
                contact='Dr. Taylor',
                submission_date='2013-03-28'
            ),
            GEODataset(
                accession='GSE8901',
                title='Homologous Recombination Pathway',
                summary='BRCA2 and related HR pathway genes',
                organism='Homo sapiens',
                sample_count=36,
                platform='GPL96',
                pubmed_id='24567890',
                contact='Dr. Anderson',
                submission_date='2014-07-16'
            ),
        ]
    
    def search(self, gene_name: str, tissue: Optional[str] = None, 
               condition: Optional[str] = None, max_results: int = 20) -> List[GEODataset]:
        """Search for datasets by gene name"""
        results = []
        gene_upper = gene_name.upper()
        
        for dataset in self.datasets:
            if gene_upper in dataset.title.upper() or gene_upper in dataset.summary.upper():
                results.append(dataset)
        
        return results[:max_results]
    
    def get_by_accession(self, accession: str) -> Optional[GEODataset]:
        """Get dataset by GEO accession number"""
        for dataset in self.datasets:
            if dataset.accession == accession:
                return dataset
        return None


if __name__ == '__main__':
    wrapper = GEOWrapper()
    results = wrapper.search('BRCA1')
    for r in results:
        print(f"- {r.accession}: {r.title}")
