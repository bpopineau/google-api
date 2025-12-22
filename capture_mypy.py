import subprocess
import sys

result = subprocess.run(
    ["uv", "run", "mypy", "."], capture_output=True, text=True, cwd=sys.argv[1]
)
output = result.stdout + result.stderr

with open("mypy_full_errors.txt", "w", encoding="utf-8") as f:
    f.write(output)

print("Errors captured to mypy_full_errors.txt")
