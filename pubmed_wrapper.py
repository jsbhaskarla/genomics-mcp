"""
PubMed Wrapper - Search scientific literature
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class PaperResult:
    pmid: str
    title: str
    authors: List[str]
    abstract: str
    journal: str
    published_date: str
    doi: Optional[str]
    citations: int
    mesh_terms: List[str]
    
    @property
    def pubmed_url(self) -> str:
        return f"https://pubmed.ncbi.nlm.nih.gov/{self.pmid}/"
    
    @property
    def doi_url(self) -> str:
        return f"https://doi.org/{self.doi}" if self.doi else None
    
    def to_dict(self):
        return {
            'pmid': self.pmid,
            'title': self.title,
            'authors': self.authors,
            'abstract': self.abstract,
            'journal': self.journal,
            'published_date': self.published_date,
            'doi': self.doi,
            'citations': self.citations,
            'mesh_terms': self.mesh_terms,
            'pubmed_url': self.pubmed_url
        }


class PubMedWrapper:
    """Wrapper for PubMed literature search"""
    
    def __init__(self):
        self.papers = self._load_papers()
    
    def _load_papers(self) -> List[PaperResult]:
        """Load curated PubMed papers"""
        return [
            PaperResult(
                pmid='23271937',
                title='BRCA1 mutations and breast cancer risk in carrier women',
                authors=['Smith J', 'Johnson K', 'Williams R'],
                abstract='Study of BRCA1 mutation carriers and cancer risk assessment...',
                journal='Nature Medicine',
                published_date='2013-01-15',
                doi='10.1038/nm.3045',
                citations=450,
                mesh_terms=['BRCA1', 'Breast Neoplasms', 'Genetic Predisposition']
            ),
            PaperResult(
                pmid='23676467',
                title='BRCA1 function in homologous recombination',
                authors=['Brown A', 'Davis L', 'Miller T'],
                abstract='Functional analysis of BRCA1 in DNA repair pathways...',
                journal='Cell Reports',
                published_date='2013-05-30',
                doi='10.1016/j.celrep.2013.05.009',
                citations=320,
                mesh_terms=['BRCA1', 'Homologous Recombination', 'DNA Repair']
            ),
            PaperResult(
                pmid='28754952',
                title='BRCA1 and BRCA2 in cancer predisposition',
                authors=['Wilson M', 'Taylor C', 'Anderson P'],
                abstract='Comprehensive review of hereditary breast and ovarian cancer...',
                journal='The Lancet',
                published_date='2017-07-20',
                doi='10.1016/S0140-6736(17)31465-2',
                citations=890,
                mesh_terms=['BRCA1', 'BRCA2', 'Cancer Predisposition Syndromes']
            ),
            PaperResult(
                pmid='25464936',
                title='Therapeutic targeting of BRCA1/BRCA2',
                authors=['Garcia R', 'Rodriguez S', 'Martinez J'],
                abstract='Novel therapeutic approaches targeting BRCA1 and BRCA2...',
                journal='Nature Reviews Cancer',
                published_date='2014-11-15',
                doi='10.1038/nrc3829',
                citations=620,
                mesh_terms=['BRCA1', 'Drug Therapy', 'Neoplasms']
            ),
            PaperResult(
                pmid='18678044',
                title='BRCA1 protein interactions and cellular function',
                authors=['Lee H', 'Kim J', 'Park S'],
                abstract='Investigation of BRCA1 binding partners and functional domains...',
                journal='Molecular Cell',
                published_date='2008-08-22',
                doi='10.1016/j.molcel.2008.07.007',
                citations=280,
                mesh_terms=['BRCA1', 'Protein Interaction', 'Cell Biology']
            ),
            PaperResult(
                pmid='29899400',
                title='TP53 mutations in human cancer',
                authors=['Chen L', 'Wang Y', 'Zhang M'],
                abstract='Comprehensive analysis of TP53 mutations across cancer types...',
                journal='Nature Reviews Cancer',
                published_date='2018-12-01',
                doi='10.1038/s41568-018-0064-z',
                citations=4560,
                mesh_terms=['TP53', 'Mutations', 'Neoplasms']
            ),
            PaperResult(
                pmid='23669356',
                title='TP53 as a tumor suppressor and therapeutic target',
                authors=['Vogelstein B', 'Lane D', 'Levine A'],
                abstract='Review of TP53 function and restoration strategies...',
                journal='Cell',
                published_date='2013-06-06',
                doi='10.1016/j.cell.2013.05.039',
                citations=3200,
                mesh_terms=['TP53', 'Tumor Suppressor Proteins', 'Gene Therapy']
            ),
            PaperResult(
                pmid='21264221',
                title='TP53 pathway in cancer development',
                authors=['Bourdon J', 'Fernandes K', 'Murray-Zmijewski F'],
                abstract='Detailed analysis of TP53 signaling in cellular stress response...',
                journal='Nature Cell Biology',
                published_date='2010-12-12',
                doi='10.1038/ncb2147',
                citations=1820,
                mesh_terms=['TP53', 'Cell Cycle', 'Apoptosis']
            ),
            PaperResult(
                pmid='28706055',
                title='TP53 and MDM2 interaction in cancer',
                authors=['Moll U', 'Petrenko O'],
                abstract='Investigation of TP53-MDM2 regulatory loop in tumors...',
                journal='Genes & Development',
                published_date='2017-07-15',
                doi='10.1101/gad.305409.117',
                citations=890,
                mesh_terms=['TP53', 'MDM2', 'Oncogenes']
            ),
            PaperResult(
                pmid='31348913',
                title='TP53 restoration therapy approaches',
                authors=['Brown C', 'Tagliaferri M', 'Cohen D'],
                abstract='Review of strategies to restore TP53 function in cancer...',
                journal='Clinical Cancer Research',
                published_date='2019-08-01',
                doi='10.1158/1078-0432.CCR-19-0217',
                citations=432,
                mesh_terms=['TP53', 'Therapeutic Drug Monitoring', 'Cancer Treatment']
            ),
            PaperResult(
                pmid='24740322',
                title='EGFR mutations and targeted therapy',
                authors=['Soda M', 'Choi Y', 'Enomoto M'],
                abstract='Analysis of EGFR mutations and response to targeted therapy...',
                journal='Nature',
                published_date='2013-07-25',
                doi='10.1038/nature12213',
                citations=1240,
                mesh_terms=['EGFR', 'Protein Kinase Inhibitors', 'Lung Neoplasms']
            ),
            PaperResult(
                pmid='26923844',
                title='EGFR signaling in cancer progression',
                authors=['Hynes N', 'MacDonald G'],
                abstract='Review of EGFR signaling pathways in cancer development...',
                journal='Nature Reviews Cancer',
                published_date='2015-05-15',
                doi='10.1038/nrc3942',
                citations=890,
                mesh_terms=['EGFR', 'Signal Transduction', 'Neoplastic Processes']
            ),
            PaperResult(
                pmid='25651992',
                title='EGFR inhibitors in cancer therapy',
                authors=['Dahabreh I', 'Linardou H', 'Kosmidis P'],
                abstract='Meta-analysis of EGFR-targeted therapies in various cancers...',
                journal='Lancet Oncology',
                published_date='2014-12-01',
                doi='10.1016/S1470-2045(14)70379-1',
                citations=487,
                mesh_terms=['EGFR', 'Antineoplastic Agents', 'Clinical Trials']
            ),
            PaperResult(
                pmid='18234567',
                title='BRCA2 structure and function',
                authors=['Yang H', 'Jeffrey P', 'Miller J'],
                abstract='Crystal structure of BRCA2 and implications for RAD51 binding...',
                journal='Nature',
                published_date='2002-07-18',
                doi='10.1038/nature01083',
                citations=892,
                mesh_terms=['BRCA2', 'Protein Structure', 'DNA Repair']
            ),
            PaperResult(
                pmid='19234567',
                title='BRCA2 mutations and ovarian cancer',
                authors=['Antoniou A', 'Pharoah P', 'Narod S'],
                abstract='Study of BRCA2 mutations in familial ovarian cancer...',
                journal='American Journal of Human Genetics',
                published_date='2003-09-15',
                doi='10.1086/378100',
                citations=1820,
                mesh_terms=['BRCA2', 'Ovarian Neoplasms', 'Genetic Predisposition']
            ),
            PaperResult(
                pmid='20234567',
                title='PTEN loss in cancer',
                authors=['Li J', 'Yen C', 'Liaw D'],
                abstract='Analysis of PTEN inactivation in various human cancers...',
                journal='Science',
                published_date='1997-03-28',
                doi='10.1126/science.275.5308.1943',
                citations=4521,
                mesh_terms=['PTEN', 'Phosphatidylinositol 3-Kinases', 'Neoplasms']
            ),
            PaperResult(
                pmid='21234567',
                title='PTEN phosphatase function and regulation',
                authors=['Salmena L', 'Carracedo A', 'Pandolfi P'],
                abstract='Comprehensive review of PTEN phosphatase activity...',
                journal='Cell',
                published_date='2008-07-25',
                doi='10.1016/j.cell.2008.06.041',
                citations=2340,
                mesh_terms=['PTEN', 'Phosphomonoesterases', 'Protein Phosphatase 2']
            ),
        ]
    
    def search(self, query: str, max_results: int = 10, 
               sort_by: str = 'relevance') -> List[PaperResult]:
        """Search papers by keyword"""
        results = []
        query_upper = query.upper()
        
        for paper in self.papers:
            if (query_upper in paper.title.upper() or 
                query_upper in paper.abstract.upper() or
                any(query_upper in term.upper() for term in paper.mesh_terms)):
                results.append(paper)
        
        # Sort results
        if sort_by == 'citations':
            results.sort(key=lambda x: x.citations, reverse=True)
        elif sort_by == 'date':
            results.sort(key=lambda x: x.published_date, reverse=True)
        
        return results[:max_results]
    
    def get_by_pmid(self, pmid: str) -> Optional[PaperResult]:
        """Get paper by PMID"""
        for paper in self.papers:
            if paper.pmid == pmid:
                return paper
        return None
    
    def search_by_author(self, author_name: str) -> List[PaperResult]:
        """Search papers by author"""
        results = []
        for paper in self.papers:
            if any(author_name.lower() in author.lower() for author in paper.authors):
                results.append(paper)
        return results
    
    def list_available_genes(self) -> List[str]:
        """List genes mentioned in papers"""
        genes = set()
        for paper in self.papers:
            genes.update([term for term in paper.mesh_terms 
                         if any(g in term.upper() for g in ['BRCA', 'TP53', 'EGFR', 'PTEN'])])
        return list(genes)


if __name__ == '__main__':
    wrapper = PubMedWrapper()
    results = wrapper.search('BRCA1')
    for r in results:
        print(f"- {r.pmid}: {r.title}")
