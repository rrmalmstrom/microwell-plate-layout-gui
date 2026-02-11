# Agent Handoff Instructions - Microwell Plate GUI Project

## Project Overview

This document provides complete handoff instructions for coding and debugging agents to implement a Python-based GUI tool for microwell plate layout design. The project uses Test-Driven Development (TDD), Context7 integration, and requires manual user verification at each phase.

## Document Structure and Dependencies

### Core Documents (READ FIRST)
1. **[microwell_plate_gui_design_specification.md](microwell_plate_gui_design_specification.md)** - Complete project requirements and architecture
2. **[coding_agent_instructions.md](coding_agent_instructions.md)** - Detailed implementation guidelines for coding agent
3. **[debugging_agent_instructions.md](debugging_agent_instructions.md)** - Comprehensive debugging protocols and procedures
4. **[conda_distribution_setup.md](conda_distribution_setup.md)** - Environment management and distribution strategy
5. **[workflow_diagrams.md](workflow_diagrams.md)** - Visual workflows and technical requirements

### Reference Files
- **[RM5097_layout.csv](../RM5097_layout.csv)** - Target CSV format for export functionality
- **[example_database.csv](../example_database.csv)** - Sample database structure
- **[example_database.db](../example_database.db)** - SQLite database for testing

## Critical Success Factors

### 1. MANDATORY Context7 Integration
- **Every implementation decision** must be researched using Context7
- Document Context7 queries and responses in code comments
- Reference specific Context7 examples in implementation
- Use Context7 for debugging and problem resolution

### 2. MANDATORY Test-Driven Development
- Write tests FIRST, then implement functionality
- Achieve minimum 90% code coverage
- Run tests after every change
- Add regression tests for all bug fixes

### 3. MANDATORY User Verification Checkpoints
- **STOP after each phase** for user testing
- Do NOT proceed without user approval
- Implement user feedback before continuing
- Document all user interactions and resolutions

### 4. MANDATORY Environment Management
- Use pinned conda environment with exact versions
- Update environment.yml throughout development
- Test environment reproducibility regularly
- Maintain deterministic builds

## Implementation Sequence (STRICT ORDER)

### Phase 0: Foundation Setup
**Duration**: 1-2 days
**Deliverables**: Working development environment, Git repository, baseline tests

**Critical Steps**:
1. Create and test conda environment on user's development machine
2. Set up Git repository with GitHub integration
3. Establish project structure and initial tests
4. Verify all tools and dependencies work correctly

**User Verification Required**: Environment setup and basic project structure

### Phase 1: Core Infrastructure
**Duration**: 3-5 days
**Deliverables**: Basic GUI with plate display, database integration, well selection

**Critical Steps**:
1. Implement main application window with split layout
2. Create plate canvas with well grid rendering
3. Integrate SQLite database for sample data
4. Implement basic rectangular well selection

**User Verification Required**: Application launches, displays correct plate, loads database

### Phase 2: Metadata System
**Duration**: 3-5 days
**Deliverables**: Complete single-sample workflow, metadata forms, validation

**Critical Steps**:
1. Create metadata entry forms with dropdowns
2. Implement dynamic plate name generation
3. Complete single-sample workflow
4. Add basic validation and error handling

**User Verification Required**: Complete single-sample workflow works end-to-end

### Phase 3: Advanced Features
**Duration**: 5-7 days
**Deliverables**: Multi-sample workflow, tri-color visualization, individual selection

**Critical Steps**:
1. Implement multi-sample workflow
2. Add individual well selection capability
3. Create tri-color well visualization system
4. Implement dynamic legend generation

**User Verification Required**: Multi-sample workflow and visual features work correctly

### Phase 4: Validation & Polish
**Duration**: 3-5 days
**Deliverables**: Comprehensive validation, accessibility features, error handling

**Critical Steps**:
1. Implement complete validation rules
2. Add accessibility features (colorblind support)
3. Comprehensive error handling and recovery
4. Performance optimization

**User Verification Required**: All validation, accessibility, and error handling works

