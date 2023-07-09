# run_all.py
import os
import subprocess

# Run main pipeline
# subprocess.run(["python", "main.py", "--databases", "biorxiv"])

# Run deployment script
subprocess.run(["python", "deploy_app.py"])

