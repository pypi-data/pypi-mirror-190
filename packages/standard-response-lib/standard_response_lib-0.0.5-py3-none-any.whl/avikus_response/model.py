from typing import Optional, Dict

from pydantic import BaseModel


class StandardResponse(BaseModel):
    """
    StandardResponse model without detail
    """
    code: int
    message: str
    result: Optional[Dict]

    def __getitem__(self, item):
        return getattr(self, item)


class _StandardResponse(BaseModel):
    code: int
    message: str
    result: Optional[Dict]
    detail: Optional[str]

    def __getitem__(self, item):
        return getattr(self, item)
