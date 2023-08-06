# METS Tools

The EduceLab METS profile library and tools.

## Requirements
- Python 3.9+

## Installation
```shell
python -m pip install educelab-mets
```

## Usage
### Python API
```python
from educelab import mets
doc = mets.METSDocument.from_file('path/to/document.xml')
```

### METS Editor
#### Install a pre-built binary
Pre-built binaries of METS Editor are provided as artifacts of the CI jobs. Use
the following links to access the latest stable version:
- macOS [[browse]](https://gitlab.com/educelab/mets-tools/-/jobs/artifacts/develop/browse?job=build:macos)
  [[zip]](https://gitlab.com/api/v4/projects/24194363/jobs/artifacts/main/download?job=build:macos)
- Windows [[browse]](https://gitlab.com/educelab/mets-tools/-/jobs/artifacts/develop/browse?job=build:windows)
  [[zip]](https://gitlab.com/api/v4/projects/24194363/jobs/artifacts/main/download?job=build:windows)
- Ubuntu 20.04 [[browse]](https://gitlab.com/educelab/mets-tools/-/jobs/artifacts/develop/browse?job=build:ubuntu:20.04)
  [[zip]](https://gitlab.com/api/v4/projects/24194363/jobs/artifacts/main/download?job=build:ubuntu:20.04)
- Ubuntu 22.04 [[browse]](https://gitlab.com/educelab/mets-tools/-/jobs/artifacts/develop/browse?job=build:ubuntu:22.04)
  [[zip]](https://gitlab.com/api/v4/projects/24194363/jobs/artifacts/main/download?job=build:ubuntu:22.04)

#### Install from source
After following the [installation instructions](#Installation), launch the 
editor from the command line using the following command:

```shell
METSEditor
```

## Building a deployable METS Editor application
A deployable METS editor package can be built using `pyinstaller`:
```shell
# macOS
pyinstaller pyinstaller/METSEditor_macOS.spec
```
```powershell
# Windows
pyinstaller pyinstaller\METSEditor_Windows.spec
```
```shell
# Ubuntu
pyinstaller pyinstaller/METSEditor_Ubuntu.spec
```
        