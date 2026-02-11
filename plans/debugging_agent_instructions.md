# Debugging Agent Instructions - Microwell Plate GUI

## CRITICAL REQUIREMENTS

### 1. Context7 Integration - MANDATORY
- **ALWAYS** query Context7 before attempting to debug any issue
- Use Context7 to research error patterns and solutions
- Reference Context7 for debugging best practices
- Document Context7 queries and solutions in bug reports

### 2. Test-First Debugging - MANDATORY
- Write failing tests that reproduce bugs before fixing
- Ensure all existing tests still pass after fixes
- Add regression tests for all resolved issues
- Maintain minimum 90% code coverage

### 3. User Feedback Integration - MANDATORY
- Prioritize issues identified during manual verification
- Test fixes with actual user workflows
- Document user feedback and resolution verification
- Do NOT mark issues as resolved without user confirmation

## Debugging Workflow

### 1. Issue Identification
**Context7 Query Required**: Research similar error patterns and debugging approaches

#### Bug Report Template
```markdown
## Bug Report
- **Issue**: [Brief description]
- **Phase**: [Which implementation phase]
- **Severity**: [Critical/High/Medium/Low]
- **User Impact**: [How this affects user workflow]
- **Reproduction Steps**: [Exact steps to reproduce]
- **Expected Behavior**: [What should happen]
- **Actual Behavior**: [What actually happens]
- **Context7 Research**: [Queries made and responses]
- **Test Case**: [Failing test that reproduces issue]
```

#### Issue Prioritization
1. **Critical**: Application crashes, data loss, cannot complete core workflow
2. **High**: Major functionality broken, poor user experience
3. **Medium**: Minor functionality issues, cosmetic problems
4. **Low**: Enhancement requests, nice-to-have features

### 2. Root Cause Analysis
**Context7 Query Required**: Research debugging techniques for identified issue type

#### Analysis Steps
1. **Reproduce Issue**: Create minimal test case that reproduces the bug
2. **Context7 Research**: Query for similar issues and solutions
3. **Code Review**: Examine relevant code sections
4. **Dependency Check**: Verify all dependencies and versions
5. **Environment Validation**: Test in clean conda environment

#### Common Issue Categories

##### Tkinter Canvas Issues
**Context7 Queries**:
- "Tkinter Canvas performance optimization for large grids"
- "Canvas mouse event handling debugging techniques"
- "Canvas item selection and highlighting issues"

**Common Problems**:
- Slow rendering with 384-well plates
- Mouse event conflicts
- Selection state inconsistencies
- Visual rendering artifacts

##### Database Integration Issues
**Context7 Queries**:
- "SQLite connection and error handling in Python"
- "Database file access and permission issues"
- "SQL query optimization and debugging"

**Common Problems**:
- Database file not found
- Permission errors
- Corrupted database files
- Query performance issues

##### Widget and Layout Issues
**Context7 Queries**:
- "Tkinter widget layout and geometry management debugging"
- "ttk.Combobox event handling and value updates"
- "Form validation and error display patterns"

**Common Problems**:
- Layout not responsive
- Dropdown values not updating
- Form validation errors
- Widget state synchronization

##### Data Validation Issues
**Context7 Queries**:
- "Python data validation debugging techniques"
- "Error handling and user feedback patterns"
- "State management debugging in GUI applications"

**Common Problems**:
- Validation rules not enforced
- Inconsistent data states
- Error messages not displayed
- Conflict resolution failures

### 3. Solution Development
**Context7 Query Required**: Research best practices for implementing fixes

#### Fix Development Process
1. **Write Failing Test**: Create test that reproduces the bug
2. **Research Solution**: Use Context7 to find best practices
3. **Implement Fix**: Make minimal changes to resolve issue
4. **Verify Fix**: Ensure test passes and no regressions
5. **User Validation**: Test fix with actual user workflow

#### Testing Requirements
- All existing tests must continue to pass
- New regression test must be added
- Manual testing with user must be performed
- Performance impact must be assessed

### 4. Performance Debugging
**Context7 Query Required**: Research performance optimization techniques

#### Performance Issues
- **Canvas Rendering**: Optimize well grid drawing for large plates
- **Database Queries**: Optimize sample data loading
- **Memory Usage**: Monitor memory consumption during operation
- **Response Time**: Ensure UI remains responsive

#### Profiling Tools
```python
# Example profiling setup
import cProfile
import pstats

def profile_function(func):
    """Profile a specific function"""
    profiler = cProfile.Profile()
    profiler.enable()
    result = func()
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats()
    return result
```

### 5. Cross-Platform Debugging
**Context7 Query Required**: Research platform-specific issues and solutions

#### Platform-Specific Issues
- **macOS**: Retina display scaling, file path handling
- **Windows**: Font rendering, file permissions
- **Linux**: Package dependencies, display managers

#### Testing Matrix
- Test on multiple Python versions (3.9, 3.10, 3.11)
- Test on different operating systems
- Test with different screen resolutions
- Test with different conda environments

## Specific Debugging Scenarios

### Canvas Performance Issues
**Context7 Research Required**:
- "Tkinter Canvas optimization for large numbers of items"
- "Canvas redraw optimization techniques"
- "Memory management for Canvas widgets"

