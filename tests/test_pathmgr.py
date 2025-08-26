import pytest
from pathlib import Path
from textwrench import PathMgr


@pytest.fixture
def path_manager(tmp_path: Path) -> PathMgr:
    """Provides a TextFile instance with a temporary directory for each test."""
    return PathMgr(relative_dir=str(tmp_path))


def test_init_creates_directory(tmp_path: Path):
    """Test that the directory is created on initialization."""
    test_dir = tmp_path / "test_data"
    assert not test_dir.exists()
    PathMgr(relative_dir=str(test_dir))
    assert test_dir.exists()
    assert test_dir.is_dir()


def test_write_and_read_lines(path_manager: PathMgr):
    """Test writing and reading lines from a text file."""
    filename = "test.txt"
    lines_to_write = ["Hello\n", "This is a test\n", "Goodbye\n"]

    path_manager.write_lines(filename, lines_to_write)

    assert (path_manager.directory / filename).exists()

    read_lines = path_manager.read_lines(filename)
    assert read_lines == lines_to_write


def test_read_nonexistent_file_raises_error(path_manager: PathMgr):
    """Test that reading a non-existent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        path_manager.read_lines("nonexistent.txt")


def test_file_exists(path_manager: PathMgr):
    """Test the file_exists method."""
    filename = "exists.txt"

    assert not path_manager.file_exists(filename)

    (path_manager.directory / filename).touch()

    assert path_manager.file_exists(filename)


def test_delete_file(path_manager: PathMgr):
    """Test deleting a file."""
    filename = "to_delete.txt"
    (path_manager.directory / filename).touch()
    assert path_manager.file_exists(filename)

    path_manager.delete_file(filename)

    assert not path_manager.file_exists(filename)


def test_delete_nonexistent_file_does_not_raise_error(path_manager: PathMgr):
    """Test that deleting a non-existent file does not raise an error."""
    try:
        path_manager.delete_file("nonexistent_to_delete.txt")
    except Exception as e:
        pytest.fail(f"Deleting a non-existent file raised an exception: {e}")


def test_write_empty_file(path_manager: PathMgr):
    """Test writing an empty list of lines to a file."""
    filename = "empty.txt"
    path_manager.write_lines(filename, [])

    assert path_manager.file_exists(filename)

    lines = path_manager.read_lines(filename)
    assert lines == []
    assert (path_manager.directory / filename).stat().st_size == 0
