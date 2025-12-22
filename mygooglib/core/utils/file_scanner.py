import os

class FileScanner:
    """
    Utility to scan a directory and extract metadata for files.
    """
    def scan(self, directory_path: str) -> list[dict]:
        """
        Scans a directory (non-recursive) and returns metadata for all files.
        
        Args:
            directory_path: Absolute path to the directory.
            
        Returns:
            List of dictionaries containing 'filename', 'absolute_path', and 'last_modified_timestamp'.
            
        Raises:
            FileNotFoundError: If the directory does not exist.
        """
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"The directory {directory_path} does not exist.")
            
        results = []
        for entry in os.scandir(directory_path):
            if entry.is_file():
                stats = entry.stat()
                results.append({
                    'filename': entry.name,
                    'absolute_path': entry.path,
                    'last_modified_timestamp': stats.st_mtime
                })
        return results

