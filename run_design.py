"""
ERRAIS - Example Workflow
Demonstrates automated irrigation design workflow
"""

from main import ERRAIS
import json
from datetime import datetime


def run_example():
    """Run a complete example irrigation design workflow"""
    
    print("\n" + "="*60)
    print("  ERRAIS - Example Irrigation Design Workflow")
    print("="*60)
    
    # Initialize ERRAIS
    print("\n[1] Initializing ERRAIS System...")
    errais = ERRAIS()
    
    # Create a project
    print("\n[2] Creating irrigation project...")
    project_data = {
        'project_name': 'Desert Farm Expansion',
        'client_name': 'Ahmed Al-Rashid',
        'location': 'Cairo, Egypt',
        'area_ha': 50,
        'crop_id': 'wheat_001',
        'water_id': 'well_001',
        'hydraulic_constraint_id': 'sprinkler_std_001'
    }
    
    project_id = errais.create_project(project_data)
    print(f"   Project ID: {project_id}")
    print(f"   Project: {project_data['project_name']}")
    print(f"   Area: {project_data['area_ha']} hectares")
    print(f"   Location: {project_data['location']}")
    
    # Get project details
    project = errais.projects[project_id]
    crop = next((c for c in errais.get_crops() if c['id'] == project['crop_id']), None)
    water = next((w for w in errais.get_water_sources() if w['id'] == project['water_id']), None)
    system = next((s for s in errais.get_hydraulic_systems() if s['id'] == project['hydraulic_constraint_id']), None)
    
    print(f"\n   📌 Design Details:")
    print(f"   - Crop: {crop['name']} (Kc: {crop['kc_mid']})")
    print(f"   - Water Source: {water['name']} (Suitability: {water['suitability']})")
    print(f"   - System: {system['name']} (Type: {system['type']})")
    
    # Assess water quality
    print("\n[3] Assessing water quality...")
    water_quality = errais.assess_water_quality(project['water_id'])
    print(f"   ✅ Water Quality Assessment:")
    print(f"   - pH: {water_quality['ph']}")
    print(f"   - EC: {water_quality['ec_ds_m']} dS/m")
    print(f"   - SAR: {water_quality['sar']}")
    print(f"   - Salinity: {water_quality['salinity_ppm']} ppm")
    print(f"   - Status: {water_quality['suitability']}")
    
    # Generate design
    print("\n[4] Generating irrigation design...")
    design_params = {
        'spacing': system['recommended_spacing_m'],
        'discharge': 2500,  # L/min
        'pressure': 250,  # kPa (mid-range)
        'pipe_diameter': 50,  # mm
    }
    
    design_id = errais.generate_design(project_id, design_params)
    design = errais.designs[design_id]
    
    print(f"   Design ID: {design_id}")
    print(f"   📋 Design Parameters:")
    print(f"   - Sprinkler Spacing: {design_params['spacing']}m")
    print(f"   - Discharge: {design_params['discharge']} L/min")
    print(f"   - Operating Pressure: {design_params['pressure']} kPa")
    print(f"   - Pipe Diameter: {design_params['pipe_diameter']}mm")
    
    # Calculate design metrics (simplified)
    print("\n[5] Calculating design metrics...")
    
    # Estimate sprinkler count
    area_m2 = project_data['area_ha'] * 10000
    spacing = design_params['spacing']
    sprinkler_count = int(area_m2 / (spacing * spacing))
    
    # Estimate daily water requirement
    root_depth = crop['root_depth_m']
    water_requirement_daily = area_m2 * root_depth * 0.6  # Simplified: 60% of root depth
    
    # Update design with calculations
    design['sprinkler_count'] = sprinkler_count
    design['estimated_water_m3_day'] = water_requirement_daily / 1000  # Convert to m³
    design['total_pipe_length_m'] = sprinkler_count * spacing * 0.5  # Approximation
    
    print(f"   ✅ Design Calculations:")
    print(f"   - Estimated Sprinklers: {sprinkler_count}")
    print(f"   - Daily Water Requirement: {design['estimated_water_m3_day']:.2f} m³")
    print(f"   - Estimated Pipe Length: {design['total_pipe_length_m']:.2f} m")
    
    # Generate sprinkler coordinates (grid pattern)
    print("\n[6] Generating sprinkler coordinates...")
    sprinklers = []
    cols = int((area_m2 ** 0.5) / spacing)
    rows = int(cols * spacing / spacing)
    
    for i in range(rows):
        for j in range(cols):
            sprinklers.append({
                'id': f"S{i*cols + j + 1}",
                'x': j * spacing,
                'y': i * spacing,
                'discharge_lpm': design_params['discharge'],
                'pressure_kpa': design_params['pressure']
            })
    
    design['sprinkler_coordinates'] = sprinklers[:sprinkler_count]
    print(f"   Generated {len(design['sprinkler_coordinates'])} sprinkler positions")
    
    # Generate reports
    print("\n[7] Generating professional reports...")
    reports = errais.generate_report(project_id, design_id)
    
    if reports:
        print(f"   ✅ Reports Generated:")
        print(f"   📄 Word Report: {reports['word_report']}")
        print(f"   📊 Excel Report: {reports['excel_report']}")
    
    # Summary
    print("\n" + "="*60)
    print("  WORKFLOW SUMMARY")
    print("="*60)
    print(f"✅ Project: {project_data['project_name']}")
    print(f"✅ Project ID: {project_id}")
    print(f"✅ Design ID: {design_id}")
    print(f"✅ Area: {project_data['area_ha']} hectares")
    print(f"✅ Sprinklers: {len(design['sprinkler_coordinates'])}")
    print(f"✅ Daily Water: {design['estimated_water_m3_day']:.2f} m³")
    print(f"✅ Pipe Required: {design['total_pipe_length_m']:.2f} m")
    print("\n" + "="*60)
    print("  ✨ Workflow completed successfully!")
    print("="*60 + "\n")
    
    # Return results
    return {
        'project': project,
        'design': design,
        'reports': reports
    }


if __name__ == "__main__":
    try:
        results = run_example()
        print("\n📊 Results exported to /reports/")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
