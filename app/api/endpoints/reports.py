from fastapi import APIRouter
from typing import List
import os
import re

router = APIRouter()

@router.get("/reports", response_model=List[str])
async def get_reports():
    """
    Returns a list of available reports in the output directory.
    """
    reports = []
    for filename in os.listdir("output"):
        if filename.endswith(".md"):
            # Sanitize the filename to prevent path traversal
            sanitized_filename = re.sub(r'[^a-zA-Z0-9_.-]', '', filename)
            if sanitized_filename == filename:
                reports.append(filename)
    return reports
