"""Repository pattern for data access"""
import logging
from typing import Optional, List
from .mongodb_client import MongoDBClient
from .models import ProjectModel, DesignModel

logger = logging.getLogger(__name__)

class ProjectRepository:
    """Project data repository"""
    
    COLLECTION = "projects"
    
    @staticmethod
    def create(project: ProjectModel) -> str:
        """Create new project"""
        doc = project.dict()
        project_id = MongoDBClient.insert_one(ProjectRepository.COLLECTION, doc)
        logger.info(f"Project created: {project_id}")
        return str(project_id)
    
    @staticmethod
    def get_by_id(project_id: str) -> Optional[ProjectModel]:
        """Get project by ID"""
        doc = MongoDBClient.find_one(
            ProjectRepository.COLLECTION,
            {"project_id": project_id}
        )
        return ProjectModel(**doc) if doc else None
    
    @staticmethod
    def get_by_client(client_name: str) -> List[ProjectModel]:
        """Get projects by client name"""
        docs = MongoDBClient.find_many(
            ProjectRepository.COLLECTION,
            {"client_name": client_name}
        )
        return [ProjectModel(**doc) for doc in docs]
    
    @staticmethod
    def list_all(limit: int = 100) -> List[ProjectModel]:
        """List all projects"""
        docs = MongoDBClient.find_many(ProjectRepository.COLLECTION, limit=limit)
        return [ProjectModel(**doc) for doc in docs]
    
    @staticmethod
    def update(project_id: str, updates: dict) -> int:
        """Update project"""
        modified = MongoDBClient.update_one(
            ProjectRepository.COLLECTION,
            {"project_id": project_id},
            updates
        )
        logger.info(f"Updated {modified} project(s)")
        return modified
    
    @staticmethod
    def delete(project_id: str) -> int:
        """Delete project"""
        deleted = MongoDBClient.delete_one(
            ProjectRepository.COLLECTION,
            {"project_id": project_id}
        )
        logger.info(f"Deleted {deleted} project(s)")
        return deleted
    
    @staticmethod
    def count() -> int:
        """Count total projects"""
        return MongoDBClient.count(ProjectRepository.COLLECTION)

class DesignRepository:
    """Design results repository"""
    
    COLLECTION = "designs"
    
    @staticmethod
    def create(design: DesignModel) -> str:
        """Create new design"""
        doc = design.dict()
        design_id = MongoDBClient.insert_one(DesignRepository.COLLECTION, doc)
        logger.info(f"Design created: {design_id}")
        return str(design_id)
    
    @staticmethod
    def get_by_id(design_id: str) -> Optional[DesignModel]:
        """Get design by ID"""
        doc = MongoDBClient.find_one(
            DesignRepository.COLLECTION,
            {"design_id": design_id}
        )
        return DesignModel(**doc) if doc else None
    
    @staticmethod
    def get_by_project(project_id: str, limit: int = 100) -> List[DesignModel]:
        """Get designs for a project"""
        docs = MongoDBClient.find_many(
            DesignRepository.COLLECTION,
            {"project_id": project_id},
            limit=limit
        )
        return [DesignModel(**doc) for doc in docs]
    
    @staticmethod
    def get_latest_for_project(project_id: str) -> Optional[DesignModel]:
        """Get latest design for project"""
        db = MongoDBClient.get_database()
        doc = db[DesignRepository.COLLECTION].find_one(
            {"project_id": project_id},
            sort=[("design_version", -1)]
        )
        return DesignModel(**doc) if doc else None
    
    @staticmethod
    def list_all(limit: int = 100) -> List[DesignModel]:
        """List all designs"""
        docs = MongoDBClient.find_many(DesignRepository.COLLECTION, limit=limit)
        return [DesignModel(**doc) for doc in docs]
    
    @staticmethod
    def update(design_id: str, updates: dict) -> int:
        """Update design"""
        modified = MongoDBClient.update_one(
            DesignRepository.COLLECTION,
            {"design_id": design_id},
            updates
        )
        logger.info(f"Updated {modified} design(s)")
        return modified
    
    @staticmethod
    def delete(design_id: str) -> int:
        """Delete design"""
        deleted = MongoDBClient.delete_one(
            DesignRepository.COLLECTION,
            {"design_id": design_id}
        )
        logger.info(f"Deleted {deleted} design(s)")
        return deleted
    
    @staticmethod
    def count_by_project(project_id: str) -> int:
        """Count designs for a project"""
        return MongoDBClient.count(
            DesignRepository.COLLECTION,
            {"project_id": project_id}
        )
