# Coding Agent Instructions - Microwell Plate GUI

## CRITICAL REQUIREMENTS

### 1. Test-Driven Development (TDD) - MANDATORY
- **Write tests FIRST, then implement**
- Every function must have corresponding unit tests
- Run tests after each implementation step
- Achieve minimum 90% code coverage
- Use pytest framework for all testing

### 2. Context7 Integration - MANDATORY
- **ALWAYS** query Context7 before implementing any Tkinter functionality
- Reference Context7 for Python best practices and patterns
- Use Context7 to resolve any implementation questions
- Document Context7 queries and responses in code comments

### 3. Manual Verification Checkpoints - MANDATORY
- **STOP** after each phase for user testing
- Do NOT proceed to next phase without user approval
- Implement user feedback before continuing
- Document all user feedback and resolutions

## Implementation Order (STRICT)

### Phase 0: Development Environment Setup (MANDATORY FIRST STEP)
**MUST BE COMPLETED BEFORE ANY CODING BEGINS**

#### 0.1 Initial Environment Creation
**Context7 Query Required**: Research conda environment best practices and dependency management

**Steps**:
1. Create initial development environment on user's development computer
2. Test all basic dependencies work correctly
3. Document exact versions that work
4. Create baseline environment.yml file
5. Verify environment reproducibility

```bash
# Create initial development environment
conda create -n microwell-gui-dev python=3.11
conda activate microwell-gui-dev

# Install basic dependencies and test
conda install tkinter pytest sqlite pandas
python -c "import tkinter; print('Tkinter works')"
python -c "import sqlite3; print('SQLite works')"
python -c "import pytest; print('Pytest works')"

# Export working environment
conda env export > environment-dev.yml
conda list --explicit > environment-explicit.txt
```

#### 0.2 Environment Documentation and Pinning
**All dependencies MUST be pinned to exact versions**

**Create environment.yml with pinned versions**:
```yaml
name: microwell-gui
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11.5=h2755cc3_0
  - tkinter=8.6.12=py311h2755cc3_0
  - sqlite=3.42.0=h2bbff1b_0
  - pytest=7.4.0=py311haa95532_0
  - pytest-cov=4.1.0=py311haa95532_0
  - pandas=2.0.3=py311hf62ec03_0
  - pip=23.2.1=py311haa95532_0
  # Add more dependencies as discovered during development
```

#### 0.3 Environment Testing and Validation
**Test environment on user's development computer**:
```bash
# Remove test environment
conda env remove -n microwell-gui-test

# Recreate from environment.yml
conda env create -f environment.yml -n microwell-gui-test
conda activate microwell-gui-test

# Run validation tests
python -c "import tkinter; import sqlite3; import pytest; print('All imports successful')"
```

#### 0.4 Git Repository Setup
**MANDATORY**: Set up version control before any coding begins

**Local Repository Setup**:
```bash
# Initialize local git repository
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create initial project structure
mkdir -p src/microwell_plate_gui/{gui,data,utils}
mkdir -p tests/{test_gui,test_data,test_utils}
mkdir -p docs plans examples

# Create initial files
touch src/microwell_plate_gui/__init__.py
touch src/microwell_plate_gui/main.py
touch tests/__init__.py
touch README.md
touch .gitignore

# Initial commit
git add .
git commit -m "Initial project structure"
```

**GitHub Repository Setup**:
**IMPORTANT**: User must provide GitHub credentials and repository preferences

**Required Information from User**:
- GitHub username
- Repository name preference (suggest: microwell-plate-gui)
- Repository visibility (public/private)
- GitHub authentication method (SSH keys/Personal Access Token)

**GitHub Repository Creation**:
```bash
# Create repository on GitHub (user must do this step or provide credentials)
# Option 1: User creates repository manually on GitHub
# Option 2: Use GitHub CLI (if available)
gh repo create microwell-plate-gui --public --description "GUI tool for microwell plate layout design"

# Connect local repo to GitHub
git remote add origin https://github.com/USERNAME/microwell-plate-gui.git
# OR for SSH:
git remote add origin git@github.com:USERNAME/microwell-plate-gui.git

# Push initial commit
git branch -M main
git push -u origin main
```

