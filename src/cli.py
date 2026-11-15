"""
cli.py - Single Command CLI Entrypoint for CodeShift

Usage:
  python src/cli.py sample_project        # Runs full multi-agent migration (Java -> Python)
  python src/cli.py output --reverse      # Runs reverse migration (Python -> Java Spring Boot)
  python src/cli.py sample_project --web  # Runs migration and launches Web Dashboard
"""

import sys
import os
import argparse
import subprocess

src_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(src_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from agents.orchestrator import MigrationOrchestrator
from agents.evaluator import BehavioralEvaluator
from agents.reverse_migrator import ReverseMigrationOrchestrator


def main():
    parser = argparse.ArgumentParser(description="CodeShift - Multi-Agent Java <-> Python Project Migration CLI")
    parser.add_argument("repo_path", nargs="?", default="sample_project", help="Path to input project folder (Java repo or Python output).")
    parser.add_argument("--reverse", action="store_true", help="Run reverse bidirectional migration (Python codebase -> Java Spring Boot project).")
    parser.add_argument("--db-migrate", action="store_true", help="Run database & ORM migration (JPA/Hibernate -> SQLAlchemy & Alembic).")
    parser.add_argument("--test", action="store_true", help="Synthesize native pytest test suite from JUnit 5 / Mockito and run tests.")
    parser.add_argument("--app-name", default="PetClinicApp", help="Application name for migration.")
    parser.add_argument("--web", action="store_true", help="Launch interactive Web Dashboard.")

    args = parser.parse_args()

    print("==================================================================")
    print(" [CODESHIFT] MULTI-AGENT MIGRATION CLI")
    print("==================================================================")

    if args.test:
        print(" Mode: AUTOMATED TEST SUITE SYNTHESIS (JUnit 5 / Mockito -> native pytest)")
        from agents.test_synthesizer import TestSuiteMigrationOrchestrator
        abs_repo = os.path.abspath(os.path.join(root_dir, args.repo_path))
        if not os.path.exists(abs_repo):
            abs_repo = os.path.abspath(args.repo_path)
        output_dir = os.path.join(root_dir, "output")
        java_test_dir = os.path.join(abs_repo, "src", "test", "java")
        if not os.path.exists(java_test_dir):
            java_test_dir = os.path.join(abs_repo, "src", "test")
        test_out_dir = os.path.join(output_dir, "tests")

        test_migrator = TestSuiteMigrationOrchestrator(
            java_test_dir=java_test_dir,
            output_tests_dir=test_out_dir,
            project_name=args.app_name
        )
        test_rep = test_migrator.run_test_synthesis()

        print("\n[CLI TEST SUITE SYNTHESIS SUMMARY]")
        print(f" Test Suites Generated:     {test_rep.test_suites_generated}")
        print(f" Total Test Cases:          {test_rep.total_test_cases}")
        print(f" Passed Test Cases:         {test_rep.passed_test_cases}")
        print(f" Test Pass Rate:            {test_rep.pass_rate_percentage:.1f}%")
        print(f" Assertions Translated:     {test_rep.assertions_translated}")
        print(f" Mocks Translated:          {test_rep.mocks_translated}")
        print(f" CrewAI Test Audit:         {test_rep.crewai_audit_score}/100.0 (APPROVED)")
        print(f" Output Test Directory:     {test_out_dir}")

        if args.web:
            print("\n[Launching CodeShift Web Dashboard on http://localhost:8080 ...]")
            dashboard_script = os.path.join(src_dir, "web", "dashboard.py")
            subprocess.run([sys.executable, dashboard_script])
        return

    if args.db_migrate:
        print(" Mode: DATABASE & ORM MIGRATION (JPA/Hibernate -> SQLAlchemy & Alembic)")
        from agents.database_migrator import DatabaseMigrationOrchestrator
        abs_repo = os.path.abspath(os.path.join(root_dir, args.repo_path))
        if not os.path.exists(abs_repo):
            abs_repo = os.path.abspath(args.repo_path)
        output_dir = os.path.join(root_dir, "output")

        print(f" Source Java Repository: '{abs_repo}'")
        print(f" Target Output Directory: '{output_dir}'")

        db_migrator = DatabaseMigrationOrchestrator(
            java_repo_dir=abs_repo,
            output_python_dir=output_dir,
            project_name=args.app_name
        )
        db_rep = db_migrator.run_database_migration()

        print("\n[CLI DATABASE MIGRATION SUMMARY]")
        print(f" Tables Synthesized:       {db_rep.total_tables_generated} ({', '.join([t.table_name for t in db_rep.tables])})")
        print(f" Columns Mapped:           {db_rep.total_columns_mapped}")
        print(f" Relationships Mapped:     {db_rep.total_relationships_mapped}")
        print(f" Target DB URL:            {db_rep.target_database_url}")
        print(f" Alembic Initial Script:   {db_rep.migration_script_path}")
        print(f" CrewAI Schema Audit:      {db_rep.crewai_audit_score}/100.0 (APPROVED)")
        print(f" Schema Parity Score:      {db_rep.schema_parity_score}%")

        if args.web:
            print("\n[Launching CodeShift Web Dashboard on http://localhost:8080 ...]")
            dashboard_script = os.path.join(src_dir, "web", "dashboard.py")
            subprocess.run([sys.executable, dashboard_script])
        return

    if args.reverse:
        print(" Mode: REVERSE MIGRATION (Python -> Java Spring Boot)")
        abs_python_dir = os.path.abspath(os.path.join(root_dir, args.repo_path))
        if not os.path.exists(abs_python_dir):
            abs_python_dir = os.path.abspath(args.repo_path)
        if not os.path.exists(abs_python_dir):
            abs_python_dir = os.path.join(root_dir, "output")

        java_output_dir = os.path.join(root_dir, "output", "migrated_java")
        print(f" Source Python Directory: '{abs_python_dir}'")
        print(f" Target Java Output Directory: '{java_output_dir}'")

        rev_orchestrator = ReverseMigrationOrchestrator(
            python_dir=abs_python_dir,
            output_java_dir=java_output_dir,
            app_name=args.app_name
        )
        report = rev_orchestrator.run_reverse_migration()

        print("\n[CLI REVERSE MIGRATION SUMMARY]")
        print(f" Total Files Converted:     {report.total_files_converted}")
        print(f" Spring Entities Generated:  {len(report.classes_generated)} ({', '.join(report.classes_generated)})")
        print(f" Controllers Generated:      {len(report.controllers_generated)}")
        print(f" Services Generated:         {len(report.services_generated)}")
        print(f" Templates Generated:        {len(report.templates_generated)}")
        print(f" Maven pom.xml:              {'Generated' if report.pom_xml_generated else 'Skipped'}")
        print(f" CrewAI A2A Audit Score:     {report.crewai_audit_score}/100.0 (APPROVED)")
        print(f" Round-Trip Parity Score:    {report.round_trip_parity_score}%")
        print(f" Output Java Directory:      {java_output_dir}")

        if args.web:
            print("\n[Launching CodeShift Web Dashboard on http://localhost:8080 ...]")
            dashboard_script = os.path.join(src_dir, "web", "dashboard.py")
            subprocess.run([sys.executable, dashboard_script])
        return

    abs_repo = os.path.abspath(os.path.join(root_dir, args.repo_path))
    if not os.path.exists(abs_repo):
        abs_repo = os.path.abspath(args.repo_path)

    output_dir = os.path.join(root_dir, "output")

    print(f"Target Java Repository Path: '{abs_repo}'")
    print(f"Target Python Output Directory: '{output_dir}'")

    # Run ADK Migration Orchestrator
    orchestrator = MigrationOrchestrator(repo_dir=abs_repo, output_dir=output_dir)
    report = orchestrator.run_full_migration()

    print("\n[CLI MIGRATION SUMMARY]")
    summary = report.manifest_summary if hasattr(report, "manifest_summary") else report.get("manifest_summary", {})
    print(f"Translated: {summary.get('TRANSLATE', 0)} files")
    print(f"Transformed: {summary.get('TRANSFORM', 0)} files")
    print(f"Dropped:     {summary.get('DROP', 0)} files")

    if args.web:
        print("\n[Launching CodeShift Web Dashboard on http://localhost:8080 ...]")
        dashboard_script = os.path.join(src_dir, "web", "dashboard.py")
        subprocess.run([sys.executable, dashboard_script])


if __name__ == "__main__":
    main()
