#!/bin/bash
echo "Creating Genomics MCP project structure..."

# Create directories
mkdir -p templates static/css static/js

# Create requirements.txt
cat > requirements.txt << 'REQS'
requests>=2.28.0
Flask==2.3.2
Werkzeug==2.3.6
Gunicorn==20.1.0
python-dotenv==1.0.0
REQS

echo "✓ Created directories and requirements.txt"
echo "Ready for me to create all the Python files!"
