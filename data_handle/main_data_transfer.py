import subprocess

def run_script(script_name):
    try:
        print(f"Running {script_name}...")
        result = subprocess.run(['python3', script_name], check=True, capture_output=True, text=True)
        print(f"Output of {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error while running {script_name}: {e.stderr}")
        raise

if __name__ == "__main__":
    # Define the paths to the scripts
    scripts = [
        'data_handle/datatransfer_gcpbucket.py',
        'data_handle/json_csv_gaia.py',
        'data_handle/datatransfer_gcpsql.py',
        'data_handle/source_text_extract.py',
    ]
    
    # Run the scripts in order
    for script in scripts:
        run_script(script)