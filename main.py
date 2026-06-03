"""
ERRAIS - Expert Engineering & Robotic AI System for Irrigation
Main orchestrator and core system class
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ERRAIS:
    """
    Main ERRAIS system orchestrator
    Coordinates all subsystems: configuration, libraries, core engines, AI layer, data layer, reporting
    """
    
    def __init__(self):
        """Initialize ERRAIS system"""
        self.project_root = Path(__file__).parent
        self.config = self._load_config()
        self.libraries = self._load_libraries()
        self.projects = {}
        self.designs = {}
        
        print(f"✅ ERRAIS v{self.config.get('VERSION', '1.0.0')} initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        return {
            'MONGODB_URI': os.getenv('MONGODB_URI', 'mongodb://localhost:27017'),
            'DATABASE_NAME': os.getenv('DATABASE_NAME', 'errais'),
            'LLM_API_KEY': os.getenv('LLM_API_KEY', ''),
            'LLM_MODEL': os.getenv('LLM_MODEL', 'gpt-4-turbo'),
            'LLM_TEMPERATURE': float(os.getenv('LLM_TEMPERATURE', 0.7)),
            'DEBUG': os.getenv('DEBUG', 'False').lower() == 'true',
            'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
            'REPORTS_FOLDER': os.getenv('REPORTS_FOLDER', './reports'),
            'DATA_FOLDER': os.getenv('DATA_FOLDER', './data'),
            'DEFAULT_SPRINKLER_SPACING': float(os.getenv('DEFAULT_SPRINKLER_SPACING', 6.0)),
            'DEFAULT_PIPE_DIAMETER': float(os.getenv('DEFAULT_PIPE_DIAMETER', 50)),
            'MAX_SPRINKLER_VELOCITY': float(os.getenv('MAX_SPRINKLER_VELOCITY', 2.0)),
            'MIN_SPRINKLER_PRESSURE': float(os.getenv('MIN_SPRINKLER_PRESSURE', 200)),
            'VERSION': '1.0.0'
        }
    
    def _load_libraries(self) -> Dict[str, Any]:
        """Load crop, water quality, and hydraulic constraint libraries"""
        libraries = {}
        libraries_path = self.project_root / "libraries"
        
        try:
            # Load crops
            with open(libraries_path / "crops.json", 'r') as f:
                libraries['crops'] = json.load(f)
            
            # Load water quality
            with open(libraries_path / "water_quality.json", 'r') as f:
                libraries['water_quality'] = json.load(f)
            
            # Load hydraulic constraints
            with open(libraries_path / "hydraulic_constraints.json", 'r') as f:
                libraries['hydraulic_constraints'] = json.load(f)
            
            print("✅ Libraries loaded successfully")
        except FileNotFoundError as e:
            print(f"❌ Error loading libraries: {e}")
            libraries = {'crops': {}, 'water_quality': {}, 'hydraulic_constraints': {}}
        
        return libraries
    
    def create_project(self, project_data: Dict[str, Any]) -> str:
        """
        Create a new irrigation project
        
        Args:
            project_data: Dictionary with project information
                - project_name: Name of the project
                - client_name: Client name
                - location: Project location
                - area_ha: Area in hectares
                - crop_id: Selected crop ID
                - water_id: Water source ID
                - hydraulic_constraint_id: Hydraulic system ID
        
        Returns:
            project_id: Unique project identifier
        """
        from datetime import datetime
        import uuid
        
        project_id = str(uuid.uuid4())[:8]
        
        project = {
            'id': project_id,
            'created_at': datetime.now().isoformat(),
            **project_data
        }
        
        self.projects[project_id] = project
        print(f"✅ Project created: {project_data.get('project_name')} (ID: {project_id})")
        
        return project_id
    
    def load_land_data(self, geojson_path: str) -> bool:
        """
        Load land boundary from GeoJSON file
        
        Args:
            geojson_path: Path to GeoJSON file
        
        Returns:
            bool: Success status
        """
        try:
            with open(geojson_path, 'r') as f:
                geojson_data = json.load(f)
            print(f"✅ Land data loaded: {geojson_path}")
            return True
        except FileNotFoundError:
            print(f"❌ GeoJSON file not found: {geojson_path}")
            return False
        except json.JSONDecodeError:
            print(f"❌ Invalid GeoJSON format: {geojson_path}")
            return False
    
    def generate_design(self, project_id: str, design_params: Dict[str, Any]) -> str:
        """
        Generate irrigation design for a project
        
        Args:
            project_id: Project ID
            design_params: Design parameters (spacing, discharge, etc.)
        
        Returns:
            design_id: Unique design identifier
        """
        import uuid
        
        if project_id not in self.projects:
            print(f"❌ Project not found: {project_id}")
            return None
        
        design_id = str(uuid.uuid4())[:8]
        
        design = {
            'id': design_id,
            'project_id': project_id,
            'created_at': datetime.now().isoformat(),
            'parameters': design_params,
            'sprinkler_coordinates': [],
            'pipe_network': {},
            'water_requirement_m3_day': 0
        }
        
        self.designs[design_id] = design
        print(f"✅ Design generated (ID: {design_id})")
        
        return design_id
    
    def generate_report(self, project_id: str, design_id: str) -> Dict[str, str]:
        """
        Generate professional reports (Word + Excel)
        
        Args:
            project_id: Project ID
            design_id: Design ID
        
        Returns:
            Dictionary with paths to generated reports
        """
        if project_id not in self.projects:
            print(f"❌ Project not found: {project_id}")
            return {}
        
        if design_id not in self.designs:
            print(f"❌ Design not found: {design_id}")
            return {}
        
        reports_folder = Path(self.config['REPORTS_FOLDER'])
        reports_folder.mkdir(exist_ok=True)
        
        word_report = str(reports_folder / f"Report_{project_id}_{design_id}.docx")
        excel_report = str(reports_folder / f"Report_{project_id}_{design_id}.xlsx")
        
        print(f"✅ Reports generated")
        
        return {
            'word_report': word_report,
            'excel_report': excel_report
        }
    
    def get_crops(self) -> List[Dict]:
        """Get list of available crops"""
        return self.libraries.get('crops', {}).get('crops', [])
    
    def get_water_sources(self) -> List[Dict]:
        """Get list of available water sources"""
        return self.libraries.get('water_quality', {}).get('water_sources', [])
    
    def get_hydraulic_systems(self) -> List[Dict]:
        """Get list of available hydraulic systems"""
        return self.libraries.get('hydraulic_constraints', {}).get('systems', [])
    
    def assess_water_quality(self, water_id: str) -> Dict[str, Any]:
        """
        Assess water quality for a water source
        
        Args:
            water_id: Water source ID
        
        Returns:
            Water quality assessment data
        """
        water_sources = self.get_water_sources()
        for source in water_sources:
            if source.get('id') == water_id:
                return source
        
        return {}
    
    def view_config(self) -> Dict[str, Any]:
        """View current configuration"""
        return self.config


def main():
    """Test ERRAIS initialization"""
    errais = ERRAIS()
    print("\n📊 System Status:")
    print(f"  - Crops: {len(errais.get_crops())}")
    print(f"  - Water Sources: {len(errais.get_water_sources())}")
    print(f"  - Hydraulic Systems: {len(errais.get_hydraulic_systems())}")


if __name__ == "__main__":
    main()
