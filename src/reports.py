import base64
from datetime import date, time
from enum import Enum
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, EmailStr
from weasyprint import HTML


class RowHeaders(Enum):
    IMAGE = "Bilder"
    DESCRIPTION = "Beschreibung"
    ASSIGNEE = "Zuständig"
    DUE_DATE = "Fälligkeit"


class Row(BaseModel):
    images: list[Path] = []
    text_content: str = ""
    assignee: str = ""
    due_date: str = ""


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


class ProjectMember(BaseModel):
    first_name: str
    last_name: str
    role: str | None = None
    company: str | None = None


class ProjectInfo(BaseModel):
    name: str
    address: Address
    number: str | None = None  # an optional identifier (e.g. an ID like `137`)
    email: EmailStr | None = None
    start_date: date | None = None
    end_date: date | None = None
    members: list[ProjectMember] | None = None


class ReportInfo(BaseModel):
    title: str
    date: date
    weather: str | None = None
    description: str | None = None
    start_time: time | None = None
    end_time: time | None = None


def image_to_base64(image_path: str) -> str:
    """Convert image to base64 string"""
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode("utf-8")
    return f"data:image/webp;base64,{encoded_string}"


def create_report(
    env_path,
    rows,
    company_info,
    project_info,
    report_info,
):
    # Create HTML content using Jinja2
    env = Environment(loader=FileSystemLoader(env_path))

    # Render main template
    main_template = env.get_template("templates/report_template.html")
    main_html = main_template.render(
        observations=rows,
        headers=RowHeaders,
        company_info=company_info,
        project_info=project_info,
        report_info=report_info,
    )

    # Render footer template
    # footer_template = env.get_template("footer_template.html")
    # footer_html = footer_template.render(company_info=company_info)

    # Create PDF with footer
    HTML(
        string=main_html,
        base_url=env_path,
    ).write_pdf(
        Path("output", "report.pdf").as_posix(),
        # presentational_hints=True,
        # footer_html=footer_html,
    )

    print("PDF report generated as 'report.pdf'")
