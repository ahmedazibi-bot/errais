"""
ERRAIS Interactive Application
User-friendly menu-driven interface for irrigation design
"""

import os
import sys
import json
from pathlib import Path
from main import ERRAIS


class InteractiveApp:
    """Interactive menu application for ERRAIS"""
    
    def __init__(self):
        """Initialize the application"""
        self.errais = ERRAIS()
        self.current_project = None
        self.current_design = None
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, text):
        """Print section header"""
        print("\n" + "="*60)
        print(f"  {text}")
        print("="*60)
    
    def print_menu(self, title, options):
        """Print menu options"""
        print(f"\n{title}")
        print("-" * 60)
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        print(f"  0. Back/Exit")
    
    def get_input(self, prompt="Select option: "):
        """Get user input"""
        try:
            choice = input(f"\n{prompt}").strip()
            return choice
        except KeyboardInterrupt:
            print("\n\n❌ Operation cancelled")
            return None
    
    def main_menu(self):
        """Main menu"""
        while True:
            self.clear_screen()
            self.print_header("🌾 ERRAIS - Irrigation Design System")
            
            options = [
                "➕ Create New Project",
                "📂 Load Land Boundary (GeoJSON)",
                "🎯 Generate Irrigation Design",
                "📊 Generate Reports (Word + Excel)",
                "📍 View Sprinkler Coordinates",
                "💧 Assess Water Quality",
                "📚 Browse Crop Library",
                "💧 Browse Water Quality Library",
                "🔧 Browse Hydraulic Constraints",
                "⚙️  View Configuration",
                "❌ Exit"
            ]
            
            self.print_menu("Main Menu", options)
            
            if self.current_project:
                print(f"\n📌 Current Project: {self.errais.projects.get(self.current_project, {}).get('project_name', 'N/A')}")
            
            choice = self.get_input()
            
            if choice == '1':
                self.create_project()
            elif choice == '2':
                self.load_land_boundary()
            elif choice == '3':
                self.generate_design()
            elif choice == '4':
                self.generate_reports()
            elif choice == '5':
                self.view_sprinklers()
            elif choice == '6':
                self.assess_water()
            elif choice == '7':
                self.browse_crops()
            elif choice == '8':
                self.browse_water_quality()
            elif choice == '9':
                self.browse_hydraulics()
            elif choice == '10':
                self.view_config()
            elif choice == '11' or choice == '0':
                print("\n👋 Thank you for using ERRAIS!")
                sys.exit(0)
            else:
                print("❌ Invalid option")
                input("Press Enter to continue...")
    
    def create_project(self):
        """Create a new project"""
        self.print_header("➕ Create New Project")
        
        project_name = input("Project name: ").strip()
        if not project_name:
            print("❌ Project name required")
            return
        
        client_name = input("Client name: ").strip()
        location = input("Location: ").strip()
        
        try:
            area_ha = float(input("Area (hectares): ").strip())
        except ValueError:
            print("❌ Invalid area")
            return
        
        # Select crop
        crops = self.errais.get_crops()
        print("\n📚 Available Crops:")
        for i, crop in enumerate(crops, 1):
            print(f"  {i}. {crop.get('name')}")
        
        crop_choice = input("Select crop (number): ").strip()
        try:
            crop_idx = int(crop_choice) - 1
            crop_id = crops[crop_idx].get('id')
        except (ValueError, IndexError):
            print("❌ Invalid crop selection")
            return
        
        # Select water source
        waters = self.errais.get_water_sources()
        print("\n💧 Available Water Sources:")
        for i, water in enumerate(waters, 1):
            print(f"  {i}. {water.get('name')}")
        
        water_choice = input("Select water source (number): ").strip()
        try:
            water_idx = int(water_choice) - 1
            water_id = waters[water_idx].get('id')
        except (ValueError, IndexError):
            print("❌ Invalid water source selection")
            return
        
        # Select hydraulic system
        systems = self.errais.get_hydraulic_systems()
        print("\n🔧 Available Hydraulic Systems:")
        for i, system in enumerate(systems, 1):
            print(f"  {i}. {system.get('name')}")
        
        system_choice = input("Select system (number): ").strip()
        try:
            system_idx = int(system_choice) - 1
            system_id = systems[system_idx].get('id')
        except (ValueError, IndexError):
            print("❌ Invalid system selection")
            return
        
        # Create project
        project_data = {
            'project_name': project_name,
            'client_name': client_name,
            'location': location,
            'area_ha': area_ha,
            'crop_id': crop_id,
            'water_id': water_id,
            'hydraulic_constraint_id': system_id
        }
        
        project_id = self.errais.create_project(project_data)
        self.current_project = project_id
        
        print(f"✅ Project created successfully!")
        print(f"Project ID: {project_id}")
        input("Press Enter to continue...")
    
    def load_land_boundary(self):
        """Load land boundary from GeoJSON"""
        self.print_header("📂 Load Land Boundary")
        
        geojson_path = input("Enter GeoJSON file path: ").strip()
        
        if self.errais.load_land_data(geojson_path):
            print("✅ Land boundary loaded!")
        else:
            print("❌ Failed to load land boundary")
        
        input("Press Enter to continue...")
    
    def generate_design(self):
        """Generate irrigation design"""
        if not self.current_project:
            print("❌ Please create a project first")
            input("Press Enter to continue...")
            return
        
        self.print_header("🎯 Generate Irrigation Design")
        
        try:
            spacing = float(input("Sprinkler spacing (meters): ").strip())
            discharge = float(input("Discharge (L/min): ").strip())
        except ValueError:
            print("❌ Invalid input")
            return
        
        design_params = {
            'spacing': spacing,
            'discharge': discharge
        }
        
        design_id = self.errais.generate_design(self.current_project, design_params)
        self.current_design = design_id
        
        print(f"✅ Design generated!")
        print(f"Design ID: {design_id}")
        input("Press Enter to continue...")
    
    def generate_reports(self):
        """Generate professional reports"""
        if not self.current_project or not self.current_design:
            print("❌ Please create a project and design first")
            input("Press Enter to continue...")
            return
        
        self.print_header("📊 Generate Reports")
        
        reports = self.errais.generate_report(self.current_project, self.current_design)
        
        if reports:
            print("✅ Reports generated:")
            print(f"  📄 Word Report: {reports.get('word_report')}")
            print(f"  📊 Excel Report: {reports.get('excel_report')}")
        else:
            print("❌ Failed to generate reports")
        
        input("Press Enter to continue...")
    
    def view_sprinklers(self):
        """View sprinkler coordinates"""
        if not self.current_design:
            print("❌ No design available")
            input("Press Enter to continue...")
            return
        
        self.print_header("📍 Sprinkler Coordinates")
        
        design = self.errais.designs.get(self.current_design, {})
        coordinates = design.get('sprinkler_coordinates', [])
        
        if coordinates:
            print(f"Total Sprinklers: {len(coordinates)}")
            for i, coord in enumerate(coordinates[:10], 1):
                print(f"  {i}. X: {coord.get('x', 'N/A')}, Y: {coord.get('y', 'N/A')}")
            if len(coordinates) > 10:
                print(f"  ... and {len(coordinates) - 10} more")
        else:
            print("No sprinkler coordinates available")
        
        input("Press Enter to continue...")
    
    def assess_water(self):
        """Assess water quality"""
        self.print_header("💧 Water Quality Assessment")
        
        if not self.current_project:
            print("❌ Please select a project first")
            input("Press Enter to continue...")
            return
        
        project = self.errais.projects.get(self.current_project, {})
        water_id = project.get('water_id')
        
        water_quality = self.errais.assess_water_quality(water_id)
        
        if water_quality:
            print(f"Water Source: {water_quality.get('name')}")
            print(f"  pH: {water_quality.get('ph')}")
            print(f"  EC (dS/m): {water_quality.get('ec_ds_m')}")
            print(f"  SAR: {water_quality.get('sar')}")
            print(f"  Salinity (ppm): {water_quality.get('salinity_ppm')}")
            print(f"  Suitability: {water_quality.get('suitability')}")
        else:
            print("❌ Water quality information not found")
        
        input("Press Enter to continue...")
    
    def browse_crops(self):
        """Browse crop library"""
        self.print_header("📚 Crop Library")
        
        crops = self.errais.get_crops()
        
        if crops:
            print(f"Total Crops: {len(crops)}\n")
            for crop in crops:
                print(f"🌾 {crop.get('name')}")
                print(f"   ID: {crop.get('id')}")
                print(f"   Kc (mid): {crop.get('kc_mid')}")
                print(f"   Root Depth: {crop.get('root_depth_m')}m")
                print(f"   Growing Period: {crop.get('growing_period_days')} days")
                print()
        else:
            print("No crops available")
        
        input("Press Enter to continue...")
    
    def browse_water_quality(self):
        """Browse water quality library"""
        self.print_header("💧 Water Quality Library")
        
        waters = self.errais.get_water_sources()
        
        if waters:
            print(f"Total Water Sources: {len(waters)}\n")
            for water in waters:
                print(f"💧 {water.get('name')}")
                print(f"   ID: {water.get('id')}")
                print(f"   pH: {water.get('ph')}")
                print(f"   EC: {water.get('ec_ds_m')} dS/m")
                print(f"   Suitability: {water.get('suitability')}")
                print()
        else:
            print("No water sources available")
        
        input("Press Enter to continue...")
    
    def browse_hydraulics(self):
        """Browse hydraulic constraints"""
        self.print_header("🔧 Hydraulic Constraints")
        
        systems = self.errais.get_hydraulic_systems()
        
        if systems:
            print(f"Total Systems: {len(systems)}\n")
            for system in systems:
                print(f"🔧 {system.get('name')}")
                print(f"   ID: {system.get('id')}")
                print(f"   Type: {system.get('type')}")
                print(f"   Pressure: {system.get('min_pressure_kpa')}-{system.get('max_pressure_kpa')} kPa")
                print(f"   Max Velocity: {system.get('max_velocity_m_s')} m/s")
                print()
        else:
            print("No hydraulic systems available")
        
        input("Press Enter to continue...")
    
    def view_config(self):
        """View configuration"""
        self.print_header("⚙️  Configuration")
        
        config = self.errais.view_config()
        
        for key, value in config.items():
            if 'KEY' not in key.upper() or value == '':
                print(f"  {key}: {value}")
        
        input("Press Enter to continue...")
    
    def run(self):
        """Start the application"""
        try:
            self.main_menu()
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    app = InteractiveApp()
    app.run()
