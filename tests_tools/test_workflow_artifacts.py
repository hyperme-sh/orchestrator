"""Actions artifact uploads must use short retention and skip unconsumed bytes."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / '.github' / 'workflows'
UPLOAD = 'actions/upload-artifact@'
DOWNLOAD = 'actions/download-artifact@'
UNCONSUMED_PACKAGE_NAMES = ('tested-dist', 'prepared-dist')


def workflow_steps(text):
    lines = text.splitlines(keepends=True)
    starts = [index for index, line in enumerate(lines) if line.startswith('      - ')]
    starts.append(len(lines))
    return [''.join(lines[start:end]) for start, end in zip(starts, starts[1:])]


def upload_steps():
    found = []
    for path in sorted(WORKFLOWS.glob('*.yml')):
        for step in workflow_steps(path.read_text()):
            if UPLOAD in step:
                found.append((path.name, step))
    return found


def test_every_upload_artifact_step_sets_finite_retention_days():
    for filename, step in upload_steps():
        retentions = [
            int(line.split(':', 1)[1].strip())
            for line in step.splitlines()
            if line.strip().startswith('retention-days:')
        ]
        assert len(retentions) == 1, (filename, step)
        assert 1 <= retentions[0] <= 90, (filename, retentions[0])


def test_workflows_skip_unconsumed_package_artifact_uploads():
    for path in sorted(WORKFLOWS.glob('*.yml')):
        text = path.read_text()
        assert DOWNLOAD not in text, path.name
    for filename, step in upload_steps():
        for name in UNCONSUMED_PACKAGE_NAMES:
            assert f'\n          name: {name}\n' not in step, (filename, name)


def test_public_distribution_has_no_actions_artifact_graph():
    for path in sorted(WORKFLOWS.glob('*.yml')):
        text = path.read_text()
        assert UPLOAD not in text, path.name
        assert DOWNLOAD not in text, path.name