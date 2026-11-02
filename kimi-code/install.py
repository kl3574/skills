#!/usr/bin/env python3

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PATCH_FILE = REPO_ROOT / "kimi-code" / "kimi-code.patch"
ADAPTERS = REPO_ROOT / "kimi-code" / "adapters"
PLUGIN_MANIFEST = REPO_ROOT / ".claude-plugin" / "plugin.json"
BASELINE_SKILL_COUNT = 27


def run_git(arguments, cwd):
    result = subprocess.run(
        ["git", *arguments],
        cwd=cwd,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr).strip())
    return result.stdout


def promoted_skills():
    manifest = json.loads(PLUGIN_MANIFEST.read_text())
    skills = []
    names = set()
    for entry in manifest["skills"]:
        source = (REPO_ROOT / entry).resolve()
        if REPO_ROOT not in source.parents or not (source / "SKILL.md").is_file():
            raise RuntimeError(f"Invalid promoted skill path: {entry}")
        if source.name in names:
            raise RuntimeError(f"Duplicate flat skill name: {source.name}")
        names.add(source.name)
        skills.append(source)
    return skills


def validate_adapter_links(root, marker):
    references = 0
    for document in root.rglob("*.md"):
        text = document.read_text()
        for link in re.findall(r"\]\(([^)]+)\)", text):
            if marker not in link:
                continue
            target = (document.parent / link.split("#", 1)[0]).resolve()
            if not target.is_file():
                raise RuntimeError(f"Broken adapter link in {document}: {link}")
            references += 1
    if references == 0:
        raise RuntimeError(f"No adapter links found under {root}")
    return references


def prepare_flattened(workspace, skills):
    patched = workspace / "patched"
    for source in skills:
        destination = patched / source.relative_to(REPO_ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, destination)
    (patched / "kimi-code").mkdir(parents=True)
    shutil.copytree(ADAPTERS, patched / "kimi-code" / "adapters")

    run_git(["apply", "--check", "--whitespace=error-all", str(PATCH_FILE)], patched)
    changed_files = len(run_git(["apply", "--numstat", str(PATCH_FILE)], patched).splitlines())
    run_git(["apply", str(PATCH_FILE)], patched)
    source_links = validate_adapter_links(patched / "skills", "../../../kimi-code/adapters/")

    flat = workspace / "flat"
    flat.mkdir()
    for source in skills:
        shutil.copytree(patched / source.relative_to(REPO_ROOT), flat / source.name)
    shutil.copytree(ADAPTERS, flat / "_kimi-code")

    replacements = 0
    for document in flat.glob("*/**/*.md"):
        text = document.read_text()
        updated = text.replace("../../../kimi-code/adapters/", "../_kimi-code/")
        replacements += text.count("../../../kimi-code/adapters/")
        if updated != text:
            document.write_text(updated)
    if replacements != source_links:
        raise RuntimeError("Adapter link rewrite count does not match source links")
    flat_links = validate_adapter_links(flat, "../_kimi-code/")
    if flat_links != source_links:
        raise RuntimeError("Flattened adapter link count does not match source links")
    return flat, changed_files, source_links


def install(flat, skills, destination, force):
    destination = destination.expanduser().resolve()
    if destination == REPO_ROOT or REPO_ROOT in destination.parents:
        raise RuntimeError("Choose a destination outside this repository")
    if destination.exists() and not destination.is_dir():
        raise RuntimeError(f"Destination is not a directory: {destination}")
    destination.mkdir(parents=True, exist_ok=True)

    names = [source.name for source in skills] + ["_kimi-code"]
    existing = [name for name in names if (destination / name).exists() or (destination / name).is_symlink()]
    if existing and not force:
        raise RuntimeError(
            "Managed destinations already exist; use --force to back them up before replacement: "
            + ", ".join(existing)
        )

    backup = None
    moved = []
    installed = []
    try:
        if existing:
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            backup = destination / f".kimi-code-backup-{stamp}"
            backup.mkdir()
            for name in existing:
                shutil.move(str(destination / name), str(backup / name))
                moved.append(name)
        for name in names:
            shutil.copytree(flat / name, destination / name)
            installed.append(name)
    except Exception:
        for name in reversed(installed):
            target = destination / name
            if target.is_dir() and not target.is_symlink():
                shutil.rmtree(target)
            elif target.exists() or target.is_symlink():
                target.unlink()
        for name in reversed(moved):
            shutil.move(str(backup / name), str(destination / name))
        if backup is not None and not any(backup.iterdir()):
            backup.rmdir()
        raise
    return destination, backup


def main():
    parser = argparse.ArgumentParser(description="Validate and install the Kimi Code adaptation overlay")
    parser.add_argument("--check", action="store_true", help="validate the patch and flattened links without installing")
    parser.add_argument("--dest", type=Path, help="flat Kimi skill directory, such as ~/.agents/skills")
    parser.add_argument("--force", action="store_true", help="back up and replace existing managed skill directories")
    args = parser.parse_args()
    if args.check and (args.dest or args.force):
        parser.error("--check cannot be combined with --dest or --force")
    if not args.check and not args.dest:
        parser.error("provide --dest, or use --check for validation only")
    if args.force and not args.dest:
        parser.error("--force requires --dest")

    try:
        skills = promoted_skills()
        with tempfile.TemporaryDirectory(prefix="kimi-code-overlay-") as temporary:
            flat, changed_files, links = prepare_flattened(Path(temporary), skills)
            print(
                f"Validated {len(skills)} promoted skills, {changed_files} patched files, "
                f"{links} adapter links, and 3 adapter documents"
            )
            if len(skills) != BASELINE_SKILL_COUNT:
                print(
                    f"Promoted skill count changed from {BASELINE_SKILL_COUNT} to {len(skills)}; "
                    "review CAPABILITY-MAP.md before installing"
                )
            if args.check:
                return
            destination, backup = install(flat, skills, args.dest, args.force)
        print(f"Installed {len(skills)} promoted skills and Kimi adapters to {destination}")
        if backup is not None:
            print(f"Previous managed directories preserved in {backup}")
    except (OSError, RuntimeError, json.JSONDecodeError) as error:
        parser.exit(1, f"error: {error}\n")


if __name__ == "__main__":
    main()
