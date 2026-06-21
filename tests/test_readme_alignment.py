from pathlib import Path
import importlib
import tomllib


def test_pyproject_scripts_define_expected_cli_entrypoints():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    scripts = pyproject["project"]["scripts"]
    expected_scripts = {
        "kmds-summary-log": "kmds.cli.summary_ingest:main",
        "kmds-exec-summary": "kmds.cli.executive_summary:main",
        "kmds-search": "kmds.cli.semantic_search:main",
        "kmds-ask": "kmds.cli.search_orchestrator:main",
        "kmds-observe": "kmds.cli.natural_language_observation:main",
    }

    assert scripts == expected_scripts

    for entrypoint in expected_scripts.values():
        module_name, attr_name = entrypoint.split(":")
        module = importlib.import_module(module_name)
        assert hasattr(module, attr_name)


def test_readme_contains_companion_install_command():
    readme_text = Path("README.md").read_text(encoding="utf-8")
    assert (
        "pip install kmds-data-helper kmds-ui kmds-featurization kmds-modeling" in readme_text
    )


def test_repository_does_not_ship_external_companion_packages():
    src_root = Path("src")
    external_modules = [
        "kmds_data_helper",
        "kmds_ui",
        "kmds_featurization",
        "kmds_modeling",
    ]

    all_paths = [p for p in src_root.rglob("*") if p.is_dir() or p.is_file()]
    names = {p.name for p in all_paths}

    for module_name in external_modules:
        assert module_name not in names
