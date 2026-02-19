# Microwell Plate GUI

A graphical user interface tool for designing microwell plate layouts with automated CSV and PDF export capabilities.

## 🚀 Quick Start

### For End Users
1. **Install**: Run `./setup_microwell_gui.sh` (one-time setup)
2. **Launch**: Double-click `🧬 Start Microwell GUI.command`
3. **Use**: Design your plate layout and export to CSV/PDF

### For Developers
1. **Clone**: `git clone <repository-url>`
2. **Setup**: `conda env create -f environment.yml`
3. **Test**: `python tests/test_environment.py`
4. **Run**: `python run_app.py`

## 📁 Project Structure

```
microwell-plate-gui/
├── 🧬 Start Microwell GUI.command    # Double-click launcher for end users
├── setup_microwell_gui.sh            # One-time installation script
├── run_app.py                        # Direct Python launcher
├── environment.yml                   # Minimal conda environment (3 packages)
├── environment_conservative.yml      # Backup environment with extra packages
├── _internal_launcher.sh             # Internal launcher script
├── README.md                         # This file
├── .gitignore                        # Git ignore rules
│
├── src/microwell_plate_gui/          # Main application source code
│   ├── main.py                       # Application entry point
│   ├── gui/                          # GUI components
│   │   ├── main_window.py           # Main application window
│   │   ├── plate_canvas.py          # Plate visualization
│   │   ├── metadata_panel.py        # Metadata input form
│   │   └── legend_panel.py          # Color legend
│   ├── data/                         # Data management
│   │   └── database.py              # SQLite database operations
│   └── utils/                        # Utility functions
│       ├── csv_export.py            # CSV export functionality
│       └── image_export.py          # PDF export functionality
│
├── docs/                             # Documentation
│   ├── INSTALLATION.md              # Detailed installation guide
│   ├── README_DISTRIBUTION.md       # Distribution package guide
│   └── VALIDATION_REPORT.md         # Environment validation results
│
├── tests/                            # Testing framework
│   ├── test_environment.py          # Environment validation suite
│   ├── test_gui_launch.py           # GUI launch testing
│   ├── test_pdf_export.py           # PDF export testing
│   ├── environment_test_minimal.yml # Test environment configuration
│   ├── _test_launcher.sh            # Test launcher script
│   ├── 🧪 Test Microwell GUI.command # Test double-click launcher
│   ├── test_gui/                    # GUI component tests
│   ├── test_data/                   # Database tests
│   └── test_utils/                  # Utility function tests
│
├── test_input_data_files/            # Example data files
│   ├── example_database.db          # Sample SQLite database
│   ├── example_database.csv         # Sample CSV data
│   └── RM5097_layout.csv           # Example layout file
│
├── plans/                            # Development documentation
│   ├── microwell_plate_gui_design_specification.md
│   ├── conda_distribution_setup.md
│   └── [other planning documents]
│
├── debug/                            # Debug utilities
│   └── debug_verbose_output.sh      # Verbose debugging script
│
└── .benchmarks/                      # Performance benchmarks
```

## 🎯 Key Features

- **Intuitive GUI**: Easy-to-use interface for plate layout design
- **Flexible Layouts**: Support for various plate formats and sample types
- **Automated Export**: One-click CSV and PDF generation
- **Cross-Platform**: Works on Intel and Apple Silicon Macs
- **Minimal Dependencies**: Only 3 conda packages required
- **Self-Validating**: Automated testing ensures reliability

## 🔧 Technical Details

### Dependencies
- **Python**: ≥3.8 (includes tkinter, sqlite3, and standard library)
- **Ghostscript**: ≥10.0 (for PDF export via ps2pdf)
- **Pip**: Package manager for future extensions

### Architecture
- **GUI Framework**: tkinter (built into Python)
- **Database**: SQLite3 (built into Python)
- **Export Formats**: CSV (standard library) + PDF (via Ghostscript)
- **Testing**: pytest + custom validation suite

## 📖 Documentation

- **[Installation Guide](docs/INSTALLATION.md)**: Detailed setup instructions
- **[Distribution Guide](docs/README_DISTRIBUTION.md)**: Package distribution information
- **[Validation Report](docs/VALIDATION_REPORT.md)**: Environment testing results

## 🧪 Testing

Run the comprehensive test suite:
```bash
python tests/test_environment.py
```

Or test individual components:
```bash
python tests/test_gui_launch.py    # GUI functionality
python tests/test_pdf_export.py    # PDF export
pytest tests/                      # Full test suite
```

## 🚀 Distribution

The project includes multiple distribution options:

1. **End User Package**: Complete with launchers and documentation
2. **Developer Setup**: Source code with development tools
3. **Minimal Environment**: Optimized for production deployment
4. **Conservative Environment**: Maximum compatibility fallback

## 🔄 Recent Updates

- ✅ **Minimal Environment**: Reduced from 80+ to 3 packages
- ✅ **Cross-Platform**: Intel and Apple Silicon Mac support
- ✅ **Automated Testing**: Comprehensive validation suite
- ✅ **Clean Organization**: Structured project layout
- ✅ **Updated Documentation**: Complete installation guides

## 📝 License

[Add your license information here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📞 Support

For issues or questions:
1. Check the [Installation Guide](docs/INSTALLATION.md)
2. Run the validation suite: `python tests/test_environment.py`
3. Review the [Validation Report](docs/VALIDATION_REPORT.md)

---

**Version**: 2.0 (Minimal Environment Release)  
**Last Updated**: February 2026  
**Tested On**: macOS 15.6.1 (Intel + Apple Silicon)