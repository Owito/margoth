import os
import sys


class PathResolver:
    @staticmethod
    def get_resource_path(relative_path):
        base_path = getattr(sys, "_MEIPASS", None)
        if base_path:
            return os.path.join(base_path, relative_path)

        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        return os.path.join(project_root, relative_path)

    @staticmethod
    def get_app_data_path():
        if getattr(sys, "frozen", False):
            return os.path.dirname(sys.executable)

        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        return project_root
