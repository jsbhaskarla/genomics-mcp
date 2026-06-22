"""
MCP Server - Tool orchestration for genomics queries
"""

from typing import Dict, Any, List
from geo_wrapper import GEOWrapper
from alphafold_wrapper import AlphaFoldWrapper
from pubmed_wrapper import PubMedWrapper


class GenomicsMCPServer:
    """MCP Server for genomics tools"""
    
    def __init__(self):
        self.geo = GEOWrapper()
        self.alphafold = AlphaFoldWrapper()
        self.pubmed = PubMedWrapper()
        self.tools = self._register_tools()
    
    def _register_tools(self) -> Dict[str, Any]:
        """Register available tools"""
        return {
            'search_geo_datasets': {
                'description': 'Search gene expression datasets',
                'parameters': ['gene_name', 'tissue', 'condition', 'max_results']
            },
            'lookup_protein_structure': {
                'description': 'Look up protein structure information',
                'parameters': ['gene_name', 'by_uniprot', 'by_pdb']
            },
            'search_pubmed': {
                'description': 'Search scientific literature',
                'parameters': ['query', 'by_author', 'by_pmid', 'max_results', 'sort_by']
            },
            'analyze_gene': {
                'description': 'Comprehensive gene analysis (all sources)',
                'parameters': ['gene_name']
            }
        }
    
    def get_tools(self) -> Dict[str, Any]:
        """Get registered tools"""
        return self.tools
    
    def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Call a tool"""
        try:
            if tool_name == 'search_geo_datasets':
                return self._search_geo_datasets(**kwargs)
            elif tool_name == 'lookup_protein_structure':
                return self._lookup_protein_structure(**kwargs)
            elif tool_name == 'search_pubmed':
                return self._search_pubmed(**kwargs)
            elif tool_name == 'analyze_gene':
                return self._analyze_gene(**kwargs)
            else:
                return {'success': False, 'error': f'Unknown tool: {tool_name}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _search_geo_datasets(self, gene_name: str = None, tissue: str = None,
                            condition: str = None, max_results: int = 20) -> Dict[str, Any]:
        """Search GEO datasets"""
        if not gene_name:
            return {'success': False, 'error': 'gene_name required'}
        
        results = self.geo.search(gene_name, tissue, condition, max_results)
        return {
            'success': True,
            'tool': 'search_geo_datasets',
            'gene': gene_name,
            'results': [r.to_dict() for r in results],
            'count': len(results)
        }
    
    def _lookup_protein_structure(self, gene_name: str = None, by_uniprot: str = None,
                                 by_pdb: str = None) -> Dict[str, Any]:
        """Look up protein structure"""
        protein = None
        
        if gene_name:
            protein = self.alphafold.lookup(gene_name)
        elif by_uniprot:
            protein = self.alphafold.get_by_uniprot(by_uniprot)
        elif by_pdb:
            protein = self.alphafold.get_by_pdb(by_pdb)
        else:
            return {'success': False, 'error': 'gene_name, by_uniprot, or by_pdb required'}
        
        if not protein:
            return {'success': False, 'error': 'Protein not found'}
        
        return {
            'success': True,
            'tool': 'lookup_protein_structure',
            'protein': protein.to_dict()
        }
    
    def _search_pubmed(self, query: str = None, by_author: str = None,
                      by_pmid: str = None, max_results: int = 10,
                      sort_by: str = 'relevance') -> Dict[str, Any]:
        """Search PubMed"""
        results = []
        
        if query:
            results = self.pubmed.search(query, max_results, sort_by)
        elif by_author:
            results = self.pubmed.search_by_author(by_author)[:max_results]
        elif by_pmid:
            paper = self.pubmed.get_by_pmid(by_pmid)
            results = [paper] if paper else []
        else:
            return {'success': False, 'error': 'query, by_author, or by_pmid required'}
        
        return {
            'success': True,
            'tool': 'search_pubmed',
            'query': query or by_author or by_pmid,
            'results': [r.to_dict() for r in results],
            'count': len(results)
        }
    
    def _analyze_gene(self, gene_name: str) -> Dict[str, Any]:
        """Comprehensive gene analysis"""
        if not gene_name:
            return {'success': False, 'error': 'gene_name required'}
        
        # Get all data sources
        expression = self.geo.search(gene_name, max_results=5)
        protein = self.alphafold.lookup(gene_name)
        papers = self.pubmed.search(gene_name, max_results=5)
        
        return {
            'success': True,
            'tool': 'analyze_gene',
            'gene': gene_name,
            'expression_datasets': [r.to_dict() for r in expression],
            'protein_structure': protein.to_dict() if protein else None,
            'papers': [p.to_dict() for p in papers],
            'summary': f"Comprehensive analysis of {gene_name}: {len(expression)} datasets, "
                      f"{'protein structure available' if protein else 'no protein structure'}, "
                      f"{len(papers)} papers"
        }


def format_result(result: Dict[str, Any]) -> str:
    """Format result for display"""
    if not result.get('success'):
        return f"Error: {result.get('error', 'Unknown error')}"
    
    lines = [f"Tool: {result.get('tool')}"]
    lines.append(f"Status: {result.get('success')}")
    
    if 'count' in result:
        lines.append(f"Results: {result['count']}")
    
    return '\n'.join(lines)


if __name__ == '__main__':
    server = GenomicsMCPServer()
    result = server.call_tool('search_geo_datasets', gene_name='BRCA1')
    print(format_result(result))
