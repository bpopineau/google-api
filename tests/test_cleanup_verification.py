import os


def test_streamlit_removed():
    """Verify that the .streamlit directory has been removed."""
    assert not os.path.exists(".streamlit"), ".streamlit directory still exists"


def test_old_cli_removed():
    """Verify that the mygooglib/cli directory has been removed."""
    assert not os.path.exists("mygooglib/cli"), "mygooglib/cli directory still exists"


def test_old_gui_removed():
    """Verify that the mygooglib/gui directory has been removed."""
    assert not os.path.exists("mygooglib/gui"), "mygooglib/gui directory still exists"


def test_temp_md_removed():
    """Verify that test_temp.md has been removed."""
    assert not os.path.exists("test_temp.md"), "test_temp.md file still exists"


def test_pytest_output_removed():
    """Verify that pytest_output.txt has been removed."""
    assert not os.path.exists("pytest_output.txt"), (
        "pytest_output.txt file still exists"
    )