**Git Workflow Protocol**:
- Commit after each significant change
- Push to GitHub after each phase completion
- Use descriptive commit messages
- Tag releases for each phase completion

#### 0.5 Dynamic Environment Management Protocol
**CRITICAL**: Environment must be updated throughout development

**After adding any new dependency**:
1. Test new dependency in development environment
2. Export updated environment: `conda env export > environment-updated.yml`
3. Pin exact versions of new dependencies
4. Test environment recreation from updated file
5. Update environment.yml with pinned versions
6. Commit changes to environment file
7. Push environment updates to GitHub

**Before each phase completion**:
1. Export current environment state
2. Test environment recreation
3. Update environment.yml with any new dependencies
4. Verify all tests pass in clean environment
5. Commit and push environment updates
6. Tag the release with phase completion

### Phase 1: Core Infrastructure
**STOP FOR USER TESTING AFTER THIS PHASE**

#### 1.1 Project Setup (Using Established Environment)
**MANDATORY**: Use the environment created in Phase 0

```bash
# Activate the established development environment
conda activate microwell-gui-dev

# Verify environment is correct
conda list
python -c "import tkinter; import sqlite3; import pytest; print('Environment ready')"
```

#### 1.2 Basic Application Structure
**Context7 Query Required**: Research Tkinter application architecture patterns

**Tests to Write First**:
```python
# test_main_window.py
def test_main_window_creation()
def test_plate_type_selection_dialog()
def test_window_layout_split_view()
```

**Implementation**:
- Create main application window with split layout
- Implement startup dialog for plate type selection (96/384)
- Basic window structure with placeholder panels

#### 1.3 Plate Canvas Foundation
**Context7 Query Required**: Research Tkinter Canvas widget for grid layouts

**Tests to Write First**:
```python
# test_plate_canvas.py
def test_canvas_creation()
def test_96_well_grid_layout()
def test_384_well_grid_layout()
def test_well_coordinate_calculation()
```

**Implementation**:
- Create Canvas widget for plate visualization
- Implement well grid calculation for both plate types
- Basic well rendering (circles with coordinates)

#### 1.4 Database Integration
**Context7 Query Required**: Research SQLite integration patterns in Python

**Tests to Write First**:
```python
# test_database.py
def test_database_connection()
def test_sample_data_loading()
def test_missing_database_handling()
def test_plate_name_generation()
```

**Implementation**:
- SQLite database reader class
- Sample data loading from database
- Graceful handling of missing database files
- Plate name generation logic

**USER TESTING CHECKPOINT**: User must verify basic application launches, displays correct plate grid, and loads database correctly.

### Phase 2: Metadata System
**STOP FOR USER TESTING AFTER THIS PHASE**

#### 2.1 Metadata Panel Creation
**Context7 Query Required**: Research Tkinter form widgets and layout management

**Tests to Write First**:
```python
# test_metadata_panel.py
def test_metadata_form_creation()
def test_dropdown_population()
def test_dynamic_plate_name_dropdown()
def test_form_validation()
```

**Implementation**:
- Create metadata entry form with all required fields
- Implement dropdown widgets with database integration
- Dynamic plate name dropdown based on sample selection
- Basic form validation

#### 2.2 Single Sample Workflow
**Context7 Query Required**: Research event handling and data binding in Tkinter

**Tests to Write First**:
```python
# test_single_sample_workflow.py
def test_sample_selection_updates_plate_names()
def test_metadata_application_to_wells()
def test_workflow_state_management()
```

**Implementation**:
- Complete single-sample workflow implementation
- Sample selection triggers plate name dropdown update
- Metadata application to selected wells
- State management for workflow

#### 2.3 Basic Well Selection
**Context7 Query Required**: Research Canvas mouse event handling and selection

**Tests to Write First**:
```python
# test_well_selection.py
def test_rectangular_drag_selection()
def test_selection_state_management()
def test_selection_modification()
```

