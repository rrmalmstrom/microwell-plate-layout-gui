# Production Environment Specification

## Production Environment File (`environment.yml`)

Based on your development environment `microwell-gui-dev`, here's the production environment with testing dependencies removed:

```yaml
name: microwell-plate-gui
channels:
  - defaults
dependencies:
  - blas=1.0=openblas
  - bzip2=1.0.8=h80987f9_6
  - ca-certificates=2025.12.2=hca03da5_0
  - expat=2.7.4=h50f4ffc_0
  - libcxx=21.1.8=hb4ce287_0
  - libexpat=2.7.4=h50f4ffc_0
  - libffi=3.4.4=hca03da5_1
  - libgfortran=15.2.0=h09d7db9_1
  - libgfortran5=15.2.0=hb654fa1_1
  - libopenblas=0.3.31=h7813bb4_0
  - libzlib=1.3.1=h5f15de7_0
  - llvm-openmp=20.1.8=he822017_0
  - ncurses=6.5=hee39554_0
  - numpy=2.4.2=py311h4bb6f22_0
  - numpy-base=2.4.2=py311h23175f9_0
  - openssl=3.0.19=ha0b305a_0
  - packaging=25.0=py311hca03da5_1
  - pandas=3.0.0=py311h3f644e9_0
  - pip=26.0.1=pyhc872135_0
  - python=3.11.14=hf701271_0
  - python-dateutil=2.9.0post0=py311hca03da5_2
  - readline=8.3=h0b18652_0
  - setuptools=80.10.2=py311hca03da5_0
  - six=1.17.0=py311hca03da5_0
  - sqlite=3.51.1=hab6afd1_0
  - tk=8.6.15=hcd8a7d5_0
  - tzdata=2025c=he532380_0
  - wheel=0.46.3=py311hca03da5_0
  - xz=5.6.4=h80987f9_1
  - zlib=1.3.1=h5f15de7_0
```

## Removed Development Dependencies

The following dependencies were removed from `environment-dev.yml` as they're only needed for development/testing:

- `iniconfig=2.3.0=py311hca03da5_0` (pytest dependency)
- `pluggy=1.5.0=py311hca03da5_0` (pytest dependency)
- `pygments=2.19.2=py311hca03da5_0` (pytest dependency)
- `pytest=9.0.2=py311hca03da5_0` (testing framework)

## Key Features

1. **Deterministic Build**: All versions exactly match your development environment
2. **Runtime Focus**: Only includes dependencies needed to run the application
3. **Simplified Name**: `microwell-plate-gui` (production) vs `microwell-gui-dev` (development)
4. **macOS Optimized**: Uses the same conda channel and build numbers that work on your system

## Verification

This environment provides:
- Python 3.11.14 with tkinter for GUI
- SQLite 3.51.1 for database operations
- Pandas 3.0.0 and NumPy 2.4.2 for data handling
- All supporting libraries with exact version pins