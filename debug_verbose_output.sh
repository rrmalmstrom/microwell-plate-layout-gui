#!/bin/bash
# Debug script to identify sources of verbose output
# This will help us understand what's generating the terminal noise

echo "=== DEBUGGING VERBOSE OUTPUT ==="
echo "Timestamp: $(date)"
echo ""

echo "1. Testing conda activation verbosity..."
# Test conda activation with different verbosity levels
if command -v conda &> /dev/null; then
    echo "   - Conda found, testing activation..."
    eval "$(conda shell.bash hook)"
    
    echo "   - Testing normal activation:"
    conda activate microwell-gui-dev 2>&1 | head -5
    
    echo "   - Testing quiet activation:"
    conda activate microwell-gui-dev 2>/dev/null && echo "   - Quiet activation successful"
else
    echo "   - Conda not found"
fi

echo ""
echo "2. Testing Python import verbosity..."
# Test if Python imports generate warnings
python -c "
import sys
import os
sys.path.insert(0, 'src')
try:
    from microwell_plate_gui.main import main
    print('   - Python imports: Clean')
except Exception as e:
    print(f'   - Python import error: {e}')
" 2>&1

echo ""
echo "3. Checking shell settings..."
echo "   - Current shell: $SHELL"
echo "   - Shell options: $-"
echo "   - BASH_SOURCE: ${BASH_SOURCE[0]}"

echo ""
echo "4. Testing terminal behavior..."
echo "   - PWD: $(pwd)"
echo "   - Script directory: $(dirname "${BASH_SOURCE[0]}")"

echo ""
echo "=== END DEBUG ==="