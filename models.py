from dataclasses import asdict, dataclass


@dataclass
class Job:
    title: str = ""
    company: str = ""
    location: str = ""
    description: str = ""
    workplace_type: str = ""
    posted_date: str = ""
    applicants_at_time_of_applying: str = ""
    linkedin_job_id: str = ""


@dataclass
class JobForVerification:
    linkedinJobId: str
    title: str
    company: str
    workplaceType: str

    def to_dict(self):
        return asdict(self)


@dataclass
class JobCounter:
    total = 0
    applied = 0
    skipped_blacklisted = 0
    skipped_already_applied = 0
    skipped_unanswered_questions = 0