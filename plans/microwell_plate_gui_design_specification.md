# Microwell Plate Selection GUI Tool - Design Specification

## Project Overview

This document provides comprehensive design specifications for a Python-based GUI tool that allows molecular biology researchers to design microwell plate layouts and generate standardized CSV files for downstream processing.

### Core Purpose
- Enable researchers to visually select wells on 96-well or 384-well plates
- Assign metadata to well groups (sample types, cell counts, grouping levels)
- Generate CSV files matching the exact format required by downstream Python scripts
- Support both single-sample and multi-sample plate configurations

## Requirements Summary

### Functional Requirements
1. **Plate Support**: 96-well (A-H, 1-12) and 384-well (A-P, 1-24) plates
2. **Well Selection**: Rectangular drag selection + individual well clicking
3. **Metadata Management**: Sample types, cell counts, hierarchical grouping (3 levels)
4. **Database Integration**: SQLite database for sample/plate name dropdowns
5. **Visual Feedback**: Tri-color well coding with dynamic legend
6. **Export**: Fixed CSV format matching [`RM5097_layout.csv`](../RM5097_layout.csv)

### Technical Requirements
- **Platform**: Python with Tkinter GUI framework
- **Distribution**: Conda package with deterministic build
- **Database**: SQLite integration for metadata dropdowns
- **Accessibility**: Colorblind support with patterns/shapes
- **Validation**: Comprehensive data validation and error checking

## User Workflow Analysis

### Primary Workflow: Single Sample Mode (Typical)
1. **Startup**: User selects plate type (96 or 384 wells)
2. **Sample Selection**: Choose sample from database dropdown
3. **Plate Name Selection**: Choose from dynamically populated plate names
4. **Well Selection**: Use drag/click to select well groups
5. **Metadata Entry**: Assign sample type, cell count, grouping levels
6. **Iteration**: Repeat selection/assignment for different well groups
7. **Export**: Generate CSV file

### Alternative Workflow: Multi-Sample Mode
1. **Startup**: User selects plate type and indicates multi-sample
2. **Plate Naming**: Manually enter custom plate name
3. **Well Selection**: Use drag/click to select well groups
4. **Metadata Entry**: Choose sample, sample type, cell count, grouping levels
5. **Iteration**: Repeat for different samples/well groups
6. **Export**: Generate CSV file

## Technical Architecture

### Core Components

#### 1. Main Application Window
- **Framework**: Tkinter with split layout design
- **Layout**: Equal space for plate visualization and metadata panels
- **Startup Dialog**: Plate type selection (96/384) and single/multi-sample mode

#### 2. Plate Visualization Component
- **Implementation**: Tkinter Canvas widget
- **Grid Layout**: Dynamic well grid based on plate type
- **Visual Feedback**: Tri-color well representation
  - 1/3 of well colored by Group Level 1
  - 1/3 of well colored by Group Level 2  
  - 1/3 of well colored by Group Level 3
- **Accessibility**: Patterns/shapes for colorblind support
- **Selection States**: 
  - Gray: Unused wells
  - Colored: Wells with assigned metadata
  - Highlighted: Currently selected wells

#### 3. Well Selection System
- **Rectangular Selection**: Mouse drag to select well blocks
- **Individual Selection**: Click individual wells
- **Modification**: Add/remove wells from current selection before metadata assignment
- **Validation**: Prevent conflicts with existing assignments

#### 4. Metadata Management System
- **Database Integration**: SQLite database reader for sample/plate data
- **Dynamic Dropdowns**: 
  - Sample dropdown pre-populated from database
  - Plate name dropdown populated based on sample selection
  - Sample type dropdown with 4 categories + "Other" option
- **Metadata Fields**:
  - Plate Name (auto-generated or manual)
  - Sample Name (from database or manual)
  - Sample Type (sample, neg_cntrl, pos_cntrl, unused, other)
  - Cell Count (integer)
  - Group Level 1 (exclusive per well)
  - Group Level 2 (can span Group 1 boundaries)
  - Group Level 3 (can span Group 1 boundaries)

#### 5. Data Validation Engine
- **Real-time Validation**: Check constraints as user enters data
- **Conflict Detection**: Ensure wells don't belong to multiple Group 1 values
- **Required Fields**: Validate all necessary fields before export
- **Data Consistency**: Cross-check grouping relationships

#### 6. Export System
- **Fixed Format**: Exact match to [`RM5097_layout.csv`](../RM5097_layout.csv) structure
- **Automatic Population**: Unused wells marked as "unused" with empty metadata
- **File Generation**: CSV export with proper formatting

### Database Schema

