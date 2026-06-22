"""
Bedrock Agent - AI reasoning layer for genomics queries
"""

from typing import List, Dict, Any
from mcp_server import GenomicsMCPServer


class GenomicsAgent:
    """AI Agent for genomics queries"""
    
    SYSTEM_PROMPT = """You are an expert genomics research assistant specializing in cancer biology 
    and molecular genetics. You have access to three data sources:
    1. GEO - Gene expression datasets
    2. AlphaFold - Protein structures
    3. PubMed - Scientific literature
    
    When answering questions:
    - Detect which genes are being asked about
    - Route to appropriate tools based on question type
    - Synthesize information from multiple sources
    - Provide mechanistic insights
    - Always cite data sources"""
    
    SUPPORTED_GENES = ['BRCA1', 'BRCA2', 'TP53', 'EGFR', 'PTEN']
    
    def __init__(self, verbose: bool = True):
        self.server = GenomicsMCPServer()
        self.verbose = verbose
        self.conversation_history = []
        self.tool_calls = []
    
    def answer_question(self, question: str) -> str:
        """Answer a genomics question"""
        self.conversation_history.append({
            'role': 'user',
            'content': question
        })
        
        # Detect genes
        genes = self._detect_genes(question)
        
        # Classify question type
        question_type = self._classify_question(question)
        
        # Route to appropriate analysis
        if 'structure' in question_type:
            answer = self._analyze_protein_structure(genes, question)
        elif 'literature' in question_type:
            answer = self._analyze_literature(genes, question)
        elif 'expression' in question_type:
            answer = self._analyze_expression(genes, question)
        else:
            answer = self._comprehensive_analysis(genes, question)
        
        self.conversation_history.append({
            'role': 'assistant',
            'content': answer
        })
        
        return answer
    
    def _detect_genes(self, text: str) -> List[str]:
        """Detect genes mentioned in text"""
        detected = []
        text_upper = text.upper()
        for gene in self.SUPPORTED_GENES:
            if gene in text_upper:
                detected.append(gene)
        return detected
    
    def _classify_question(self, question: str) -> List[str]:
        """Classify question type"""
        q_lower = question.lower()
        types = []
        
        if any(word in q_lower for word in ['domain', 'structure', 'binding', 'protein']):
            types.append('structure')
        if any(word in q_lower for word in ['paper', 'literature', 'published', 'study']):
            types.append('literature')
        if any(word in q_lower for word in ['expression', 'dataset', 'tissue', 'experiment']):
            types.append('expression')
        
        return types if types else ['comprehensive']
    
    def _analyze_protein_structure(self, genes: List[str], question: str) -> str:
        """Analyze protein structure"""
        if not genes:
            return "No genes detected. Please mention a gene name (BRCA1, BRCA2, TP53, EGFR, or PTEN)."
        
        answers = []
        for gene in genes:
            result = self.server.call_tool('lookup_protein_structure', gene_name=gene)
            self.tool_calls.append({'tool': 'lookup_protein_structure', 'success': result['success']})
            
            if result['success']:
                protein = result['protein']
                answer = f"**{gene} - {protein['protein_name']}**\n\n"
                answer += f"- **Length:** {protein['length_amino_acids']} amino acids\n"
                answer += f"- **UniProt ID:** {protein['uniprot_id']}\n"
                answer += f"- **Domains:** {', '.join(protein['domains'])}\n"
                answer += f"- **PDB Structures:** {', '.join(protein['pdb_ids'])}\n"
                answer += f"- **AlphaFold pLDDT:** {protein['plddt_score']}\n"
                answer += f"- **Binding Sites:** {', '.join(protein['binding_sites'])}\n"
                answers.append(answer)
        
        return '\n\n'.join(answers) if answers else "No protein structure data found."
    
    def _analyze_literature(self, genes: List[str], question: str) -> str:
        """Analyze scientific literature"""
        if not genes:
            genes = ['BRCA1', 'TP53']  # Default
        
        all_papers = []
        for gene in genes:
            result = self.server.call_tool('search_pubmed', query=gene, max_results=5)
            self.tool_calls.append({'tool': 'search_pubmed', 'success': result['success']})
            
            if result['success']:
                all_papers.extend(result['results'])
        
        if not all_papers:
            return "No papers found."
        
        answer = f"**Found {len(all_papers)} relevant papers:**\n\n"
        for paper in all_papers[:5]:
            answer += f"- **{paper['title']}** ({paper['published_date']})\n"
            answer += f"  Authors: {', '.join(paper['authors'][:3])}\n"
            answer += f"  Citations: {paper['citations']}\n"
            answer += f"  URL: {paper['pubmed_url']}\n\n"
        
        return answer
    
    def _analyze_expression(self, genes: List[str], question: str) -> str:
        """Analyze gene expression"""
        if not genes:
            return "No genes detected. Please mention a gene name."
        
        answers = []
        for gene in genes:
            result = self.server.call_tool('search_geo_datasets', gene_name=gene, max_results=5)
            self.tool_calls.append({'tool': 'search_geo_datasets', 'success': result['success']})
            
            if result['success']:
                datasets = result['results']
                answer = f"**{gene} Expression Datasets ({len(datasets)} found):**\n\n"
                for ds in datasets:
                    answer += f"- **{ds['accession']}:** {ds['title']}\n"
                    answer += f"  Samples: {ds['sample_count']}, Platform: {ds['platform']}\n\n"
                answers.append(answer)
        
        return '\n'.join(answers) if answers else "No expression data found."
    
    def _comprehensive_analysis(self, genes: List[str], question: str) -> str:
        """Comprehensive analysis of genes"""
        if not genes:
            genes = self.SUPPORTED_GENES
        
        answers = []
        for gene in genes:
            result = self.server.call_tool('analyze_gene', gene_name=gene)
            self.tool_calls.append({'tool': 'analyze_gene', 'success': result['success']})
            
            if result['success']:
                answer = f"## {gene} - Comprehensive Analysis\n\n"
                answer += f"{result['summary']}\n\n"
                
                # Expression data
                if result['expression_datasets']:
                    answer += f"### Expression Data ({len(result['expression_datasets'])} datasets)\n"
                    for ds in result['expression_datasets'][:3]:
                        answer += f"- {ds['accession']}: {ds['title']}\n"
                    answer += "\n"
                
                # Protein structure
                if result['protein_structure']:
                    ps = result['protein_structure']
                    answer += f"### Protein Structure\n"
                    answer += f"- Domains: {', '.join(ps['domains'])}\n"
                    answer += f"- Length: {ps['length_amino_acids']} aa\n"
                    answer += f"- PDB: {', '.join(ps['pdb_ids'])}\n\n"
                
                # Literature
                if result['papers']:
                    answer += f"### Key Papers ({len(result['papers'])} papers)\n"
                    for paper in result['papers'][:3]:
                        answer += f"- {paper['title']}\n"
                    answer += "\n"
                
                answers.append(answer)
        
        return '\n'.join(answers) if answers else "No data found."
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def get_tool_calls(self) -> List[Dict]:
        """Get tool call history"""
        return self.tool_calls
    
    def reset(self):
        """Reset agent state"""
        self.conversation_history = []
        self.tool_calls = []


if __name__ == '__main__':
    agent = GenomicsAgent()
    answer = agent.answer_question("What domains does BRCA1 have?")
    print(answer)
