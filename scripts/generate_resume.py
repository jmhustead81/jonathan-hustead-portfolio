"""Generate Jonathan Hustead resume PDF from current portfolio content."""

from pathlib import Path

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    Frame,
    PageTemplate,
    BaseDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "docs" / "Resume_Jonathan_Hustead_Staff_Software_Engineer.pdf"

INK = HexColor("#101318")
MUTED = HexColor("#5c6570")
ACCENT = HexColor("#0f6f69")
RULE = HexColor("#d5dbe3")
LIGHT = HexColor("#f4f6f8")


def styles():
    return {
        "name": ParagraphStyle(
            "name",
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=INK,
            spaceAfter=2,
        ),
        "title": ParagraphStyle(
            "title",
            fontName="Helvetica",
            fontSize=11,
            leading=14,
            textColor=ACCENT,
            spaceAfter=4,
        ),
        "contact": ParagraphStyle(
            "contact",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=MUTED,
            spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=INK,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=INK,
            spaceAfter=6,
        ),
        "role": ParagraphStyle(
            "role",
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=INK,
        ),
        "meta": ParagraphStyle(
            "meta",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=MUTED,
            spaceAfter=3,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName="Helvetica",
            fontSize=9,
            leading=11.5,
            textColor=INK,
            leftIndent=10,
            firstLineIndent=-10,
            spaceAfter=2,
        ),
        "small": ParagraphStyle(
            "small",
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            textColor=INK,
        ),
        "smallBold": ParagraphStyle(
            "smallBold",
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11,
            textColor=INK,
        ),
        "mutedSmall": ParagraphStyle(
            "mutedSmall",
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=MUTED,
        ),
    }


def p(text: str, style):
    return Paragraph(text.replace("&", "&amp;"), style)


def section(title: str, s) -> list:
    return [
        p(title.upper(), s["h2"]),
        HRFlowable(width="100%", thickness=1, color=RULE, spaceBefore=0, spaceAfter=6),
    ]


def job(role, company, location, dates, bullets, s) -> KeepTogether:
    bits = [
        Table(
            [[p(role, s["role"]), p(dates, s["meta"])]],
            colWidths=[4.7 * inch, 2.3 * inch],
        ),
        p(f"{company} | {location}", s["meta"]),
    ]
    bits[0].setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ]
        )
    )
    for b in bullets:
        bits.append(p(f"- {b}", s["bullet"]))
    bits.append(Spacer(1, 6))
    return KeepTogether(bits)


def build():
    s = styles()
    doc = BaseDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.45 * inch,
        title="Jonathan Hustead - Staff Software Engineer",
        author="Jonathan Hustead",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame])])

    summary = (
        "Staff Software Engineer with more than twenty years in front-end development. "
        "I own UI architecture for enterprise products, with a focus on reusable patterns, "
        "accessible interfaces, and systems that stay fast as they grow. Most of my career "
        "has been in financial services and healthcare, with earlier years on large-scale e-commerce."
    )

    experience = [
        (
            "Staff Software Engineer",
            "SS&C Advent",
            "Jacksonville, FL",
            "Aug 2018 - Present",
            [
                "Lead UI architecture for enterprise products, working with design and engineering to define shared templates and patterns teams can reuse.",
                "Build production front-end layouts in .NET and .NET Core with MVC, AngularJS, jQuery, and Kendo UI.",
                "Prototype early with stakeholders so we can prove a flow before wiring it to backend APIs.",
                "Push the stack forward where it counts, including .NET Core 10 work and micro-frontend structures when the app shape starts to get in the way.",
            ],
        ),
        (
            "Web Marketing Manager",
            "Optimum Healthcare IT",
            "Jacksonville, FL",
            "Jun 2016 - Jun 2018",
            [
                "Worked with the Creative Director on design and development for corporate sites and marketing properties.",
                "Built and maintained custom WordPress applications with PHP, jQuery, HTML5, and CSS3.",
            ],
        ),
        (
            "Senior UI Engineer",
            "Clearsense, LLC",
            "Jacksonville, FL",
            "Jun 2015 - Jun 2016",
            [
                "Helped a young startup grow by shaping the first real UI frameworks instead of one-off screens.",
                "Built interactive prototypes in AngularJS, .NET MVC, and jQuery for executive demos and proof-of-concept reviews.",
            ],
        ),
        (
            "Lead Front-End Developer",
            "Fanatics, Inc.",
            "Jacksonville, FL",
            "May 2010 - Jun 2015",
            [
                "Worked with IT, design, SEO, and marketing to define front-end layouts and the technical requirements behind them.",
                "Built prototype pages and style systems that kept branding consistent across hundreds of high-traffic sports storefronts.",
            ],
        ),
    ]

    technical = [
        ".NET Core 10",
        ".NET RCL",
        "ASP.NET MVC",
        "Alpine.js",
        "htmx",
        "AngularJS",
        "jQuery",
        "Tailwind CSS",
        "Bootstrap",
        "Kendo UI",
        "Python",
        "PHP",
        "WordPress",
        "Coveo Search",
    ]
    expertise = [
        "UI/UX Architecture",
        "Design systems",
        "Micro-Frontends",
        "Rapid prototyping",
        "ADA Compliance",
        "E-commerce Systems",
        "Analytics & SEO",
        "Usability Testing",
    ]

    story = []
    story.append(p("JONATHAN HUSTEAD", s["name"]))
    story.append(p("Staff Software Engineer", s["title"]))
    story.append(
        p(
            "Jacksonville, FL  |  jonathanhustead.com  |  linkedin.com/in/jmhustead  |  github.com/jmhustead81",
            s["contact"],
        )
    )

    story.extend(section("Professional Summary", s))
    story.append(p(summary, s["body"]))

    story.extend(section("Professional Experience", s))
    for item in experience:
        story.append(job(*item, s))

    # Skills + education side by side
    tech_text = "  |  ".join(technical)
    expertise_text = "  |  ".join(expertise)

    left = [
        p("TECHNICAL SKILLS", s["smallBold"]),
        Spacer(1, 3),
        HRFlowable(width="100%", thickness=1, color=RULE, spaceBefore=0, spaceAfter=5),
        p(tech_text, s["small"]),
        Spacer(1, 8),
        p("CORE EXPERTISE", s["smallBold"]),
        Spacer(1, 3),
        HRFlowable(width="100%", thickness=1, color=RULE, spaceBefore=0, spaceAfter=5),
        p(expertise_text, s["small"]),
    ]
    right = [
        p("EDUCATION", s["smallBold"]),
        Spacer(1, 3),
        HRFlowable(width="100%", thickness=1, color=RULE, spaceBefore=0, spaceAfter=5),
        p("Master of Science", s["smallBold"]),
        p("Management Information Systems", s["small"]),
        p("University of Central Florida", s["mutedSmall"]),
        p("2007", s["mutedSmall"]),
        Spacer(1, 6),
        p("Bachelor of Science", s["smallBold"]),
        p("Information Technology", s["small"]),
        p("University of Central Florida", s["mutedSmall"]),
        p("2005", s["mutedSmall"]),
    ]

    grid = Table([[left, right]], colWidths=[4.85 * inch, 2.15 * inch])
    grid.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (0, 0), 12),
                ("RIGHTPADDING", (1, 0), (1, 0), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(Spacer(1, 2))
    story.append(grid)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.build(story)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
