from typing import List, Optional, Union
from pydantic import BaseModel
from datetime import datetime


class Media(BaseModel):
    id: int
    name: str
    alternativeText: str
    caption: str
    width: Optional[int]
    height: Optional[int]
    format: Optional[str]
    hash: str
    ext: str
    mime: str
    size: float
    url: str
    previewUrl: Optional[str]
    provider: str
    provider_metadata: Optional[str]
    created_at: datetime
    updated_at: datetime
    related: List[int]
    sha256: Optional[str]


class MediaCreate(BaseModel):
    event: str
    created_at: datetime
    media: Media


class MediaUpdate(BaseModel):
    event: str
    created_at: datetime
    media: Media
