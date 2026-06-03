SETUP_GUIDE - ERRAIS Installation & Configuration

# 🌾 ERRAIS Setup Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Configuration](#configuration)
4. [Verification](#verification)
5. [First Run](#first-run)
6. [Advanced Setup](#advanced-setup)
7. [Uninstallation](#uninstallation)

---

## System Requirements

### Operating System
- Windows 10 or later
- macOS 10.14 or later
- Linux (Ubuntu 18.04+ recommended)

### Python
- Python 3.9 or higher
- pip (Python package manager)

### Database
- MongoDB 4.4+ (optional, can use default settings)

### Disk Space
- ~500 MB for installation
- ~1-5 GB for project data (depending on usage)

### Memory
- Minimum: 2 GB RAM
- Recommended: 4 GB+ RAM

### Internet
- Required for OpenAI API calls
- Recommended bandwidth: 1 Mbps+


---

## Installation Methods

### Method 1: Automated Setup (Recommended)

#### Step 1: Clone Repository
```bash
git clone https://github.com/ahmedazibi-bot/errais.git
cd errais
```

#### Step 2: Run Setup Script
```bash
python setup.py
```

The setup script will:
✓ Check Python version (3.9+)
✓ Create virtual environment (venv/)
✓ Install all dependencies
✓ Configure .env file
✓ Create project directories
✓ Generate library JSON files
✓ Create startup scripts
✓ Verify installation

#### Step 3: Follow Prompts
- Enter OpenAI API key (optional)
- Confirm installation settings

That's it! Installation is complete.


### Method 2: Manual Setup

#### Step 1: Clone Repository
```bash
git clone https://github.com/ahmedazibi-bot/errais.git
cd errais
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Configure Environment
```bash
# Copy template
cp .env.example .env

# Edit .env with your settings
# Windows: notepad .env
# macOS/Linux: nano .env
```

#### Step 5: Create Directories
```bash
mkdir -p config libraries core ai_layer data_layer reporting utils reports logs data
```

#### Step 6: Create Library Files

Create `libraries/crops.json`:
```json
{
  "crops": [
    {
      "id": "wheat_001",
      "name": "Wheat",
      "kc_mid": 1.15,
      "root_depth_m": 1.0,
      "water_sensitivity": 0.8,
      "growing_period_days": 150,
      "irrigation_methods": ["sprinkler", "flood"]
    }
  ]
}
```

Create `libraries/water_quality.json`:
```json
{
  "water_sources": [
    {
      "id": "well_001",
      "name": "Well Water",
      "ph": 7.5,
      "ec_ds_m": 0.8,
      "sar": 3.0,
      "salinity_ppm": 520,
      "suitability": "Excellent"
    }
  ]
}
```

Create `libraries/hydraulic_constraints.json`:
```json
{
  "systems": [
    {
      "id": "sprinkler_std_001",
      "name": "Standard Sprinkler System",
      "type": "Sprinkler",
      "min_pressure_kpa": 200,
      "max_pressure_kpa": 400,
      "recommended_spacing_m": 6.0,
      "max_velocity_m_s": 2.0,
      "pipe_diameters_mm": [25, 32, 40, 50]
    }
  ]
}
```

#### Step 7: Verify Installation
```bash
python -c "from main import ERRAIS; ERRAIS()"
```

You should see: `✅ ERRAIS v1.0.0 initialized`


---

## Configuration

### Environment Variables (.env)

#### Database Configuration
```env
# MongoDB connection
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=errais
```

#### AI/LLM Configuration
```env
# Get API key from https://platform.openai.com/api-keys
LLM_API_KEY=sk-your-api-key-here
LLM_MODEL=gpt-4-turbo
LLM_TEMPERATURE=0.7
```

#### Application Settings
```env
DEBUG=True
LOG_LEVEL=INFO
REPORTS_FOLDER=./reports
DATA_FOLDER=./data
```

#### Default Values
```env
DEFAULT_SPRINKLER_SPACING=6.0
DEFAULT_PIPE_DIAMETER=50
MAX_SPRINKLER_VELOCITY=2.0
MIN_SPRINKLER_PRESSURE=200
```

#### Path Configuration
```env
LIBRARIES_PATH=./libraries
CONFIG_PATH=./config
```

### MongoDB Setup (Optional)

If you want to use MongoDB instead of in-memory storage:

#### Windows
```cmd
# Download from: https://www.mongodb.com/try/download/community
# Run installer, select "Install as Service"
# MongoDB starts automatically

# Test connection:
mongosh
```

#### macOS
```bash
# Install via Homebrew
brew tap mongodb/brew
brew install mongodb-community

# Start service
brew services start mongodb-community

# Test connection:
mongosh
```

#### Linux (Ubuntu)
```bash
# Install MongoDB
sudo apt-get install -y mongodb

# Start service
sudo systemctl start mongodb

# Test connection:
mongosh
```

#### Docker (All Platforms)
```bash
# Pull and run MongoDB container
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Verify
docker logs mongodb
```


---

## Verification

### Test Installation
```bash
# Activate virtual environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Test imports
python -c "import shapely, pymongo, pydantic; print('✅ All modules loaded')"

# Test ERRAIS
python -c "from main import ERRAIS; e = ERRAIS(); print('✅ ERRAIS initialized')"

# Test app
python app.py
```

### Check System Info
```bash
# Python version
python --version

# Installed packages
pip list | grep -E "shapely|pymongo|pydantic|python-docx|openpyxl|pandas"

# Virtual environment
which python  # macOS/Linux
where python  # Windows
```

### Verify File Structure
```
errais/
├── setup.py ✓
├── app.py ✓
├── main.py ✓
├── run_design.py ✓
├── requirements.txt ✓
├── .env ✓
├── .env.example ✓
├── QUICKSTART.txt ✓
├── SETUP_GUIDE.md ✓
├── README.md ✓
├── venv/ ✓
├── libraries/ ✓
│   ├── crops.json ✓
│   ├── water_quality.json ✓
│   └── hydraulic_constraints.json ✓
├── config/ ✓
├── core/ ✓
├── ai_layer/ ✓
├── data_layer/ ✓
├── reporting/ ✓
├── utils/ ✓
├── reports/ ✓
├── logs/ ✓
└── data/ ✓
```


---

## First Run

### Quick Start
```bash
# 1. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 2. Run interactive app
python app.py

# 3. Follow menu prompts
```

### Example Workflow
1. Select: Option 1 (Create New Project)
2. Fill: Project name, client name, location, area
3. Select: Crop, water source, hydraulic system
4. Select: Option 3 (Generate Design)
5. Enter: Spacing (6.0), discharge (2500)
6. Select: Option 4 (Generate Reports)
7. Check: ./reports/ folder for outputs

### Run Example
```bash
python run_design.py
```

This demonstrates a complete automated workflow.


---

## Advanced Setup

### Development Setup
```bash
# Install development tools
pip install -e .
pip install pytest black flake8 sphinx

# Run tests (when available)
pytest tests/

# Code formatting
black .

# Linting
flake8 .
```

### Docker Setup
```bash
# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
EOF

# Build image
docker build -t errais .

# Run container
docker run -it errais
```

### IDE Configuration

#### VS Code
1. Create `.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.pylintEnabled": true,
  "python.linting.pylintPath": "${workspaceFolder}/venv/bin/pylint"
}
```

#### PyCharm
1. Settings > Project > Python Interpreter
2. Click gear icon > Add
3. Select "Existing Environment"
4. Navigate to: `errais/venv/bin/python` (macOS/Linux) or `errais\venv\Scripts\python.exe` (Windows)

### Virtual Environment Management

List environments:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

Deactivate:
```bash
deactivate
```

Recreate:
```bash
rm -rf venv  # or: rmdir /s venv (Windows)
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)
pip install -r requirements.txt
```


---

## Uninstallation

### Remove ERRAIS
```bash
# Deactivate virtual environment
deactivate

# Remove repository
cd ..
rm -rf errais  # or: rmdir /s errais (Windows)
```

### Remove MongoDB (if installed)

#### Windows
- Control Panel > Programs > Programs and Features
- Uninstall "MongoDB Server"

#### macOS
```bash
brew uninstall mongodb-community
```

#### Linux
```bash
sudo apt-get remove mongodb
```

#### Docker
```bash
docker stop mongodb
docker rm mongodb
```


---

## Troubleshooting Setup

### Python Not Found
```bash
# Check if Python is installed
python --version

# If not found:
# Windows: Download from python.org, add to PATH
# macOS: brew install python3
# Linux: sudo apt-get install python3 python3-pip
```

### Virtual Environment Issues
```bash
# Recreate from scratch
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Dependency Conflicts
```bash
# Update pip
pip install --upgrade pip

# Clear cache and reinstall
pip cache purge
pip install -r requirements.txt
```

### Permission Denied (macOS/Linux)
```bash
chmod +x venv/bin/activate
chmod +x run.sh
```

### MongoDB Connection Fails
```bash
# Verify MongoDB is running
mongosh

# If not running:
# Windows: mongod.exe
# macOS: brew services start mongodb-community
# Linux: sudo systemctl start mongodb
```

### Library Files Missing
```bash
# Regenerate libraries
python setup.py

# Then select option to recreate libraries
```


---

## Next Steps

1. **Read Documentation**
   - Check QUICKSTART.txt for quick reference
   - Read README.md for full documentation

2. **Run Example**
   - Execute: `python run_design.py`
   - See complete workflow in action

3. **Create First Project**
   - Run: `python app.py`
   - Follow interactive menu

4. **Check Reports**
   - Look in: `./reports/` folder
   - Download Word and Excel files

5. **Configure API Key**
   - Get key from: https://platform.openai.com/api-keys
   - Add to: `.env` file
   - Restart application

6. **Explore Features**
   - Browse crop library
   - View water quality data
   - Examine hydraulic systems
   - Generate designs

---

## Support

- **GitHub Issues**: https://github.com/ahmedazibi-bot/errais/issues
- **Documentation**: README.md, QUICKSTART.txt, this file
- **Community**: GitHub Discussions

---

**Installation Complete! Happy Designing! 🌾**
