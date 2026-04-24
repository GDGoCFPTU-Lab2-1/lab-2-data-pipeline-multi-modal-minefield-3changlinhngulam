from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# ==========================================
# v1 schema — anticipate v2 field renames at T+60min

class UnifiedDocument(BaseModel):
    document_id: str
    content: str
    source_type: str  # 'PDF' | 'Video' | 'HTML' | 'CSV' | 'Code'
    author: Optional[str] = "Unknown"
    timestamp: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)
    source_metadata: dict = Field(default_factory=dict)

    class Config:
        # Allow extra fields to ease v2 migration
        extra = "allow"
