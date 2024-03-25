import requests
import uuid
import threading
import time
import yaml
import os
from modules.cache import cache
import subprocess
# from . import db


def url_available(url):
    for _ in range(10):
        try:
            response = requests.head(url, allow_redirects=True, timeout=3)
            return True
        except requests.RequestException:
            pass
        time.sleep(1)
    return False


def run_scan(target, severity, output_file, report_uuid):
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        nuclei_path = config.get('nuclei_path', '')

    nuclei_executable = os.path.join(nuclei_path, "nuclei")
    command = [nuclei_executable, "-target", target, "-severity", severity, "-o", output_file]

    try:
        subprocess.run(command, check=True)
        cache.set(report_uuid, 'completed')
        # db.completed(report_uuid)
        return True
    except subprocess.CalledProcessError as e:
        cache.set(report_uuid, f'error : {e}')
        # db.error(report_uuid, e)
        return False


def run_nuclei(target, severity):

    if not url_available(target):
        return False

    report_uuid = str(uuid.uuid4())
    output_file = f"reports/{report_uuid}.json"

    if not os.path.exists(output_file):
        open(output_file, 'w').close()

    thread_scan = threading.Thread(target=run_scan, args=(target, severity, output_file, report_uuid))

    thread_scan.start()
    cache.set(report_uuid, 'started')
    # db.started(report_uuid)
    time.sleep(3)

    return {"status": True,
            "message": "Scan started! Check report file later",
            "report_file": f"/api/scan/reports?report_uuid={report_uuid}"}
