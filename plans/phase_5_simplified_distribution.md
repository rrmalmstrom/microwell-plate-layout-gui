# Phase 5: Simplified Distribution Strategy

## Environment Analysis

**Current Development Environment:** `microwell-gui-dev`
- Location: `/Users/RRMalmstrom/anaconda3/envs/microwell-gui-dev`
- Python: 3.11.14 (pinned)
- Key dependencies already pinned with exact versions
- Working application with comprehensive test suite

## Distribution Requirements

**Target Users:** Lab colleagues on macOS
**Goal:** Simple conda environment setup + easy executable launcher
**Constraint:** Deterministic environment (pinned versions) to match development

## Simplified Phase 5 Strategy

### 1. Production Environment File
Create `environment.yml` (production) from `environment-dev.yml`:
- Remove development-only dependencies (pytest, etc.)
- Keep core runtime dependencies with exact pinned versions
- Rename environment to `microwell-plate-gui`

### 2. Simple Launcher Script
Create `launch_microwell_gui.sh`:
- Activates conda environment
- Runs application via `python run_app.py`
- Handles basic error cases
- macOS-focused (no cross-platform complexity)

### 3. Minimal Distribution Package
```
microwell-plate-gui/
├── README.md                    # Simple installation instructions
├── environment.yml              # Production conda environment
├── launch_microwell_gui.sh      # Simple launcher script
├── run_app.py                   # Application entry point
├── src/                         # Source code
├── example_database.db          # Sample data
└── example_database.csv         # Sample data
```

### 4. Installation Process
1. User downloads/clones package
2. Creates conda environment: `conda env create -f environment.yml`
3. Makes launcher executable: `chmod +x launch_microwell_gui.sh`
4. Runs application: `./launch_microwell_gui.sh`

## Key Simplifications vs. Current Plan

**Removed Complexity:**
- ❌ Cross-platform installers (Windows batch files, Linux desktop entries)
- ❌ Automated installation scripts with desktop shortcuts
- ❌ Complex package structure with multiple environment files
- ❌ Verification scripts and elaborate error handling
- ❌ Application bundle creation for macOS

**Focused Approach:**
- ✅ Single production environment file with pinned versions
- ✅ Simple shell script launcher for macOS
- ✅ Minimal package structure
- ✅ Clear, concise installation instructions
- ✅ Deterministic builds matching development environment

## Implementation Steps

1. **Create Production Environment**
   - Strip testing dependencies from `environment-dev.yml`
   - Rename environment to `microwell-plate-gui`
   - Verify all runtime dependencies are pinned

2. **Create Simple Launcher**
   - Shell script that activates environment and runs app
   - Basic error handling for missing environment
   - macOS-specific (no Windows/Linux complexity)

3. **Package Structure**
   - Copy source code and essential files
   - Include sample database files
   - Add simple README with installation steps

4. **Test Distribution**
   - Test on clean macOS system
   - Verify environment creation works
   - Confirm application launches correctly

This approach provides exactly what you need: a simple way for lab colleagues to set up the deterministic conda environment and launch the application, without the over-engineering of the current plan.