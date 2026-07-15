"""
Configuration management for Project Prometheus
"""

import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    debug: bool = Field(default=True, env="DEBUG")
    
    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        env="CORS_ORIGINS"
    )
    
    # Google Integration
    google_client_id: str = Field(default="", env="GOOGLE_CLIENT_ID")
    google_client_secret: str = Field(default="", env="GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str = Field(default="", env="GOOGLE_REDIRECT_URI")
    
    # Microsoft Integration
    microsoft_tenant_id: str = Field(default="", env="MICROSOFT_TENANT_ID")
    microsoft_client_id: str = Field(default="", env="MICROSOFT_CLIENT_ID")
    microsoft_client_secret: str = Field(default="", env="MICROSOFT_CLIENT_SECRET")
    
    # Model Paths
    face_landmark_model: str = Field(
        default="models/shape_predictor_68_face_landmarks.dat",
        env="FACE_LANDMARK_MODEL"
    )
    face_recognition_model: str = Field(
        default="models/facenet.h5",
        env="FACE_RECOGNITION_MODEL"
    )
    
    # Database
    database_url: str = Field(default="sqlite:///./prometheus.db", env="DATABASE_URL")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/prometheus.log", env="LOG_FILE")
    
    # File Upload Limits
    max_file_size: int = Field(default=104857600, env="MAX_FILE_SIZE")  # 100MB
    
    # Allowed File Types
    allowed_image_types: List[str] = Field(
        default=["image/jpeg", "image/png", "image/heic"],
        env="ALLOWED_IMAGE_TYPES"
    )
    allowed_video_types: List[str] = Field(
        default=["video/mp4", "video/webm", "video/avi"],
        env="ALLOWED_VIDEO_TYPES"
    )
    allowed_document_types: List[str] = Field(
        default=[
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ],
        env="ALLOWED_DOCUMENT_TYPES"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
