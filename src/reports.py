from __future__ import annotations

from datetime import date
from enum import Enum
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, model_validator
from weasyprint import HTML


class Address(BaseModel):
    street: str
    postal_code: int
    city: str


def convert_empty_str_to_none(data: dict, fields: list[str]) -> dict:
    for field in fields:
        if field in data and data[field] == "":
            data[field] = None
    return data


class CompanyInfo(BaseModel):
    name: str
    address: Address
    department: str | None = None
    phone: str | None = None
    email: str | None = None
    website: str | None = None
    logo: Path | None = None

    @model_validator(mode="before")
    @classmethod
    def empty_str_to_none(cls, data):
        return convert_empty_str_to_none(
            data, ["department", "phone", "email", "website"]
        )


class ProjectInfo(BaseModel):
    name: str
    address: Address | None = None
    number: str | None = None  # an optional identifier (e.g. an ID like `137`)
    email: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    members: list[ProjectMember] | None = None

    @model_validator(mode="before")
    @classmethod
    def empty_str_to_none(cls, data):
        return convert_empty_str_to_none(
            data, ["number", "email", "start_date", "end_date"]
        )


class ProjectMember(BaseModel):
    first_name: str
    last_name: str
    role: str | None = None
    company: str | None = None

    @model_validator(mode="before")
    @classmethod
    def empty_str_to_none(cls, data):
        return convert_empty_str_to_none(data, ["role", "company"])


class ReportInfo(BaseModel):
    title: str
    date: date
    weather: str | None = None
    description: str | None = None
    start_time: str | None = None
    end_time: str | None = None

    @model_validator(mode="before")
    @classmethod
    def empty_str_to_none(cls, data):
        return convert_empty_str_to_none(
            data, ["weather", "description", "start_time", "end_time"]
        )


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


async def create_report(
    template_directory: Path,
    images_directory: Path,
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
        base_url=images_directory,
    ).write_pdf(output_path.as_posix())

    print(f"PDF report generated in '{output_path.as_posix()}'")
