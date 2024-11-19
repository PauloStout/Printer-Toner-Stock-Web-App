import sys
import os
from flask import Flask

# Check if running in a PyInstaller bundled executable
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    app = Flask(
        __name__,
        template_folder=os.path.join(base_path, 'templates'),  # Templates folder
        static_folder=os.path.join(base_path, 'static')       # Static folder
    )
else:
    app = Flask(__name__)  # Standard behavior during development

