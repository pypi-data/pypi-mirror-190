"""jobs.py."""
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from strangeworks_core.types.file import File
from strangeworks_core.types.resource import Resource
from strangeworks_core.utils import str_to_datetime


@dataclass
class Job:
    """Object representing a Strangeworks platform job entry."""

    slug: str
    job_id: Optional[str] = None
    child_jobs: Optional[List] = None
    external_identifier: Optional[str] = None
    resource: Optional[Resource] = None
    status: Optional[str] = None
    is_terminal_state: Optional[bool] = False
    remote_status: Optional[str] = None
    job_data_schema: Optional[str] = None
    job_data: Optional[Dict[str, Any]] = None
    files: Optional[List[File]] = None
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None

    @classmethod
    def from_dict(cls, res: Dict[str, Any]) -> "Job":
        """Generate a Job object from dictionary."""

        child_jobs: Optional[List[Job]] = (
            list(map(lambda x: Job.from_dict(x), res.get("childJobs")))
            if "childJobs" in res
            else None
        )

        files: Optional[List[File]] = (
            list(map(lambda x: File.from_dict(x), res.get("files")))
            if "files" in res
            else None
        )

        resource = (
            Resource.from_dict(res.get("resource")) if "resource" in res else None
        )

        return cls(
            job_id=res.get("id"),
            external_identifier=res.get("externalIdentifier"),
            slug=res.get("slug"),
            resource=resource,
            status=res.get("status"),
            is_terminal_state=res.get("isTerminalState"),
            remote_status=res.get("remoteStatus"),
            job_data_schema=res.get("jobDataSchema"),
            job_data=res.get("jobData"),
            child_jobs=child_jobs,
            files=files,
            date_created=str_to_datetime(res.get("dateCreated")),
            date_updated=str_to_datetime(res.get("dateUpdated")),
        )

    def is_complete(self) -> bool:
        """Check if job is in terminal state.

        deprecated method, kept to limit number of changes
        required for extension SDKs
        """
        return self.is_terminal_state