**Implementation**:
- Rectangular drag selection on canvas
- Selection state management
- Visual feedback for selected wells

**USER TESTING CHECKPOINT**: User must verify complete single-sample workflow works end-to-end.

### Phase 3: Advanced Features
**STOP FOR USER TESTING AFTER THIS PHASE**

#### 3.1 Multi-Sample Workflow
**Context7 Query Required**: Research conditional UI updates and workflow management

**Tests to Write First**:
```python
# test_multi_sample_workflow.py
def test_multi_sample_mode_selection()
def test_manual_plate_name_entry()
def test_per_well_sample_selection()
```

**Implementation**:
- Multi-sample mode selection at startup
- Manual plate name entry for multi-sample mode
- Per-well sample selection in metadata form

#### 3.2 Individual Well Selection
**Context7 Query Required**: Research Canvas item identification and click handling

**Tests to Write First**:
```python
# test_individual_selection.py
def test_individual_well_clicking()
def test_selection_combination_modes()
def test_well_deselection()
```

**Implementation**:
- Individual well clicking functionality
- Combination of drag and click selection
- Well deselection capabilities

#### 3.3 Tri-Color Well Visualization
**Context7 Query Required**: Research Canvas drawing and color management

**Tests to Write First**:
```python
# test_well_visualization.py
def test_tri_color_well_rendering()
def test_group_color_assignment()
def test_visual_state_updates()
```

**Implementation**:
- Tri-color well rendering (1/3 each for group levels)
- Dynamic color assignment for groups
- Real-time visual updates when metadata changes

#### 3.4 Dynamic Legend
**Tests to Write First**:
```python
# test_legend.py
def test_legend_creation()
def test_legend_updates()
def test_color_pattern_mapping()
```

**Implementation**:
- Dynamic legend generation
- Real-time legend updates
- Color and pattern mapping display

**USER TESTING CHECKPOINT**: User must verify multi-sample workflow and advanced visual features work correctly.

### Phase 4: Validation & Polish
**STOP FOR USER TESTING AFTER THIS PHASE**

#### 4.1 Comprehensive Validation
**Context7 Query Required**: Research Python validation patterns and error handling

**Tests to Write First**:
```python
# test_validation.py
def test_group_level_1_exclusivity()
def test_group_level_2_3_inclusivity()
def test_required_field_validation()
def test_data_type_validation()
def test_conflict_resolution()
```

**Implementation**:
- Complete validation rule implementation
- Real-time validation feedback
- Conflict detection and resolution
- Error message system

#### 4.2 Accessibility Features
**Context7 Query Required**: Research accessibility patterns in GUI applications

**Tests to Write First**:
```python
# test_accessibility.py
def test_colorblind_patterns()
def test_high_contrast_mode()
def test_keyboard_navigation()
```

**Implementation**:
- Colorblind support with patterns/shapes
- High contrast mode
- Keyboard navigation support

#### 4.3 Error Handling & Recovery
**Tests to Write First**:
```python
# test_error_handling.py
def test_database_error_recovery()
def test_invalid_selection_handling()
def test_export_error_handling()
```

**Implementation**:
- Comprehensive error handling
- User-friendly error messages
- Recovery mechanisms

**USER TESTING CHECKPOINT**: User must verify all validation, accessibility, and error handling works correctly.

### Phase 5: Export & Distribution
**STOP FOR USER TESTING AFTER THIS PHASE**

#### 5.1 CSV Export System
**Context7 Query Required**: Research CSV writing and file handling in Python

**Tests to Write First**:
```python
# test_export.py
def test_csv_format_matching()
def test_unused_well_handling()
def test_export_validation()
def test_file_writing()
```

**Implementation**:
- CSV export matching exact format of RM5097_layout.csv
- Automatic unused well population
- Export validation
- File writing with error handling

#### 5.2 Conda Package Creation
**Context7 Query Required**: Research Python package distribution with conda