Based on [`example_database.csv`](../example_database.csv):
```sql
CREATE TABLE samples (
    Proposal TEXT,
    Project TEXT,
    Sample TEXT,
    Number_of_sorted_plates INTEGER
);
```

**Plate Name Generation Logic**:
- Format: `{Project}.{Sample}.{plate_number}`
- Example: `BP9735.SitukAM.1`, `BP9735.SitukAM.2`, `BP9735.SitukAM.3`

## User Interface Design

### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│ Menu Bar: File | Edit | View | Help                        │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────┐ ┌─────────────────────────────────┐ │
│ │                     │ │ Metadata Panel                  │ │
│ │   Plate Canvas      │ │ ┌─────────────────────────────┐ │ │
│ │   (Well Grid)       │ │ │ Sample: [Dropdown ▼]       │ │ │
│ │                     │ │ │ Plate:  [Dropdown ▼]       │ │ │
│ │                     │ │ │ Type:   [Dropdown ▼]       │ │ │
│ │                     │ │ │ Cells:  [Entry Field]      │ │ │
│ │                     │ │ │ Group1: [Entry Field]      │ │ │
│ │                     │ │ │ Group2: [Entry Field]      │ │ │
│ │                     │ │ │ Group3: [Entry Field]      │ │ │
│ │                     │ │ │ [Apply] [Clear Selection]  │ │ │
│ │                     │ │ └─────────────────────────────┘ │ │
│ │                     │ │                                 │ │
│ │                     │ │ Legend Panel                    │ │
│ │                     │ │ ┌─────────────────────────────┐ │ │
│ │                     │ │ │ Color/Pattern Legend        │ │ │
│ │                     │ │ │ (Dynamic based on groups)   │ │ │
│ │                     │ │ └─────────────────────────────┘ │ │
│ └─────────────────────┘ └─────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Status Bar: Selection info | Validation messages           │
├─────────────────────────────────────────────────────────────┤
│ [Reset All] [Export CSV] [Exit]                            │
└─────────────────────────────────────────────────────────────┘
```

### Visual Design Elements

#### Well Representation
- **Shape**: Circular wells in grid layout
- **Size**: Proportional to plate type (smaller for 384-well)
- **Colors**: Distinct colors for each group level
- **Patterns**: Stripes, dots, hatching for colorblind accessibility
- **Labels**: Well coordinates (A1, B2, etc.) visible on hover

#### Dynamic Legend
- **Auto-generation**: Appears when first metadata is assigned
- **Group Colors**: Shows color/pattern mapping for each group level
- **Sample Types**: Visual indicators for different sample types
- **Update**: Real-time updates as new groups are created

## Error Handling & Validation

### Validation Rules
1. **Group Level 1**: Wells cannot belong to multiple Group 1 values (exclusive)
2. **Group Levels 2-3**: Can span across Group 1 boundaries (inclusive)
3. **Required Fields**: Sample type and plate name must be specified
4. **Data Types**: Cell count must be integer, grouping values must be strings
5. **Database Integrity**: Sample names must exist in database (unless "Other" selected)

### Error Messages
- **Real-time Feedback**: Immediate validation messages in status bar
- **Conflict Resolution**: Clear instructions for resolving Group 1 conflicts
- **Missing Data**: Highlight incomplete metadata before export
- **Database Errors**: Graceful handling of missing/corrupted database files

### Fallback Behaviors
- **Missing Database**: Prompt user, continue with manual entry only
- **Invalid Selections**: Auto-deselect conflicting wells
- **Export Errors**: Validate all data before allowing export

## Accessibility Features

### Colorblind Support
- **Pattern Overlay**: Stripes, dots, hatching in addition to colors
- **High Contrast**: Alternative color schemes
- **Shape Coding**: Different well border styles for group levels

### Usability Features
- **Tooltips**: Hover information for all interface elements
- **Keyboard Navigation**: Tab order and keyboard shortcuts
- **Undo/Redo**: Step back through selection changes
- **Bulk Operations**: Clear all, reset plate, copy metadata

## Testing Strategy

### Unit Testing Requirements
- **Well Selection Logic**: Test rectangular and individual selection
- **Metadata Validation**: Test all validation rules and edge cases
- **Database Integration**: Test with various database states
- **Export Functionality**: Verify CSV format matches exactly
- **Visual Rendering**: Test plate layouts and color coding

### Integration Testing
- **End-to-End Workflows**: Complete single and multi-sample workflows
- **Database Scenarios**: Test with missing, corrupted, and valid databases
- **Error Recovery**: Test error handling and user recovery paths
- **Cross-Platform**: Test on different operating systems

### Manual Testing Checkpoints
1. **Startup Configuration**: Verify plate type selection works correctly
2. **Database Loading**: Confirm sample dropdowns populate correctly
3. **Well Selection**: Test drag selection and individual clicking
4. **Metadata Entry**: Verify all form fields work as expected
5. **Visual Feedback**: Confirm tri-color wells and legend display correctly
6. **Validation**: Test error messages and conflict resolution
7. **Export**: Verify CSV output matches expected format exactly
8. **Edge Cases**: Test with empty selections, invalid data, etc.

## Implementation Phases

### Phase 1: Core Infrastructure
- Basic Tkinter application structure
- Plate canvas with well grid rendering
- Database connection and sample loading
- Basic well selection (rectangular drag)

### Phase 2: Metadata System
- Metadata entry forms with dropdowns
- Dynamic plate name generation
- Basic validation and error handling
- Single-sample workflow implementation

### Phase 3: Advanced Features
- Multi-sample workflow support
- Tri-color well visualization
- Dynamic legend generation
- Individual well selection

### Phase 4: Polish & Testing
- Accessibility features (patterns, high contrast)
- Comprehensive validation
- Error handling and recovery
- Manual testing and refinement

### Phase 5: Distribution
- Conda package creation
- Documentation and user guides
- Installation testing
- Final validation

## Context7 Integration Requirements

### For Design Phase (Current)
- Reference Tkinter Canvas documentation for well grid implementation
- Verify Combobox capabilities for dropdown menus
- Research SQLite integration patterns
- Validate accessibility best practices

### For Coding Agent
- **Mandatory**: Use Context7 for all Tkinter implementation questions
- **TDD Approach**: Write tests first, then implement features
- **Documentation**: Reference Context7 for proper widget usage
- **Best Practices**: Query Context7 for Python GUI design patterns

### For Debugging Agent
- **Error Resolution**: Use Context7 to research error solutions
- **Performance**: Query optimization techniques for Tkinter Canvas
- **Cross-Platform**: Research platform-specific issues and solutions
- **Testing**: Reference testing frameworks and methodologies

## Manual Verification Protocol

### Required User Testing Points
1. **After Phase 1**: User tests basic plate display and well selection
2. **After Phase 2**: User tests complete single-sample workflow
3. **After Phase 3**: User tests multi-sample workflow and visual feedback
4. **After Phase 4**: User tests accessibility features and error handling
5. **Before Release**: Complete end-to-end user acceptance testing

### Verification Criteria
- User can complete typical workflow without assistance
- All visual elements display correctly and are intuitive
- Error messages are clear and actionable
- Export CSV matches expected format exactly
- Performance is acceptable for typical use cases

## Handoff Instructions

### For Coding Agent
1. **Start with TDD**: Write comprehensive tests before implementation
2. **Use Context7**: Reference for all Tkinter and Python questions
3. **Follow Phases**: Implement in specified order with user testing checkpoints
4. **Manual Verification**: Stop after each phase for user validation
5. **Documentation**: Comment code thoroughly and maintain design alignment

### For Debugging Agent
1. **Context7 First**: Always research issues using Context7 before other approaches
2. **Test Coverage**: Ensure all functionality has corresponding tests
3. **User Feedback**: Incorporate manual testing feedback into bug fixes
4. **Performance**: Monitor and optimize Canvas rendering performance
5. **Cross-Platform**: Test on multiple operating systems

### Success Criteria
- All functional requirements implemented and tested
- User can successfully complete both single and multi-sample workflows
- CSV export matches [`RM5097_layout.csv`](../RM5097_layout.csv) format exactly
- Application runs reliably on target platforms
- User provides positive feedback on usability and functionality

## File Structure

```
microwell_plate_gui/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py      # Main application window
│   │   ├── plate_canvas.py     # Plate visualization component
│   │   ├── metadata_panel.py   # Metadata entry forms
│   │   └── dialogs.py          # Startup and confirmation dialogs
│   ├── data/
│   │   ├── __init__.py
│   │   ├── database.py         # SQLite database interface
│   │   ├── validation.py       # Data validation logic
│   │   └── export.py           # CSV export functionality
│   └── utils/
│       ├── __init__.py
│       ├── colors.py           # Color and pattern management
│       └── constants.py        # Application constants
├── tests/
│   ├── __init__.py
│   ├── test_gui/
│   ├── test_data/
│   └── test_utils/
├── docs/
│   ├── user_guide.md
│   └── developer_guide.md
├── environment.yml             # Conda environment specification
├── setup.py                    # Package setup
└── README.md                   # Project overview
```

This design specification provides the comprehensive foundation needed for coding and debugging agents to build a robust, user-friendly microwell plate selection GUI tool that meets all specified requirements.