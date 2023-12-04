import dataclasses


@dataclasses.dataclass
class Job:
    title: str = ""
    company: str = ""
    location: str = ""
    description: str = ""
    workplace_type: str = ""
    posted_date: str = ""
    applicants_at_time_of_applying: str = ""