// Genomics Agent Web Interface

class GenomicsUI {
    constructor() {
        this.sessionId = `session-${Date.now()}`;
        this.chatHistory = document.getElementById('chatHistory');
        this.questionInput = document.getElementById('questionInput');
        this.questionForm = document.getElementById('questionForm');
        this.submitBtn = document.getElementById('submitBtn');
        this.charCount = document.getElementById('charCount');
        this.examplesList = document.getElementById('examplesList');
        this.genesList = document.getElementById('genesList');
        
        this.init();
    }
    
    async init() {
        await this.loadExamples();
        await this.loadGenes();
        
        this.questionForm.addEventListener('submit', (e) => this.handleSubmit(e));
        this.questionInput.addEventListener('input', (e) => this.updateCharCount(e));
        
        await this.checkHealth();
    }
    
    async loadExamples() {
        try {
            const response = await fetch('/api/examples');
            const examples = await response.json();
            
            this.examplesList.innerHTML = examples.map(ex => `
                <div class="example-item" onclick="ui.selectExample('${ex.question.replace(/'/g, "\\'")}')">
                    <div class="example-category">${ex.category}</div>
                    <div>${ex.question}</div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading examples:', error);
        }
    }
    
    async loadGenes() {
        try {
            const response = await fetch('/api/genes');
            const genes = await response.json();
            
            this.genesList.innerHTML = genes.map(gene => `
                <div class="gene-item" onclick="ui.selectGene('${gene.symbol}')">
                    <div class="gene-symbol">${gene.symbol}</div>
                    <div class="gene-info">
                        ${gene.papers} papers • ${gene.datasets} datasets
                    </div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading genes:', error);
        }
    }
    
    async checkHealth() {
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            
            if (data.status === 'healthy') {
                document.getElementById('statusBadge').textContent = '● Online';
            }
        } catch (error) {
            document.getElementById('statusBadge').textContent = '● Offline';
        }
    }
    
    selectExample(question) {
        this.questionInput.value = question;
        this.questionInput.focus();
    }
    
    selectGene(gene) {
        const currentValue = this.questionInput.value.trim();
        const newValue = currentValue 
            ? `${currentValue} ${gene}`
            : `Tell me about ${gene}`;
        this.questionInput.value = newValue;
        this.questionInput.focus();
    }
    
    updateCharCount(event) {
        this.charCount.textContent = event.target.value.length;
    }
    
    async handleSubmit(event) {
        event.preventDefault();
        
        const question = this.questionInput.value.trim();
        
        if (!question) {
            this.showError('Please enter a question');
            return;
        }
        
        this.submitBtn.disabled = true;
        this.submitBtn.classList.add('loading');
        this.questionInput.disabled = true;
        
        this.questionInput.value = '';
        this.charCount.textContent = '0';
        
        this.addMessage(question, 'user');
        
        try {
            const response = await fetch('/api/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    question: question,
                    session_id: this.sessionId
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.addMessage(data.answer, 'assistant');
            } else {
                this.showError(data.error || 'Failed to get answer');
            }
        } catch (error) {
            this.showError(`Error: ${error.message}`);
        } finally {
            this.submitBtn.disabled = false;
            this.submitBtn.classList.remove('loading');
            this.questionInput.disabled = false;
            this.questionInput.focus();
        }
    }
    
    addMessage(text, role) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = this.formatText(text);
        
        messageDiv.appendChild(contentDiv);
        
        const welcome = this.chatHistory.querySelector('.welcome-message');
        if (welcome && (this.chatHistory.querySelectorAll('.message').length === 0)) {
            welcome.remove();
        }
        
        this.chatHistory.appendChild(messageDiv);
        this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
    }
    
    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        this.chatHistory.appendChild(errorDiv);
        this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
    }
    
    formatText(text) {
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>')
            .replace(/\n/g, '<br>');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.ui = new GenomicsUI();
});

document.addEventListener('keydown', (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        const form = document.getElementById('questionForm');
        if (form) {
            form.dispatchEvent(new Event('submit'));
        }
    }
});