**Implementation**:
- Create environment.yml with exact dependencies
- Package setup and configuration
- Installation testing

**FINAL USER TESTING CHECKPOINT**: Complete end-to-end user acceptance testing.

## Context7 Usage Guidelines

### Required Queries by Topic

#### Tkinter Canvas
- "Tkinter Canvas mouse event handling for drag selection"
- "Canvas item creation and management for grid layouts"
- "Canvas drawing methods for colored shapes and patterns"

#### Tkinter Widgets
- "ttk.Combobox dynamic value updates and event handling"
- "Tkinter form layout and validation patterns"
- "Event binding and callback management in Tkinter"

#### Python Patterns
- "Python SQLite integration best practices"
- "Test-driven development patterns for GUI applications"
- "Error handling and validation in Python applications"

#### Accessibility
- "GUI accessibility patterns for colorblind users"
- "Keyboard navigation implementation in Tkinter"

### Documentation Requirements
- Include Context7 query and response in code comments
- Reference specific Context7 examples in implementation
- Document any deviations from Context7 recommendations

## Testing Requirements

### Unit Test Coverage
- **Minimum 90% code coverage required**
- Every public method must have tests
- Edge cases and error conditions must be tested
- Mock external dependencies (database, file system)

### Test Structure
```python
# Example test structure
class TestPlateCanvas:
    def setup_method(self):
        """Setup for each test method"""
        pass
    
    def test_96_well_grid_creation(self):
        """Test 96-well plate grid creation"""
        # Context7 Reference: [specific query/response]
        pass
    
    def test_well_coordinate_calculation(self):
        """Test well coordinate calculation"""
        pass
```

### Integration Tests
- Test complete workflows end-to-end
- Test database integration scenarios
- Test error recovery paths

## Manual Verification Protocol

### After Each Phase
1. **Demonstrate functionality** to user
2. **Collect feedback** on usability and correctness
3. **Document issues** and required changes
4. **Implement fixes** before proceeding
5. **Re-test** with user if significant changes made

### Verification Criteria
- User can complete intended workflow without assistance
- All visual elements display correctly
- Performance is acceptable
- Error handling works as expected

## Code Quality Standards

### Code Organization
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and returns
- Include comprehensive docstrings
- Organize code into logical modules

### Error Handling
- Use specific exception types
- Provide user-friendly error messages
- Log errors for debugging
- Implement graceful degradation

### Performance
- Optimize Canvas rendering for large plate sizes
- Implement efficient selection algorithms
- Monitor memory usage during testing

## Deliverables Checklist

### Code Deliverables
- [ ] Complete source code with tests
- [ ] Conda environment specification
- [ ] Setup and installation scripts
- [ ] User documentation
- [ ] Developer documentation

### Testing Deliverables
- [ ] Unit test suite with 90%+ coverage
- [ ] Integration test suite
- [ ] Manual testing results
- [ ] Performance benchmarks

### Documentation Deliverables
- [ ] Context7 query log with responses
- [ ] User feedback documentation
- [ ] Known issues and limitations
- [ ] Installation and usage instructions

## Success Criteria

### Functional Success
- All requirements from design specification implemented
- User can complete both single and multi-sample workflows
- CSV export matches required format exactly
- Application runs reliably on target platforms

### Quality Success
- 90%+ test coverage achieved
- All manual verification checkpoints passed
- User provides positive feedback on usability
- Code meets quality standards

### Process Success
- TDD approach followed throughout
- Context7 used for all implementation questions
- Manual verification completed after each phase
- User feedback incorporated into final product

## CRITICAL REMINDERS

1. **DO NOT SKIP USER TESTING** - Stop after each phase for verification
2. **WRITE TESTS FIRST** - No implementation without corresponding tests
3. **USE CONTEXT7** - Query before implementing any Tkinter functionality
4. **DOCUMENT EVERYTHING** - Include Context7 references and user feedback
5. **FOLLOW PHASES** - Do not jump ahead or combine phases

The success of this project depends on strict adherence to these guidelines. Any deviation must be approved by the user before proceeding.