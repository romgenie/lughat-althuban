import os
import pathlib
import subprocess
import sys

from arabicpython.cli import main


def test_01_hello_runs(capsys):
    repo_root = pathlib.Path(__file__).parents[1]
    path = repo_root / "examples" / "01_hello.apy"
    assert main([str(path)]) == 0
    out, _ = capsys.readouterr()
    assert out == "مرحبا، يا عالم\n"


def test_02_arithmetic_runs(capsys):
    repo_root = pathlib.Path(__file__).parents[1]
    path = repo_root / "examples" / "02_arithmetic.apy"
    assert main([str(path)]) == 0
    out, _ = capsys.readouterr()
    assert out == "باقي 40 سنة\n"


def test_03_control_flow_runs(capsys):
    repo_root = pathlib.Path(__file__).parents[1]
    path = repo_root / "examples" / "03_control_flow.apy"
    assert main([str(path)]) == 0
    out, _ = capsys.readouterr()
    expected = "1: فردي\n" "2: زوجي\n" "3: فردي\n" "4: زوجي\n" "5: فردي\n"
    assert out == expected


def test_04_functions_runs(capsys):
    repo_root = pathlib.Path(__file__).parents[1]
    path = repo_root / "examples" / "04_functions.apy"
    assert main([str(path)]) == 0
    out, _ = capsys.readouterr()
    assert out == "15\n12\n"


def test_05_data_structures_runs(capsys):
    repo_root = pathlib.Path(__file__).parents[1]
    path = repo_root / "examples" / "05_data_structures.apy"
    assert main([str(path)]) == 0
    out, _ = capsys.readouterr()
    expected = "تفاح: 3 ريال\n" "موز: 2 ريال\n" "برتقال: 4 ريال\n"
    assert out == expected


def test_06_classes_runs(capsys):
    repo_root = pathlib.Path(__file__).parents[1]
    path = repo_root / "examples" / "06_classes.apy"
    assert main([str(path)]) == 0
    out, _ = capsys.readouterr()
    assert out == "5.0\n"


def test_07_imports_runs_via_subprocess():
    repo_root = pathlib.Path(__file__).parents[1]
    examples_dir = repo_root / "examples"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root) + os.pathsep + env.get("PYTHONPATH", "")
    res = subprocess.run(
        [sys.executable, "-m", "arabicpython.cli", "07_imports.apy"],
        cwd=str(examples_dir),
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    assert res.returncode == 0
    assert res.stdout == "25\n27\n"


def test_all_expected_examples_present():
    repo_root = pathlib.Path(__file__).parents[1]
    examples_dir = repo_root / "examples"
    expected_files = [
        "01_hello.apy",
        "02_arithmetic.apy",
        "03_control_flow.apy",
        "04_functions.apy",
        "05_data_structures.apy",
        "06_classes.apy",
        "07_imports.apy",
        "helper.apy",
        "README.md",
    ]
    for f in expected_files:
        assert (examples_dir / f).exists(), f"Missing expected example file: {f}"


def test_examples_readme_exists_and_lists_all_examples():
    repo_root = pathlib.Path(__file__).parents[1]
    readme_path = repo_root / "examples" / "README.md"
    assert readme_path.exists()
    content = readme_path.read_text(encoding="utf-8")
    filenames = [
        "01_hello.apy",
        "02_arithmetic.apy",
        "03_control_flow.apy",
        "04_functions.apy",
        "05_data_structures.apy",
        "06_classes.apy",
        "07_imports.apy",
        "helper.apy",
    ]
    for f in filenames:
        assert f in content, f"README.md does not mention {f}"


def test_old_hello_apy_removed():
    repo_root = pathlib.Path(__file__).parents[1]
    old_hello = repo_root / "examples" / "hello.apy"
    assert not old_hello.exists()
