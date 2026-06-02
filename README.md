# 🌾 ERRAIS - Expert Engineering & Robotic AI System for Irrigation

> **An intelligent 2D irrigation design system with automated setup, interactive program, and complete workflow**

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-Integration-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🚀 **Quick Start - 3 Commands**

```bash
# 1. Automated setup (one-time)
python setup.py

# 2. Activate virtual environment
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# 3. Run the interactive program
python app.py
```

That's it! Everything else is automated.

---

## ✨ **Features**

### 🎯 **Core Capabilities**
- ✅ 2D Geometric Processing (Shapely)
- ✅ Intelligent Sprinkler Grid Optimization
- ✅ Hydraulic Network Design & Routing
- ✅ AI-Powered Design Recommendations (OpenAI)
- ✅ Water Quality Assessment
- ✅ Professional Report Generation (Word + Excel)
- ✅ MongoDB Data Persistence
- ✅ GeoJSON/GIS Data Support

### 📚 **Knowledge Libraries**
- ✅ **Crops**: 5+ predefined crops with Kc values, root depth, water sensitivity
- ✅ **Water Quality**: 3+ water sources with quality parameters and suitability assessments
- ✅ **Hydraulic Constraints**: 3+ irrigation system types with pressure and velocity limits

### 🔧 **Technical Stack**
| Technology | Purpose |
|-----------|---------|
| Python 3.9+ | Core programming |
| Shapely | 2D geometry processing |
| MongoDB | Document database |
| Pydantic | Data validation |
| OpenAI API | AI design recommendations |
| python-docx | Word report generation |
| openpyxl | Excel report generation |
| pandas | Data analysis |

---

## 📦 **What's Included**

```
errais/
├── setup.py                    ← RUN THIS FIRST
├── app.py                      ← Interactive program
├── run_design.py               ← Example workflow
├── main.py                     ← Core system
├── requirements.txt            ← Dependencies
├── .env.example               ← Config template
├── QUICKSTART.txt             ← Quick reference
│
├── config/                    ← Settings & DB
├── libraries/                 ← Crops, water, hydraulic data
├── core/                      ← Design engines
├── ai_layer/                  ← LLM integration
├── data_layer/                ← MongoDB
├── reporting/                 ← Report generation
├── utils/                     ← Helpers
└── reports/                   ← Generated reports
```

---

## 🔧 **Installation**

### **Method 1: Automated Setup (Recommended)**

```bash
# Clone repository
git clone https://github.com/ahmedazibi-bot/errais.git
cd errais

# Run automated setup
python setup.py
```

The setup script will:
1. ✅ Check Python version
2. ✅ Create virtual environment
3. ✅ Install all dependencies
4. ✅ Configure environment variables
5. ✅ Create necessary folders
6. ✅ Verify installation

### **Method 2: Manual Setup**

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings
```

---

## 💻 **Usage**

### **Option 1: Interactive Application (Recommended)**

```bash
# Activate virtual environment first
source venv/bin/activate  # or: venv\Scripts\activate (Windows)

# Run the interactive program
python app.py
```

**Menu Options:**
1. ➕ Create New Project
2. 📂 Load Land Boundary (GeoJSON)
3. 🎯 Generate Irrigation Design
4. 📊 Generate Reports (Word + Excel)
5. 📍 View Sprinkler Coordinates
6. 💧 Assess Water Quality
7. 📚 Browse Crop Library
8. 💧 Browse Water Quality Library
9. 🔧 Browse Hydraulic Constraints
10. ⚙️  View Configuration
11. ❌ Exit

### **Option 2: Automated Example**

```bash
python run_design.py
```

This runs a complete example workflow automatically.

### **Option 3: Python Code**

```python
from main import ERRAIS

# Initialize
errais = ERRAIS()

# Create project
project_id = errais.create_project({
    'project_name': 'My Farm',
    'client_name': 'John Doe',
    'location': 'Cairo',
    'area_ha': 50,
    'crop_id': 'wheat_001',
    'water_id': 'well_001',
    'hydraulic_constraint_id': 'sprinkler_std_001'
})

# Load land boundary
errais.load_land_data('land_boundary.geojson')

# Generate design
design_id = errais.generate_design(project_id, {
    'spacing': 6.0,
    'discharge': 2500
})

# Generate reports
reports = errais.generate_report(project_id, design_id)
print(f"Word Report: {reports['word_report']}")
print(f"Excel Report: {reports['excel_report']}")
```

---

## 📋 **Configuration**

Edit `.env` file to configure:

```env
# Database
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=errais

# AI/LLM
LLM_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxx
LLM_MODEL=gpt-4-turbo
LLM_TEMPERATURE=0.7

# Application
DEBUG=True
LOG_LEVEL=INFO
REPORTS_FOLDER=./reports

