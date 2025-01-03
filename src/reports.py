from __future__ import annotations

from datetime import date, time
from enum import Enum
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, EmailStr
from weasyprint import HTML


class Address(BaseModel):
    street: str
    postal_code: int
    city: str


class CompanyInfo(BaseModel):
    name: str
    department: str | None = None
    address: Address
    phone: str | None = None
    email: EmailStr | None = None
    website: str | None = None
    logo: Path | None = None


class ProjectInfo(BaseModel):
    name: str
    address: Address
    number: str | None = None  # an optional identifier (e.g. an ID like `137`)
    email: EmailStr | None = None
    start_date: date | None = None
    end_date: date | None = None
    members: list[ProjectMember] | None = None


class ProjectMember(BaseModel):
    first_name: str
    last_name: str
    role: str | None = None
    company: str | None = None


class ReportInfo(BaseModel):
    title: str
    date: date
    weather: str | None = None
    description: str | None = None
    start_time: time | None = None
    end_time: time | None = None


class TableHeaders(Enum):
    IMAGE = "Bilder"
    DESCRIPTION = "Beschreibung"
    ASSIGNEE = "Zuständig"
    DUE_DATE = "Fälligkeit"


class Observation(BaseModel):
    images: list[Path] = []
    text_content: str = ""
    assignee: str = ""
    due_date: str = ""


def create_report(
    template_directory: Path,
    company_info: CompanyInfo,
    project_info: ProjectInfo,
    report_info: ReportInfo,
    table_headers: TableHeaders,
    observations: list[Observation],
    output_path: Path = Path("output", "report.pdf"),
):
    # Setup
    env = Environment(loader=FileSystemLoader(template_directory))

    # Render HTML
    template = env.get_template("template.html")
    html = template.render(
        observations=observations,
        headers=table_headers,
        company_info=company_info,
        project_info=project_info,
        report_info=report_info,
    )

    # Create PDF
    HTML(
        string=html,
        base_url=template_directory,
    ).write_pdf(output_path.as_posix())

    print(f"PDF report generated in '{output_path.as_posix()}'")
