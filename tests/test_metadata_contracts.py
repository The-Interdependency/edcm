from __future__ import annotations

from pathlib import Path

from tools.check_metadata_contracts import verify_skill_lib_identity


ROOT = Path(__file__).resolve().parents[1]
CURRENT_SHA = "c14ee9d500579a4b5d6821f62c9d82ca96e73608"


def _write_identity_fixture(root: Path, *, checker_sha: str = CURRENT_SHA) -> None:
    workflow = root / ".github" / "workflows" / "skill-compliance.yml"
    workflow.parent.mkdir(parents=True)
    workflow.write_text(
        "repository: The-Interdependency/skill-lib\n"
        f"ref: {CURRENT_SHA}\n"
        f"run: checker --sha {checker_sha} \\\n\n",
        encoding="utf-8",
    )
    for relative in (Path("AGENTS.md"), Path("CLAUDE.md"), Path("docs/integrity-gates.md")):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"The-Interdependency/skill-lib@{CURRENT_SHA}\n",
            encoding="utf-8",
        )


def test_current_skill_lib_identity_is_consistent() -> None:
    assert verify_skill_lib_identity(ROOT) == []


def test_skill_lib_identity_drift_is_reported(tmp_path: Path) -> None:
    _write_identity_fixture(tmp_path)

    (tmp_path / "AGENTS.md").write_text(
        "The-Interdependency/skill-lib@a1c6a7124af537ee9937b6fc6084940091982fe5\n",
        encoding="utf-8",
    )

    findings = verify_skill_lib_identity(tmp_path)
    assert [(finding.path, finding.code) for finding in findings] == [
        ("AGENTS.md", "SKILL_LIB_IDENTITY_DRIFT")
    ]


def test_skill_lib_workflow_drift_is_reported(tmp_path: Path) -> None:
    _write_identity_fixture(
        tmp_path,
        checker_sha="a1c6a7124af537ee9937b6fc6084940091982fe5",
    )

    findings = verify_skill_lib_identity(tmp_path)
    assert [(finding.path, finding.code) for finding in findings] == [
        (".github/workflows/skill-compliance.yml", "SKILL_LIB_WORKFLOW_DRIFT")
    ]
