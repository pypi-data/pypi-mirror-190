import os
import shutil
import subprocess
import sys
from typing import List, Optional


class ClangFormater:
    def __init__(self, name) -> None:
        self.name = name

    def format_c_cpp_files(self) -> None:
        if not self._check_clang_format_tool():
            print(f"Clang format tool {self.name} not found")
            sys.exit(1)
        code_directory = self._find_code_directory()
        if code_directory is None:
            print("Code directory not found")
            sys.exit(1)
        c_cpp_files = self._search_c_cpp_files(target_directory=code_directory)
        if len(c_cpp_files) == 0:
            print("No C/C++ files found")
            sys.exit(1)
        for file in c_cpp_files:
            self._format_files(file)

    def _check_clang_format_tool(self) -> bool:
        """Check if clang-format tool is installed on the system and available in the PATH"""
        check = shutil.which(self.name)
        if check is None:
            return False
        return True

    def _find_code_directory(self) -> Optional[str]:
        """Find the code directory in the project root"""
        target_folder = "code"
        for root, dirs, *_ in os.walk(os.getcwd()):
            for dir in dirs:
                if dir == target_folder:
                    return os.path.join(root, dir)
        return None

    def _search_c_cpp_files(self, target_directory) -> List[str]:
        """Search all C/C++ files in the code directory and subdirectories
        return a list of C/C++ files paths"""
        file_extensions = [".h", ".cpp"]
        c_cpp_files = []
        for root, dirs, files in os.walk(target_directory):
            for file in files:
                if any(file.endswith(ext) for ext in file_extensions):
                    c_cpp_files.append(os.path.join(root, file))
        return c_cpp_files

    def _format_files(self, file: str) -> None:
        """Format the C/C++ files"""
        subprocess.run([self.name, "-i", file])
