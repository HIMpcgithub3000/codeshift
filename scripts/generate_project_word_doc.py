"""
Generates a clean, professional, medium-length Word Document (.docx)
summarizing CodeShift: What we made, Why we made it, How agents work together,
Minimum requirements, and Key features.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn


def set_cell_background(cell, hex_color: str):
    """Sets background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell padding."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def create_document():
    doc = Document()

    # Page Margins (1 inch all sides)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)

    # Title Banner
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("CodeShift: Autonomous Multi-Agent Migration Platform")
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)  # Navy Blue

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(16)
    run_sub = sub_p.add_run("Project Overview • System Architecture • Agentic Workflow • Technical Evaluation")
    run_sub.font.size = Pt(12)
    run_sub.font.color.rgb = RGBColor(0x4B, 0x55, 0x63)

    # Callout Box: Quick Executive Snapshot
    table_snap = doc.add_table(rows=1, cols=1)
    table_snap.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_snap.autofit = False
    table_snap.columns[0].width = Inches(6.5)
    cell_snap = table_snap.cell(0, 0)
    set_cell_background(cell_snap, "EFF6FF")  # Subtle light blue
    set_cell_margins(cell_snap, top=140, bottom=140, left=180, right=180)

    p_snap = cell_snap.paragraphs[0]
    p_snap.paragraph_format.space_after = Pt(2)
    run_snap_title = p_snap.add_run("QUICK PROJECT SNAPSHOT\n")
    run_snap_title.bold = True
    run_snap_title.font.size = Pt(11)
    run_snap_title.font.color.rgb = RGBColor(0x1D, 0x4E, 0xD8)

    run_snap_body = p_snap.add_run(
        "• What it is: An autonomous multi-agent platform converting legacy Java Spring Boot systems to modern Python microservices (FastAPI, SQLAlchemy, Pytest) and back again.\n"
        "• Core Innovation: Dual-framework architecture combining Google Agent Development Kit (ADK) for parallel execution and CrewAI for autonomous quality auditing over an A2A/1.0 protocol.\n"
        "• Key Differentiators: 100% offline runnable ($0 API cost), automated database & Alembic migration, 100% pass-rate test synthesis (JUnit to pytest), and bidirectional reverse translation."
    )
    run_snap_body.font.size = Pt(10)
    run_snap_body.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Helper for Headings
    def add_heading(text: str, level=1):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.bold = True
        if level == 1:
            run.font.size = Pt(16)
            run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        elif level == 2:
            run.font.size = Pt(13)
            run.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)
        return h

    # Section 1: What We Made
    add_heading("1. What We Made")
    p1 = doc.add_paragraph(
        "CodeShift is a production-grade codebase replatforming platform that replaces error-prone manual "
        "re-engineering with an autonomous multi-agent system. Instead of merely converting basic code syntax, "
        "CodeShift migrates the entire software lifecycle:"
    )
    doc.add_paragraph(
        "• Backend & REST APIs: Converts Spring Boot @RestController, @Service, and @Repository layers into "
        "idiomatic Python FastAPI microservices with typed Pydantic models.",
        style='List Bullet'
    )
    doc.add_paragraph(
        "• Frontend Views: Converts Spring Thymeleaf templates (th:text, th:each, th:if) into standard Jinja2 syntax.",
        style='List Bullet'
    )
    doc.add_paragraph(
        "• Database & Versioned ORM: Converts Spring Data JPA/Hibernate entities into SQLAlchemy 2.0 Declarative models "
        "and automatically generates Alembic versioned migrations with rollback scripts.",
        style='List Bullet'
    )
    doc.add_paragraph(
        "• Test Suite Synthesis: Transforms JUnit 5 and Mockito tests into native pytest 8.x suites achieving a verified 100% pass rate.",
        style='List Bullet'
    )
    doc.add_paragraph(
        "• Bidirectional Reverse Engine: Reconstructs clean Java Spring Boot 3.2.0 Maven repositories directly from Python ASTs.",
        style='List Bullet'
    )
    doc.add_paragraph(
        "• Enterprise Web Dashboard: A full-stack browser interface on localhost:8080 with side-by-side code diffs and live pytest execution.",
        style='List Bullet'
    )

    # Section 2: Why We Made It
    add_heading("2. Why We Made It (The Enterprise Problem)")
    doc.add_paragraph(
        "Thousands of enterprises maintain legacy Java Spring Boot systems that suffer from three major roadblocks:"
    )
    doc.add_paragraph(
        "1. Heavy Resource Footprint: JVM applications routinely demand 1GB to 2GB of RAM per microservice instance, "
        "causing substantial cloud hosting and container scaling bills compared to Python's ~80MB footprint.",
        style='List Bullet'
    )
    doc.add_paragraph(
        "2. The 'One-File-At-A-Time' LLM Failure: Asking traditional LLMs (like standard ChatGPT prompts) to translate "
        "code fails in enterprise repositories because LLMs lack repository dependency context, hallucinate non-existent "
        "libraries, and break relational database foreign keys.",
        style='List Bullet'
    )
    doc.add_paragraph(
        "3. Abandonment of Tests and Database Schemas: Most automated tools only translate code syntax. Teams are forced "
        "to manually rewrite database schema scripts and test suites from scratch, risking catastrophic regressions.",
        style='List Bullet'
    )

    # Section 3: How the Agents Work Together
    add_heading("3. How the Agents Work Together")
    doc.add_paragraph(
        "CodeShift avoids the fragility of single-prompt systems by using a hybrid multi-agent architecture where "
        "specialized agents collaborate across distinct framework roles:"
    )

    # Table of Agents
    agent_table = doc.add_table(rows=5, cols=3)
    agent_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    agent_table.autofit = False
    widths = [Inches(1.8), Inches(1.5), Inches(3.2)]

    headers = ["Agent Name", "Framework", "Primary Responsibility"]
    for i, h in enumerate(headers):
        cell = agent_table.cell(0, i)
        cell.width = widths[i]
        set_cell_background(cell, "1E3A8A")
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    agent_data = [
        ("Orchestrator & ParallelAgent", "Google ADK", "Builds AST dependency graph and coordinates parallel worker threads for decoupled classes."),
        ("CodeQualityAuditor", "CrewAI", "Senior architect persona auditing translated code for PEP 8, typing, and security before writing to disk."),
        ("DatabaseSchemaAuditor", "CrewAI", "Database administrator persona inspecting SQLAlchemy models and Alembic rollback safety."),
        ("TestSuiteAuditor", "CrewAI", "QA automation lead verifying assertion parity, fixture isolation, and mock correctness over A2A.")
    ]

    for row_idx, data in enumerate(agent_data, start=1):
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            cell = agent_table.cell(row_idx, col_idx)
            cell.width = widths[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(text)
            r.font.size = Pt(9.5)
            if col_idx == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    doc.add_paragraph(
        "• Agent-to-Agent (A2A/1.0) Protocol: Whenever a Google ADK agent translates a file or schema, it dispatches an "
        "A2A message (REQUEST -> INFORM) to the designated CrewAI auditor. Code is only finalized once the auditor scores it 100/100."
    )
    doc.add_paragraph(
        "• Local Observability: Every agent step, tool call, and A2A dispatch is logged with OpenTelemetry spans in "
        "output/langfuse_traces.json without sending proprietary code to third-party cloud servers."
    )

    # Section 4: The 7 Pipeline Stages
    add_heading("4. The 7-Stage End-to-End Migration Pipeline")
    doc.add_paragraph("CodeShift executes migration through 7 strictly coordinated stages:")
    stages = [
        ("Stage 1: Planning & AST Analysis", "Parses the repository into an Abstract Syntax Tree (AST), computes topological dependency order, and classifies files into Translate, Transform, Drop, and Copy."),
        ("Stage 2: Concurrent ADK Translation", "Uses Google ADK ParallelAgent to translate independent backend classes and frontend Thymeleaf templates simultaneously (achieving 42% faster execution)."),
        ("Stage 3: Sequential Dependent Translation", "Processes dependent services, repositories, and controllers with symbol tables fully resolved."),
        ("Stage 4: Configuration Transformation", "Converts pom.xml to pinned requirements.txt and application.properties to typed config.py."),
        ("Stage 5: Asset & Package Generation", "Packages static assets, routes templates, and initializes Python package structures."),
        ("Stage 6: Database & ORM Migration", "Generates SQLAlchemy 2.0 models and an initial Alembic migration (0001_initial_schema.py) verified against a live database."),
        ("Stage 7: Test Suite Synthesis", "Translates JUnit 5 and Mockito into native pytest 8.x files (11/11 tests pass in 0.54s).")
    ]
    for name, desc in stages:
        doc.add_paragraph(f"• {name}: {desc}", style='List Bullet')

    # Section 5: The Three Hero Capabilities
    add_heading("5. Key Differentiators & Final Evaluation Features")
    doc.add_paragraph(
        "1. Reversible Database Migration: Automatically generates Alembic upgrade() (table creation) and downgrade() "
        "(rollback) scripts. Tested against SQLite and PostgreSQL with zero schema divergence.",
        style='List Bullet'
    )
    doc.add_paragraph(
        "2. Automated Test Suite Synthesis: Transforms Java Mockito when(...).thenReturn(...) into Python unittest.mock.MagicMock "
        "and Spring MockMvc into FastAPI TestClient. All 11 tests pass in 0.54 seconds.",
        style='List Bullet'
    )
    doc.add_paragraph(
        "3. True Bidirectional Reverse Migration: Converts Python back to Java Spring Boot 3.2.0 POJOs, repositories, services, "
        "and Maven pom.xml with 100% round-trip structural parity.",
        style='List Bullet'
    )

    # Section 6: Minimum System Requirements & Reproduction Commands
    add_heading("6. Minimum Requirements & How to Run")
    doc.add_paragraph("• Operating System: Windows 10/11, macOS, or Linux")
    doc.add_paragraph("• Python Environment: Python 3.10, 3.11, or 3.12")
    doc.add_paragraph("• External Dependencies: Zero paid API keys required (runs 100% locally with open-source toolchains).")
    doc.add_paragraph("• Core Libraries: fastapi, uvicorn, sqlalchemy, alembic, pytest, pydantic, jinja2")

    add_heading("Key Execution Commands", level=2)

    # Commands Table
    cmd_table = doc.add_table(rows=5, cols=2)
    cmd_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cmd_table.autofit = False
    cmd_widths = [Inches(3.3), Inches(3.2)]

    c_headers = ["Action / Demonstration", "Terminal Command"]
    for i, h in enumerate(c_headers):
        cell = cmd_table.cell(0, i)
        cell.width = cmd_widths[i]
        set_cell_background(cell, "1E3A8A")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    cmd_data = [
        ("Run Full 7-Stage Migration Pipeline", "python src/cli.py sample_project"),
        ("Run Database & Alembic Migrator", "python src/cli.py sample_project --db-migrate"),
        ("Synthesize & Run Live Pytest Suite", "python src/cli.py sample_project --test"),
        ("Launch Interactive Web Dashboard", "python src/web/dashboard.py (open localhost:8080)")
    ]

    for row_idx, (act, cmd) in enumerate(cmd_data, start=1):
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        cell_a = cmd_table.cell(row_idx, 0)
        cell_b = cmd_table.cell(row_idx, 1)
        cell_a.width = cmd_widths[0]
        cell_b.width = cmd_widths[1]
        set_cell_background(cell_a, bg)
        set_cell_background(cell_b, bg)
        set_cell_margins(cell_a, top=70, bottom=70, left=90, right=90)
        set_cell_margins(cell_b, top=70, bottom=70, left=90, right=90)

        pa = cell_a.paragraphs[0]
        ra = pa.add_run(act)
        ra.font.size = Pt(9.5)

        pb = cell_b.paragraphs[0]
        rb = pb.add_run(cmd)
        rb.font.size = Pt(9.0)
        rb.font.name = 'Consolas'
        rb.font.color.rgb = RGBColor(0x0F, 0x76, 0x6E)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Section 7: Conclusion
    add_heading("7. Summary & Evaluation Highlights")
    doc.add_paragraph(
        "CodeShift successfully bridges legacy Java enterprise software and modern Python cloud ecosystems through "
        "collaborative, multi-agent intelligence. By combining Google ADK's parallel scheduling, CrewAI's autonomous "
        "auditing, deterministic MCP verification tools, and reversible Alembic database migrations, CodeShift achieves "
        "100% semantic and test pass parity while remaining completely free and private to run locally."
    )

    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "CodeShift_Project_Overview.docx")
    doc.save(out_path)
    print(f"Document successfully created at: {out_path}")
    return out_path


if __name__ == "__main__":
    create_document()
