from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class Posting:
    source_url: str
    title: Optional[str]
    company: Optional[str]
    location: Optional[str]
    full_description: str
    responsibilities: List[str]
    qualifications: List[str]
    skills: List[str]
    salary: Optional[str]
    job_type: Optional[str]

    def to_dict(self):
        return asdict(self)
    
