import pytest
from mygooglib.core.utils.file_scanner import FileScanner

def test_scan_directory_with_files(tmp_path):
    # Setup: Create temporary files
    file1 = tmp_path / "test1.txt"
    file1.write_text("content1")
    
    file2 = tmp_path / "test2.csv"
    file2.write_text("content2")
    
    # Ensure modified times are captured (wait a bit if necessary, but filesystem usually handles it)
    
    scanner = FileScanner()
    results = scanner.scan(str(tmp_path))
    
    # Sort results by filename to ensure deterministic assertions
    results.sort(key=lambda x: x['filename'])
    
    assert len(results) == 2
    
    assert results[0]['filename'] == "test1.txt"
    assert results[0]['absolute_path'] == str(file1)
    assert isinstance(results[0]['last_modified_timestamp'], float)
    
    assert results[1]['filename'] == "test2.csv"
    assert results[1]['absolute_path'] == str(file2)
    assert isinstance(results[1]['last_modified_timestamp'], float)

def test_scan_empty_directory(tmp_path):
    scanner = FileScanner()
    results = scanner.scan(str(tmp_path))
    assert results == []

def test_scan_non_existent_directory():
    scanner = FileScanner()
    with pytest.raises(FileNotFoundError):
        scanner.scan("non/existent/path")

def test_scan_skips_directories(tmp_path):
    # Create a subdirectory
    sub_dir = tmp_path / "subdir"
    sub_dir.mkdir()
    (sub_dir / "ignored.txt").write_text("ignored")
    
    # Create a file in root
    file1 = tmp_path / "root.txt"
    file1.write_text("root")
    
    scanner = FileScanner()
    results = scanner.scan(str(tmp_path))
    
    assert len(results) == 1
    assert results[0]['filename'] == "root.txt"


