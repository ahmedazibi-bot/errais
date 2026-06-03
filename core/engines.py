"""
ERRAIS Geometry Engine
2D geometric processing using Shapely
"""

from shapely.geometry import Point, Polygon, LineString
from typing import List, Dict, Tuple

class GeometryEngine:
    """Handles geometric operations for irrigation design"""
    
    @staticmethod
    def create_grid_sprinklers(polygon: Polygon, spacing: float) -> List[Point]:
        """
        Generate sprinkler positions in a grid pattern
        
        Args:
            polygon: Land boundary polygon
            spacing: Distance between sprinklers
        
        Returns:
            List of sprinkler Point objects
        """
        sprinklers = []
        minx, miny, maxx, maxy = polygon.bounds
        
        x = minx
        while x < maxx:
            y = miny
            while y < maxy:
                point = Point(x, y)
                if polygon.contains(point) or polygon.touches(point):
                    sprinklers.append(point)
                y += spacing
            x += spacing
        
        return sprinklers
    
    @staticmethod
    def calculate_distance(p1: Point, p2: Point) -> float:
        """Calculate distance between two points"""
        return p1.distance(p2)
    
    @staticmethod
    def get_polygon_area(polygon: Polygon) -> float:
        """Get area of polygon in square meters"""
        return polygon.area
    
    @staticmethod
    def get_polygon_perimeter(polygon: Polygon) -> float:
        """Get perimeter of polygon in meters"""
        return polygon.length


class HydraulicEngine:
    """Handles hydraulic calculations"""
    
    @staticmethod
    def calculate_flow_velocity(discharge_lpm: float, diameter_mm: float) -> float:
        """
        Calculate flow velocity in pipes
        
        Args:
            discharge_lpm: Discharge in liters per minute
            diameter_mm: Pipe diameter in millimeters
        
        Returns:
            Velocity in m/s
        """
        # Convert units and calculate
        discharge_m3_s = discharge_lpm / 60000  # L/min to m³/s
        area_m2 = (3.14159 * (diameter_mm / 2000) ** 2)  # mm to m
        
        if area_m2 == 0:
            return 0
        
        velocity_m_s = discharge_m3_s / area_m2
        return velocity_m_s
    
    @staticmethod
    def calculate_pressure_loss(pipe_length_m: float, diameter_mm: float, 
                               discharge_lpm: float) -> float:
        """
        Estimate pressure loss in pipe using simplified Hazen-Williams
        
        Args:
            pipe_length_m: Pipe length in meters
            diameter_mm: Diameter in millimeters
            discharge_lpm: Discharge in L/min
        
        Returns:
            Pressure loss in kPa
        """
        # Simplified calculation (Hazen-Williams)
        Q = discharge_lpm / 1000  # L/min to m³/min
        D = diameter_mm / 25.4  # mm to inches
        
        # Pressure loss per 100 m
        pressure_loss_per_100m = (0.2083 * Q ** 1.852) / (D ** 4.8655)
        
        # Total pressure loss
        total_loss_psi = (pipe_length_m / 100) * pressure_loss_per_100m
        total_loss_kpa = total_loss_psi * 6.89476
        
        return total_loss_kpa
