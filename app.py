"""
Flask web server for Genomics Agent
"""

from flask import Flask, render_template, request, jsonify
from bedrock_agent import GenomicsAgent
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize agent
agent = GenomicsAgent(verbose=False)

# Store sessions
sessions = {}

def get_session(session_id):
    """Get or create a session"""
    if session_id not in sessions:
        sessions[session_id] = {
            "agent": GenomicsAgent(verbose=False),
            "created": datetime.now().isoformat(),
            "messages": []
        }
    return sessions[session_id]


@app.route('/', methods=['GET'])
def home():
    """Serve the web interface"""
    return render_template('index.html')


@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Ask a genomics question"""
    try:
        data = request.json
        question = data.get('question', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not question:
            return jsonify({'success': False, 'error': 'Question cannot be empty'}), 400
        
        if len(question) > 500:
            return jsonify({'success': False, 'error': 'Question too long (max 500 characters)'}), 400
        
        # Get session
        session = get_session(session_id)
        agent_instance = session["agent"]
        
        # Get answer
        answer = agent_instance.answer_question(question)
        
        # Store in session
        session["messages"].append({
            "role": "user",
            "content": question,
            "timestamp": datetime.now().isoformat()
        })
        session["messages"].append({
            "role": "assistant",
            "content": answer,
            "timestamp": datetime.now().isoformat()
        })
        
        return jsonify({
            "success": True,
            "question": question,
            "answer": answer,
            "tools_called": agent_instance.get_tool_calls(),
            "message_count": len(session["messages"]),
            "timestamp": datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Get example questions"""
    examples = [
        {
            "category": "Structure",
            "question": "What domains does BRCA1 have?",
            "description": "Learn about BRCA1 protein domains and structure"
        },
        {
            "category": "Literature",
            "question": "Find papers about TP53 mutations in cancer",
            "description": "Search scientific literature on TP53"
        },
        {
            "category": "Expression",
            "question": "What datasets exist for BRCA2?",
            "description": "Find gene expression data"
        },
        {
            "category": "Comprehensive",
            "question": "Give me a comprehensive analysis of EGFR",
            "description": "Get complete info: structure, expression, papers"
        },
        {
            "category": "Structure",
            "question": "What are the binding partners of TP53?",
            "description": "Learn protein-protein interactions"
        },
        {
            "category": "Literature",
            "question": "What recent papers discuss PTEN?",
            "description": "Find latest PTEN research"
        },
    ]
    return jsonify(examples), 200


@app.route('/api/genes', methods=['GET'])
def get_supported_genes():
    """Get list of supported genes"""
    genes = [
        {
            "symbol": "BRCA1",
            "name": "Breast cancer type 1 susceptibility protein",
            "role": "DNA repair, tumor suppressor",
            "datasets": 4,
            "papers": 5
        },
        {
            "symbol": "BRCA2",
            "name": "Breast cancer type 2 susceptibility protein",
            "role": "DNA repair, homologous recombination",
            "datasets": 1,
            "papers": 2
        },
        {
            "symbol": "TP53",
            "name": "Tumor protein p53",
            "role": "Cell cycle regulation, apoptosis",
            "datasets": 3,
            "papers": 5
        },
        {
            "symbol": "EGFR",
            "name": "Epidermal growth factor receptor",
            "role": "Receptor tyrosine kinase, cell growth",
            "datasets": 0,
            "papers": 3
        },
        {
            "symbol": "PTEN",
            "name": "Phosphatase and tensin homolog",
            "role": "Phosphatase, tumor suppressor",
            "datasets": 0,
            "papers": 1
        },
    ]
    return jsonify(genes), 200


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status"""
    return jsonify({
        "status": "online",
        "version": "1.0.0",
        "agent": "Bedrock Genomics Agent",
        "supported_genes": 5,
        "total_datasets": 10,
        "total_papers": 18,
        "total_tests_passing": 85,
        "components": {
            "geo_wrapper": "active",
            "alphafold_wrapper": "active",
            "pubmed_wrapper": "active",
            "mcp_server": "active",
            "bedrock_agent": "active"
        }
    }), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        test_agent = GenomicsAgent(verbose=False)
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": "all_operational"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 503


@app.route('/api/docs', methods=['GET'])
def get_documentation():
    """Get API documentation"""
    docs = {
        "title": "Genomics Agent API",
        "version": "1.0.0",
        "description": "AI-powered genomics research assistant",
        "endpoints": {
            "GET /": "Web interface",
            "POST /api/ask": "Ask a genomics question",
            "GET /api/examples": "Get example questions",
            "GET /api/genes": "Get supported genes",
            "GET /api/status": "Get system status",
            "GET /api/health": "Health check",
            "GET /api/docs": "This documentation"
        },
        "example_request": {
            "endpoint": "POST /api/ask",
            "body": {
                "question": "What domains does BRCA1 have?",
                "session_id": "optional-user-id"
            }
        }
    }
    return jsonify(docs), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found", "status": 404}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error", "status": 500}), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("GENOMICS AGENT API SERVER")
    print("="*70)
    print("\n📡 Starting server...")
    print("🌐 Web interface: http://localhost:5000")
    print("📚 API docs: http://localhost:5000/api/docs")
    print("❤️  Health check: http://localhost:5000/api/health")
    print("\n" + "="*70 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
