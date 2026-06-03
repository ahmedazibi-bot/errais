#!/usr/bin/env python3
"""
ERRAIS Setup Script
Automated installation, configuration, and verification
"""

import os
import sys
import subprocess
import platform
import json
import shutil
from pathlib import Path

class SetupManager:
    def __init__(self):
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        self.os_type = platform.system()
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        
    def print_header(self, text):
        print("\n" + "="*60)
        print(f"  {text}")
        print("="*60)
    
    def print_step(self, step_num, text):
        print(f"\n[STEP {step_num}] {text}...")
    
    def print_success(self, text):
        print(f"✅ {text}")
    
    def print_error(self, text):
        print(f"❌ {text}")
    
    def print_warning(self, text):
        print(f"⚠️  {text}")
    
    def check_python_version(self):
        """Check if Python version is 3.9 or higher"""
        self.print_step(1, "Checking Python version")
        
        if sys.version_info < (3, 9):
            self.print_error(f"Python 3.9+ required. You have {self.python_version}")
            sys.exit(1)
        
        self.print_success(f"Python {self.python_version} detected")
    
    def create_virtual_environment(self):
        """Create virtual environment"""
        self.print_step(2, "Creating virtual environment")
        
        if self.venv_path.exists():
            self.print_warning("Virtual environment already exists")
            response = input("Do you want to recreate it? (y/n): ").lower()
            if response == 'y':
                shutil.rmtree(self.venv_path)
            else:
                self.print_success("Using existing virtual environment")
                return
        
        try:
            subprocess.check_call([sys.executable, "-m", "venv", str(self.venv_path)])
            self.print_success("Virtual environment created")
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to create virtual environment: {e}")
            sys.exit(1)
    
    def get_pip_executable(self):
        """Get the pip executable for the virtual environment"""
        if self.os_type == "Windows":
            return str(self.venv_path / "Scripts" / "pip.exe")
        else:
            return str(self.venv_path / "bin" / "pip")
    
    def install_dependencies(self):
        """Install required packages"""
        self.print_step(3, "Installing dependencies")
        
        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            self.print_error("requirements.txt not found")
            sys.exit(1)
        
        pip_exec = self.get_pip_executable()
        
        try:
            # Upgrade pip first
            subprocess.check_call([pip_exec, "install", "--upgrade", "pip"])
            # Install requirements
            subprocess.check_call([pip_exec, "install", "-r", str(requirements_file)])
            self.print_success("All dependencies installed")
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to install dependencies: {e}")
            sys.exit(1)
    
    def create_directories(self):
        """Create necessary project directories"""
        self.print_step(4, "Creating project directories")
        
        directories = [
            "config",
            "libraries",
            "core",
            "ai_layer",
            "data_layer",
            "reporting",
            "utils",
            "reports",
            "logs",
            "data"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(exist_ok=True)
            
            # Create __init__.py for Python packages
            if directory not in ["reports", "logs", "data"]:
                init_file = dir_path / "__init__.py"
                init_file.touch()
        
        self.print_success(f"Created {len(directories)} directories")
    
    def setup_environment_file(self):
        """Setup .env file from template"""
        self.print_step(5, "Configuring environment variables")
        
        env_file = self.project_root / ".env"
        env_example = self.project_root / ".env.example"
        
        if env_file.exists():
            self.print_warning(".env file already exists")
        else:
            if env_example.exists():
                shutil.copy(env_example, env_file)
                self.print_success(".env file created from template")
            else:
                # Create default .env
                env_content = """# ERRAIS Configuration

# Database
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=errais

# AI/LLM
LLM_API_KEY=sk-your-api-key-here
LLM_MODEL=gpt-4-turbo
LLM_TEMPERATURE=0.7

# Application
DEBUG=True
LOG_LEVEL=INFO
REPORTS_FOLDER=./reports
DATA_FOLDER=./data

# Defaults
DEFAULT_SPRINKLER_SPACING=6.0
DEFAULT_PIPE_DIAMETER=50
MAX_SPRINKLER_VELOCITY=2.0
MIN_SPRINKLER_PRESSURE=200

# Paths
LIBRARIES_PATH=./libraries
CONFIG_PATH=./config
"""
                with open(env_file, 'w') as f:
                    f.write(env_content)
                self.print_success(".env file created with default values")
        
        # Prompt for API key
        api_key = input("\nEnter your OpenAI API Key (or press Enter to skip): ").strip()
        if api_key:
            self._update_env_file('LLM_API_KEY', api_key)
            self.print_success("OpenAI API key configured")
    
    def _update_env_file(self, key, value):
        """Update a specific key in .env file"""
        env_file = self.project_root / ".env"
        
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        with open(env_file, 'w') as f:
            for line in lines:
                if line.startswith(f"{key}="):
                    f.write(f"{key}={value}\n")
                else:
                    f.write(line)
    
    def create_library_files(self):
        """Create default library JSON files"""
        self.print_step(6, "Creating library files")
        
        libraries_path = self.project_root / "libraries"
        
        # Crops library
        crops_data = {
            "crops": [
                {
                    "id": "wheat_001",
                    "name": "Wheat",
                    "kc_mid": 1.15,
                    "root_depth_m": 1.0,
                    "water_sensitivity": 0.8,
                    "growing_period_days": 150,
                    "irrigation_methods": ["sprinkler", "flood"]
                },
                {
                    "id": "corn_001",
                    "name": "Corn",
                    "kc_mid": 1.2,
                    "root_depth_m": 1.2,
                    "water_sensitivity": 0.9,
                    "growing_period_days": 140,
                    "irrigation_methods": ["drip", "sprinkler"]
                },
                {
                    "id": "tomato_001",
                    "name": "Tomato",
                    "kc_mid": 1.0,
                    "root_depth_m": 0.6,
                    "water_sensitivity": 0.95,
                    "growing_period_days": 180,
                    "irrigation_methods": ["drip"]
                },
                {
                    "id": "potato_001",
                    "name": "Potato",
                    "kc_mid": 1.1,
                    "root_depth_m": 0.5,
                    "water_sensitivity": 0.85,
                    "growing_period_days": 120,
                    "irrigation_methods": ["sprinkler", "flood"]
                },
                {
                    "id": "alfalfa_001",
                    "name": "Alfalfa",
                    "kc_mid": 1.0,
                    "root_depth_m": 2.0,
                    "water_sensitivity": 0.7,
                    "growing_period_days": 365,
                    "irrigation_methods": ["sprinkler"]
                }
            ]
        }
        
        # Water quality library
        water_data = {
            "water_sources": [
                {
                    "id": "well_001",
                    "name": "Well Water",
                    "ph": 7.5,
                    "ec_ds_m": 0.8,
                    "sar": 3.0,
                    "salinity_ppm": 520,
                    "suitability": "Excellent"
                },
                {
                    "id": "river_001",
                    "name": "River Water",
                    "ph": 7.2,
                    "ec_ds_m": 0.5,
                    "sar": 1.5,
                    "salinity_ppm": 320,
                    "suitability": "Good"
                },
                {
                    "id": "treated_001",
                    "name": "Treated Municipal Water",
                    "ph": 7.0,
                    "ec_ds_m": 0.3,
                    "sar": 0.8,
                    "salinity_ppm": 150,
                    "suitability": "Excellent"
                }
            ]
        }
        
        # Hydraulic constraints library
        hydraulic_data = {
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
                },
                {
                    "id": "drip_001",
                    "name": "Drip Irrigation System",
                    "type": "Drip",
                    "min_pressure_kpa": 100,
                    "max_pressure_kpa": 200,
                    "recommended_spacing_m": 1.0,
                    "max_velocity_m_s": 0.5,
                    "pipe_diameters_mm": [16, 20, 25]
                },
                {
                    "id": "micro_001",
                    "name": "Micro-irrigation System",
                    "type": "Micro",
                    "min_pressure_kpa": 150,
                    "max_pressure_kpa": 300,
                    "recommended_spacing_m": 2.0,
                    "max_velocity_m_s": 1.5,
                    "pipe_diameters_mm": [20, 25, 32]
                }
            ]
        }
        
        # Save library files
        files = {
            "crops.json": crops_data,
            "water_quality.json": water_data,
            "hydraulic_constraints.json": hydraulic_data
        }
        
        for filename, data in files.items():
            filepath = libraries_path / filename
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        
        self.print_success(f"Created {len(files)} library files")
    
    def verify_installation(self):
        """Verify installation"""
        self.print_step(7, "Verifying installation")
        
        pip_exec = self.get_pip_executable()
        
        required_packages = [
            "shapely",
            "pymongo",
            "python-dotenv",
            "pydantic",
            "python-docx",
            "openpyxl",
            "pandas",
            "requests",
            "openai"
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                subprocess.check_output([pip_exec, "show", package], 
                                      stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                missing_packages.append(package)
        
        if missing_packages:
            self.print_warning(f"Missing packages: {', '.join(missing_packages)}")
            self.print_warning("Reinstalling dependencies...")
            subprocess.check_call([pip_exec, "install", "-r", 
                                 str(self.project_root / "requirements.txt")])
        else:
            self.print_success(f"All {len(required_packages)} required packages installed")
    
    def create_startup_scripts(self):
        """Create startup scripts for different OS"""
        self.print_step(8, "Creating startup scripts")
        
        if self.os_type == "Windows":
            # Windows batch script
            batch_content = """@echo off
REM ERRAIS - Windows Startup Script
echo Activating virtual environment...
call venv\\Scripts\\activate.bat
echo Running ERRAIS...
python app.py
pause
"""
            with open(self.project_root / "run.bat", 'w') as f:
                f.write(batch_content)
            self.print_success("Created run.bat")
        else:
            # Unix shell script
            shell_content = """#!/bin/bash
# ERRAIS - Unix Startup Script
echo "Activating virtual environment..."
source venv/bin/activate
echo "Running ERRAIS..."
python app.py
"""
            script_path = self.project_root / "run.sh"
            with open(script_path, 'w') as f:
                f.write(shell_content)
            os.chmod(script_path, 0o755)
            self.print_success("Created run.sh")
    
    def print_final_instructions(self):
        """Print final setup instructions"""
        self.print_header("SETUP COMPLETE ✅")
        
        print("\n🎉 ERRAIS has been successfully set up!")
        print("\n📝 Next Steps:")
        
        if self.os_type == "Windows":
            print("   1. Run the application: .\\run.bat")
        else:
            print("   1. Run the application: ./run.sh")
        
        print("   2. Or manually activate venv and run:")
        if self.os_type == "Windows":
            print("      venv\\Scripts\\activate")
        else:
            print("      source venv/bin/activate")
        
        print("      python app.py")
        
        print("\n📚 Documentation:")
        print("   • README.md - Project overview")
        print("   • .env - Configuration file")
        print("   • libraries/ - Crop and water quality data")
        
        print("\n🔧 Important Configuration:")
        print("   • Edit .env file to add your OpenAI API key")
        print("   • Ensure MongoDB is running locally or update MONGODB_URI")
        
        print("\n💡 Tips:")
        print("   • Check QUICKSTART.txt for quick reference")
        print("   • Run 'python run_design.py' for an example workflow")
        print("   • Generated reports will be saved in ./reports/")
        
        print("\n" + "="*60 + "\n")
    
    def run(self):
        """Execute complete setup"""
        self.print_header("ERRAIS SETUP WIZARD")
        print(f"Python {self.python_version} on {self.os_type}")
        
        try:
            self.check_python_version()
            self.create_virtual_environment()
            self.install_dependencies()
            self.create_directories()
            self.setup_environment_file()
            self.create_library_files()
            self.verify_installation()
            self.create_startup_scripts()
            self.print_final_instructions()
        except KeyboardInterrupt:
            self.print_error("Setup interrupted by user")
            sys.exit(1)
        except Exception as e:
            self.print_error(f"Unexpected error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    manager = SetupManager()
    manager.run()
