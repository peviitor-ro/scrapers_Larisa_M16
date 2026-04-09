#
#
#
#
#
#
import os
import subprocess
import sys

# exclude files
exclude = ['__init__.py',
           '__create_scraper.py',
           "__main_RunnerFile.py",
           '000.py'
           

           ]

path = os.path.dirname(os.path.abspath(__file__))
timeout_seconds = int(os.getenv('SCRAPER_TIMEOUT_SECONDS', '600'))

for site in os.listdir(path):
    if site.endswith('.py') and site not in exclude:
        try:
            action = subprocess.run(
                [sys.executable, os.path.join(path, site)],
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired as error:
            print(f"Timeout scraping {site} after {timeout_seconds} seconds")
            if error.stderr:
                print(error.stderr)
            continue

        if action.returncode != 0:
            print("Error in " + site)
            print(action.stderr)
        else:
            print("Success scraping " + site)