# Defaults
DEFAULT_SPRINKLER_SPACING=6.0
DEFAULT_PIPE_DIAMETER=50
MAX_SPRINKLER_VELOCITY=2.0
MIN_SPRINKLER_PRESSURE=200
```

---

## 📚 **Libraries Overview**

### **Crops Library** (`libraries/crops.json`)
Pre-configured crops with:
- Crop coefficients (Kc values)
- Root depth information
- Water sensitivity indices
- Growing periods
- Suitable irrigation methods

**Example crops:**
- Wheat, Corn, Tomato, Potato, Alfalfa

### **Water Quality Library** (`libraries/water_quality.json`)
Water sources with:
- pH, EC, SAR values
- Salt concentrations
- Suitability assessments
- Usage restrictions

**Example sources:**
- Well, River, Treated Municipal

### **Hydraulic Constraints** (`libraries/hydraulic_constraints.json`)
System specifications:
- Pressure ranges (kPa)
- Velocity limits (m/s)
- Pipe diameters (mm)
- Sprinkler spacing recommendations

**Example systems:**
- Standard Sprinkler, Drip, Micro-irrigation

---

## 📊 **Generated Reports**

### **Word Report** (Professional)
- Project Information
- Design Summary
- Pipe Network Details
- Water Quality Assessment
- Crop Requirements

### **Excel Report** (Detailed)
- Project Info Sheet
- Design Results
- Water Quality Data
- Crop Information
- **Bill of Quantities (BOQ)**
- Sprinkler Coordinates

---

## 🔍 **System Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   app.py     │  │ run_design   │  │ Python Code  │       │
│  │(Interactive) │  │  (Example)   │  │  (API Use)   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                      MAIN ORCHESTRATOR (main.py)            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ ERRAIS Class - Coordinates all subsystems           │  │
│  └──────────────────────────────────────────────────────┘  │
└─┬───┬───────────┬───────────┬──────────┬────────────────┬─┘
  │   │           │           │          │                │
  ▼   ▼           ▼           ▼          ▼                ▼
┌──────┐ ┌─────────────┐ ┌──────────┐ ┌────────┐ ┌─────────┐
│CONFIG│ │  LIBRARIES  │ │CORE      │ │AI_LAYER│ │DATA_    │
│      │ │             │ │ENGINES   │ │        │ │LAYER    │
│Setup │ │Crops        │ │Geometry  │ │Prompt  │ │MongoDB  │
│DB    │ │Water        │ │Sprinkler │ │Builder │ │Models   │
│Env   │ │Hydraulic    │ │Pipe      │ │LLM     │ │Repo     │
└──────┘ └─────────────┘ │Calculate │ │Int     │ │Pattern  │
                          └──────────┘ └────────┘ └─────────┘
                                │
                          ┌─────▼──────┐
                          │ REPORTING  │
                          │            │
                          │Word Gen    │
                          │Excel Gen   │
                          │Report Mgr  │
                          └────────────┘
```

---

## 🛠️ **Troubleshooting**

### **Problem: MongoDB Connection Error**
```
❌ Error: Could not connect to MongoDB
```
**Solution:**
```bash
# Ensure MongoDB is running
# Windows: mongod should start automatically after install
# Mac: brew services start mongodb-community
# Linux: sudo systemctl start mongodb

# Test connection:
python -c "from pymongo import MongoClient; MongoClient('mongodb://localhost:27017').admin.command('ping')"
```

### **Problem: Module Not Found**
```
❌ ModuleNotFoundError: No module named 'shapely'
```
**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate  # or: venv\Scripts\activate (Windows)

# Reinstall dependencies
pip install -r requirements.txt
```

### **Problem: OpenAI API Error**
```
❌ Error: Invalid API key
```
**Solution:**
1. Get API key from https://platform.openai.com/api-keys
2. Update `.env` file with correct key
3. Ensure you have credits on your OpenAI account

### **Problem: Permission Denied (Mac/Linux)**
```
❌ Permission denied: 'venv/bin/python'
```
**Solution:**
```bash
chmod +x venv/bin/python
source venv/bin/activate
```

---

## 📖 **Documentation**

- **QUICKSTART.txt** - Quick reference guide
- **SETUP_GUIDE.md** - Detailed setup instructions
- **Inline Docstrings** - See function docstrings in Python files

---

## 🎯 **Workflow Example**

```
┌─────────────────────────────────────────────────────────┐
│                     START                               │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────▼──────────────┐
         │ 1. Run setup.py          │
         │    (One-time setup)      │
         └───────────┬──────────────┘
                     │
         ┌───────────▼──────────────┐
         │ 2. Activate venv         │
         │    (source venv/bin/act) │
         └───────────┬──────────────┘
                     │
         ┌───────────▼──────────────┐
         │ 3. Run app.py            │
         │    (Interactive program) │
         └───────────┬──────────────┘
                     │
    ┌────────────────▼────────────────┐
    │ 4. Create Project (Menu Option 1)
    └────────────────┬────────────────┘
                     │
    ┌────────────────▼─────────────────┐
    │ 5. Load Land Boundary (Option 2) │
    └────────────────┬─────────────────┘
                     │
    ┌────────────────▼──────────────────┐
    │ 6. Generate Design (Option 3)     │
    └────────────────┬──────────────────┘
                     │
    ┌────────────────▼──────────────────┐
    │ 7. Generate Reports (Option 4)    │
    └────────────────┬──────────────────┘
                     │
    ┌────────────────▼──────────────────┐
    │ 8. View Reports in /reports       │
    └────────────────┬──────────────────┘
                     │
         ┌───────────▼──────────────┐
         │       SUCCESS ✅         │
         └──────────────────────────┘
```

---

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 **License**

This project is licensed under the MIT License - see LICENSE file for details

---

## 🙋 **Support**

- **Issues**: https://github.com/ahmedazibi-bot/errais/issues
- **Documentation**: See SETUP_GUIDE.md and QUICKSTART.txt
- **Email**: support@errais.dev

---

## 🌟 **Roadmap**

- [ ] Web UI interface
- [ ] Multi-language support
- [ ] DXF/CAD export
- [ ] Mobile app
- [ ] Advanced ML optimization
- [ ] Real-time monitoring
- [ ] Integration with remote sensing

---

## 📞 **Quick Links**

- **Repository**: https://github.com/ahmedazibi-bot/errais
- **Python Package Index**: (coming soon)
- **Documentation**: See included guides
- **Issues**: GitHub Issues

---

**Made with ❤️ for sustainable irrigation design**

*Last Updated: 2024*
*Version: 1.0.0*