### Phase 5: Export & Distribution
**Duration**: 2-3 days
**Deliverables**: CSV export, conda package, installation system

**Critical Steps**:
1. Implement CSV export matching exact format
2. Create conda package with launcher scripts
3. Test installation and distribution system
4. Final user acceptance testing

**User Verification Required**: Complete end-to-end user acceptance testing

## Context7 Integration Protocol

### Required Queries by Phase

#### Phase 0 Queries
```
"Python conda environment best practices and dependency management"
"Git repository setup and GitHub integration workflows"
"Python project structure and packaging standards"
```

#### Phase 1 Queries
```
"Tkinter application architecture patterns and main window setup"
"Tkinter Canvas widget for interactive grid layouts and mouse events"
"SQLite database integration patterns in Python applications"
```

#### Phase 2 Queries
```
"Tkinter form widgets and layout management best practices"
"ttk.Combobox dynamic value updates and event handling"
"Python data validation patterns and error handling"
```

#### Phase 3 Queries
```
"Tkinter Canvas drawing methods for colored shapes and patterns"
"Mouse event handling and selection algorithms in Tkinter"
"GUI state management and component synchronization"
```

#### Phase 4 Queries
```
"Python validation frameworks and comprehensive error handling"
"GUI accessibility patterns for colorblind and keyboard users"
"Performance optimization techniques for Tkinter applications"
```

#### Phase 5 Queries
```
"Python CSV writing and file handling best practices"
"Conda package creation and distribution workflows"
"Cross-platform Python application deployment"
```

### Documentation Requirements
- Include Context7 query in code comments before implementation
- Reference specific Context7 examples used
- Document any deviations from Context7 recommendations
- Maintain query log for debugging reference

## Testing Requirements

### Unit Testing Standards
- **Coverage**: Minimum 90% code coverage required
- **Framework**: Use pytest for all testing
- **Structure**: Separate test files for each module
- **Mocking**: Mock external dependencies (database, file system)

### Test Categories Required
1. **GUI Component Tests**: Widget creation, layout, event handling
2. **Business Logic Tests**: Validation, state management, data processing
3. **Database Tests**: Connection, queries, error handling
4. **Integration Tests**: End-to-end workflows, component interaction
5. **Performance Tests**: Rendering speed, memory usage, responsiveness

### Test Execution Protocol
- Run tests after every code change
- Run full test suite before each phase completion
- Add regression tests for every bug fix
- Test in clean conda environment regularly

## User Verification Protocol

### Verification Process
1. **Demonstrate Functionality**: Show working features to user
2. **Collect Feedback**: Document user comments and issues
3. **Prioritize Issues**: Critical, High, Medium, Low severity
4. **Implement Fixes**: Address issues before proceeding
5. **Re-verify**: Test fixes with user if significant changes made

### Verification Criteria
- User can complete intended workflow without assistance
- All visual elements display correctly and intuitively
- Performance meets user expectations
- Error handling provides clear guidance
- Application behaves predictably and reliably

### Documentation Requirements
- Record all user feedback verbatim
- Document resolution for each issue raised
- Track user satisfaction scores for each phase
- Maintain change log of user-requested modifications

## Quality Assurance Standards

### Code Quality Requirements
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and returns
- Include comprehensive docstrings
- Organize code into logical modules
- Maintain consistent naming conventions

### Performance Standards
- Canvas rendering: < 500ms for 384-well plate
- Database loading: < 200ms for sample data
- Well selection response: < 100ms
- CSV export: < 1 second
- Memory usage: < 100MB during operation

### Error Handling Standards
- Use specific exception types
- Provide user-friendly error messages
- Log errors for debugging purposes
- Implement graceful degradation
- Offer recovery mechanisms where possible

## Git Workflow Requirements

### Repository Management
- Commit after each significant change
- Use descriptive commit messages
- Push to GitHub after each phase completion
- Tag releases for each phase
- Maintain clean commit history

