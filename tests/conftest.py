from pathlib import Path

import pytest

from diagram_differ import DiagramDiffer


@pytest.fixture(scope='session')
def session_diagram_differ():
    """ Track all images compared in a session. """
    diffs_path = Path(__file__).parent / 'image_diffs'
    differ = DiagramDiffer(diffs_path)
    yield differ
    differ.remove_common_prefix()


@pytest.fixture
def diagram_differ(request, session_diagram_differ):
    """ Pass the current request to the session image differ. """
    session_diagram_differ.request = request
    yield session_diagram_differ
