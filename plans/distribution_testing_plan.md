# Distribution Testing Plan

## Testing Strategy

### Goal
Verify that the simplified Phase 5 distribution approach works correctly before deployment to lab colleagues.

## Test Environment Setup

### Test Scenario: Clean macOS System
Simulate a lab colleague's computer by testing on a clean environment:

1. **Create test directory**: Separate from development environment
2. **Use different conda environment**: Avoid conflicts with `microwell-gui-dev`
3. **Test from scratch**: Follow user installation instructions exactly

## Testing Steps

### 1. Package Creation Test
```bash
# Create distribution package
mkdir microwell-plate-gui-dist
cd microwell-plate-gui-dist

# Copy essential files
cp ../run_app.py .
cp -r ../src .
cp ../example_database.db .
cp ../example_database.csv .

# Create production environment file (from plans/production_environment_spec.md)
# Create launcher script (from plans/launcher_script_design.md)
# Create README.md (from plans/user_installation_instructions.md)
```

### 2. Environment Creation Test
```bash
# Test conda environment creation
conda env create -f environment.yml

# Verify environment contents
conda activate microwell-plate-gui
conda list

# Check key dependencies
python -c "import tkinter; print('tkinter: OK')"
python -c "import sqlite3; print('sqlite3: OK')"
python -c "import pandas; print('pandas: OK')"
```

### 3. Application Launch Test
```bash
# Test launcher script
chmod +x launch_microwell_gui.sh
./launch_microwell_gui.sh

# Verify application starts
# Test basic functionality:
# - Startup dialog appears
# - Plate canvas loads
# - Metadata panel works
# - CSV export functions
```

### 4. Error Handling Test
```bash
# Test error scenarios
# 1. Missing conda
PATH="/usr/bin:/bin" ./launch_microwell_gui.sh

# 2. Missing environment
conda env remove -n microwell-plate-gui
./launch_microwell_gui.sh

# 3. Wrong directory
cd /tmp
/path/to/launch_microwell_gui.sh
```

## Validation Checklist

### Environment Validation
- [ ] Environment creates successfully from `environment.yml`
- [ ] All dependencies install with correct versions
- [ ] Python 3.11.14 is installed
- [ ] tkinter, sqlite3, pandas are available
- [ ] No development dependencies (pytest, etc.) are included

### Application Validation
- [ ] Application launches without errors
- [ ] Startup dialog appears and functions
- [ ] Plate canvas displays correctly
- [ ] Well selection works
- [ ] Metadata panel loads
- [ ] Database connection works
- [ ] CSV export functions
- [ ] PDF export functions
- [ ] Application exits cleanly

### Launcher Validation
- [ ] Script is executable
- [ ] Conda environment activates automatically
- [ ] Error messages are helpful and actionable
- [ ] Application launches successfully
- [ ] Script handles missing conda gracefully
- [ ] Script handles missing environment gracefully
- [ ] Script validates working directory

### User Experience Validation
- [ ] Installation instructions are clear
- [ ] Setup takes ~5 minutes as advertised
- [ ] Daily usage is simple (single command)
- [ ] Error messages guide users to solutions
- [ ] Troubleshooting section covers common issues

## Success Criteria

### Technical Success
- Environment creates deterministically
- Application runs identically to development version
- All core features function properly
- Error handling works as designed

### User Success
- Lab colleague can follow instructions independently
- Setup process is straightforward
- Daily usage is simple and reliable
- Support burden is minimal

## Test Documentation

### Record Results
- Environment creation output
- Application startup logs
- Feature testing results
- Error scenario outcomes
- Performance observations

### Package Refinement
Based on testing results:
- Update environment.yml if needed
- Refine launcher script error handling
- Improve installation instructions
- Add missing troubleshooting scenarios

This testing approach ensures the distribution package works reliably before sharing with lab colleagues.