**Debugging Steps**:
1. Profile canvas rendering performance
2. Identify bottlenecks in well drawing
3. Implement incremental rendering
4. Optimize color and pattern application
5. Test with both 96 and 384-well plates

### Database Connection Issues
**Context7 Research Required**:
- "SQLite file access debugging in Python"
- "Database connection error handling patterns"
- "File permission debugging techniques"

**Debugging Steps**:
1. Verify database file exists and is readable
2. Check file permissions and ownership
3. Test database integrity
4. Implement graceful fallback handling
5. Add comprehensive error logging

### Selection Logic Issues
**Context7 Research Required**:
- "Mouse event handling debugging in Tkinter"
- "Canvas item selection algorithms"
- "State management debugging techniques"

**Debugging Steps**:
1. Log all mouse events and coordinates
2. Verify well coordinate calculations
3. Test selection state management
4. Debug visual feedback updates
5. Test edge cases and boundary conditions

### Validation Logic Issues
**Context7 Research Required**:
- "Python validation framework debugging"
- "Error message display and handling"
- "Data consistency debugging techniques"

**Debugging Steps**:
1. Test all validation rules individually
2. Verify error message display
3. Test conflict resolution logic
4. Debug state synchronization
5. Test with invalid data inputs

## Testing and Verification

### Automated Testing
- Run full test suite after every fix
- Verify no regressions introduced
- Check code coverage remains above 90%
- Performance benchmarks must not degrade

### Manual Testing Protocol
1. **Reproduce Original Issue**: Verify fix resolves the problem
2. **Test Related Functionality**: Ensure no side effects
3. **User Workflow Testing**: Complete end-to-end workflows
4. **Edge Case Testing**: Test boundary conditions
5. **User Acceptance**: Get user confirmation of fix

### Regression Testing
- Maintain comprehensive regression test suite
- Add test for every resolved bug
- Run regression tests before each release
- Document test coverage for each component

## Documentation Requirements

### Bug Resolution Documentation
```markdown
## Bug Resolution Report
- **Issue ID**: [Unique identifier]
- **Original Problem**: [Description of bug]
- **Root Cause**: [What caused the issue]
- **Context7 Research**: [Queries and responses used]
- **Solution**: [How the issue was resolved]
- **Tests Added**: [New tests to prevent regression]
- **User Verification**: [User confirmation of fix]
- **Performance Impact**: [Any performance changes]
```

### Code Comments
- Document complex debugging solutions
- Reference Context7 queries and responses
- Explain non-obvious fixes
- Include performance considerations

## Quality Assurance

### Code Review Checklist
- [ ] Fix addresses root cause, not just symptoms
- [ ] Solution follows Context7 best practices
- [ ] All tests pass including new regression tests
- [ ] Code coverage maintained above 90%
- [ ] Performance impact assessed and acceptable
- [ ] User has verified fix resolves issue
- [ ] Documentation updated appropriately

### Release Criteria
- All critical and high priority bugs resolved
- User acceptance testing completed successfully
- Performance benchmarks meet requirements
- Cross-platform testing completed
- Documentation updated and accurate

## Common Debugging Tools

### Python Debugging
```python
import pdb
import logging
import traceback

# Set up comprehensive logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

# Use pdb for interactive debugging
pdb.set_trace()

# Comprehensive exception handling
try:
    # Code that might fail
    pass
except Exception as e:
    logging.error(f"Error: {e}")
    logging.error(traceback.format_exc())
    raise
```

### Tkinter Debugging
```python
# Debug widget states
def debug_widget_state(widget):
    """Print comprehensive widget state information"""
    print(f"Widget: {widget}")
    print(f"State: {widget.cget('state')}")
    print(f"Value: {widget.get() if hasattr(widget, 'get') else 'N/A'}")
    print(f"Focus: {widget.focus_get()}")

# Debug Canvas items
def debug_canvas_items(canvas):
    """Print information about all canvas items"""
    for item in canvas.find_all():
        print(f"Item {item}: {canvas.type(item)}")
        print(f"  Coords: {canvas.coords(item)}")
        print(f"  Tags: {canvas.gettags(item)}")
```

## Success Criteria

### Bug Resolution Success
- All reported issues resolved to user satisfaction
- No regressions introduced during debugging
- Application stability improved
- User workflows function reliably

### Process Success
- Context7 used for all debugging research
- Comprehensive testing performed for all fixes
- User feedback incorporated into solutions
- Documentation maintained throughout process

### Quality Success
- Code coverage maintained above 90%
- Performance meets or exceeds requirements
- Cross-platform compatibility verified
- User acceptance criteria met

## CRITICAL REMINDERS

1. **CONTEXT7 FIRST** - Always research issues using Context7 before attempting fixes
2. **TEST EVERYTHING** - Write tests that reproduce bugs before fixing
3. **USER VALIDATION** - Get user confirmation that fixes work correctly
4. **NO REGRESSIONS** - Ensure existing functionality continues to work
5. **DOCUMENT SOLUTIONS** - Maintain comprehensive debugging documentation

The debugging process is critical to delivering a reliable, high-quality application that meets user needs and expectations.