### Branch Strategy
- Use main branch for stable releases
- Create feature branches for major changes
- Merge only after testing and user verification
- Maintain environment.yml in version control

### Documentation in Git
- Update README.md throughout development
- Maintain CHANGELOG.md with user-visible changes
- Include installation and usage instructions
- Document known issues and limitations

## Environment Management Protocol

### Development Environment
- Use exact pinned versions in environment.yml
- Test environment recreation regularly
- Update environment file when adding dependencies
- Verify cross-platform compatibility

### Distribution Environment
- Create locked environment file for distribution
- Test installation on clean systems
- Provide automated installation scripts
- Include environment verification tools

### Continuous Integration
- Test in multiple Python versions (3.9, 3.10, 3.11)
- Test on multiple platforms (macOS, Windows, Linux)
- Verify environment reproducibility
- Monitor performance benchmarks

## Risk Management

### Technical Risks
- **Canvas Performance**: Monitor rendering speed with large plates
- **Database Issues**: Test with various database states
- **Cross-Platform**: Verify functionality on all target platforms
- **Memory Usage**: Monitor for memory leaks during long sessions

### Process Risks
- **User Availability**: Schedule verification sessions in advance
- **Scope Creep**: Document and approve all requirement changes
- **Technical Debt**: Refactor code regularly to maintain quality
- **Integration Issues**: Test component interactions thoroughly

### Mitigation Strategies
- Regular performance testing and optimization
- Comprehensive error handling and logging
- Frequent user communication and feedback
- Continuous integration and testing

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
- Code meets all quality standards

### Process Success
- TDD approach followed throughout development
- Context7 used for all implementation questions
- Manual verification completed after each phase
- User feedback incorporated into final product

### Delivery Success
- Conda package installs and runs correctly
- Documentation is complete and accurate
- User can operate application independently
- Application meets performance requirements

## Final Deliverables Checklist

### Code Deliverables
- [ ] Complete source code with comprehensive tests
- [ ] Conda environment specification (pinned versions)
- [ ] Installation and launcher scripts
- [ ] Cross-platform compatibility verified

### Documentation Deliverables
- [ ] User manual and installation guide
- [ ] Developer documentation and API reference
- [ ] Context7 query log with responses
- [ ] User feedback documentation and resolutions

### Testing Deliverables
- [ ] Unit test suite with 90%+ coverage
- [ ] Integration test suite
- [ ] Manual testing results and user verification
- [ ] Performance benchmarks and optimization notes

### Distribution Deliverables
- [ ] Conda package ready for distribution
- [ ] Automated installation system
- [ ] User verification of installation process
- [ ] Support documentation and troubleshooting guide

## Emergency Procedures

### If User Testing Fails
1. Stop all development immediately
2. Document all issues identified by user
3. Prioritize issues by severity and user impact
4. Create focused plan to address critical issues
5. Re-test with user before proceeding

### If Context7 is Unavailable
1. Document the specific issue or question
2. Research using alternative documentation sources
3. Implement conservative, well-tested solution
4. Mark for Context7 verification when available
5. Update implementation based on Context7 guidance

### If Environment Issues Occur
1. Document exact error conditions and environment state
2. Test with clean environment recreation
3. Identify and pin problematic dependencies
4. Update environment.yml with fixes
5. Verify fix works on user's development machine

### If Performance Issues Arise
1. Profile application to identify bottlenecks
2. Research optimization techniques using Context7
3. Implement targeted performance improvements
4. Verify improvements meet performance requirements
5. Update performance benchmarks

## Contact and Escalation

### User Communication
- Schedule regular check-ins during development
- Provide progress updates after each phase
- Request immediate feedback on critical issues
- Document all communication and decisions

### Technical Escalation
- Use Context7 for all technical questions first
- Escalate to user for requirement clarifications
- Document all technical decisions and rationale
- Maintain decision log for future reference

This comprehensive handoff ensures that coding and debugging agents have all necessary information, protocols, and standards to successfully deliver a high-quality microwell plate GUI application that meets user needs and technical requirements.