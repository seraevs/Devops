import jenkins
import requests
from datetime import datetime, time
from flask import Flask
import os
import sys
from flask_sock import Sock
import configparser
import json
import re
import time

## The array for exlclude jobs from jenkins
jobs_array = ['Leo_VM_Autotest']
## excluded jenkins jobs
#'Leo_VM_Autotest'
#'UnifiedIPL'
#'Leo': 'Leo'
#'Skin_Diagnostic'
#'Stellar_Unified'
#'StellarIPL'
#'Unified'
#'Hair_Growth'


# Read config file
config = configparser.ConfigParser()
config.read('config.ini')
jenkins_url = config['default']['jenkins_url']
jenkins_url_schema = config['default']['jenkins_url_schema']
jenkins_username = config['default']['jenkins_username']
jenkins_password = config['default']['jenkins_password']
workspace_directory = config['default']['workspace_directory_win']
#if sys.platform == "win32":
#    workspace_directory = config['default']['workspace_directory_win']
#elif sys.platform == "darwin" or sys.platform == "linux":
#    workspace_directory = config['default']['workspace_directory_unix']

sonarqube_url = config['default']['sonarqube_url']
sonar_projects_analyze = json.loads(config['default']['sonar_projects_analyze'])
jenkins_full_url = "{}{}:{}@{}".format(jenkins_url_schema, jenkins_username, jenkins_password, jenkins_url)
# archive_directory = os.path.join(workspace_directory, "archive", "Leo")
version_file_path = os.path.join("scripts", "VersionControl", "VersionControl.txt")

version = "0.0.0.0"
app = Flask(__name__)
sock = Sock(app)


@sock.route("/jenkins")
def get_jenkins_jobs_status(web_socket, version_=version):
    while True:
        path_to_version = ""
        # Connect Jenkins
        jnk = jenkins.Jenkins(jenkins_url_schema + jenkins_url, jenkins_username, jenkins_password)
        # Get all available jobs
        jobs = jnk.get_all_jobs(folder_depth=None)
        build_description = {'data': []}
        # Iterate over all found jobs to get build details and generate json array with the results
        for job in jobs:
            # get to excluded jobs from array
            if (job['name']) not in jobs_array:
                path_to_version = os.path.join(workspace_directory, job['fullname'] + 'Prj', 'version.txt')
                if path_to_version != "" and os.path.isfile(path_to_version):
                    with open(path_to_version, 'r') as f:
                        version_ = re.sub('\s+', '', f.read())
                info = jnk.get_job_info(job['fullname'])
                if info['lastBuild'] is None:
                    continue
                build_number = info['lastBuild']['number']
                # Get job's last build details
                job_details = requests.request('GET', jenkins_full_url + '/job/' + job['fullname'] + '/' + str(
                    build_number) + '/wfapi').json()
                midnight_time = time.mktime(
                    datetime.strptime(datetime.fromtimestamp(job_details['startTimeMillis'] / 1000).strftime('%d/%m/%Y'),
                                      "%d/%m/%Y").timetuple())
                threshold_time = midnight_time + 21600
                if job_details['startTimeMillis'] / 1000 > midnight_time and job_details[
                    'startTimeMillis'] / 1000 < threshold_time:
                    build_type = "Nightly"
                else:
                    build_type = "Daily"
                duration = round(job_details['durationMillis'] / 1000)
                end_date = datetime.fromtimestamp(job_details['endTimeMillis'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
                # TBD: If job status is not running, then skip it and do not add it to the final results
                # if "IN_PROGRESS" not in job_details["status"]:
                #    continue
                start_date = datetime.fromtimestamp(job_details['startTimeMillis'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
                duration = round(job_details['durationMillis'] / 1000)
                end_date = datetime.fromtimestamp(job_details['endTimeMillis'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
                # Generate job details for the final array
                job_stages = get_jenkins_stages(job['fullname'])
                if job_stages == 0:
                    continue
                job_array = {
                    job['fullname']: {
                        'build_number': build_number,
                        'build_type': build_type,
                        'url': jenkins_full_url + '/job/' + job['fullname'] + '/' + str(build_number),
                        'job_stages_count': len(job_stages['stage_names']),
                        'job_stages_names': job_stages['stage_names'],
                        'status': job_details["status"],
                        'startTime': start_date,
                        'duration': duration,
                        'end_date': end_date,
                        'version': version_,
                        'stages': []
                    }
                }

                # Get details of the job's stages
                for stage in job_details["stages"]:
                    start_date = datetime.fromtimestamp(stage['startTimeMillis'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    duration = round(stage['durationMillis'] / 1000)
                    stage_id = int(stage['id']) + 1
                    stage_array = {
                        'stage_name': stage['name'],
                        'status': stage['status'],
                        'startTime': str(start_date),
                        'duration': duration,
                        'logUrl': jenkins_full_url + '/job/' + job['fullname'] + '/' + str(
                            build_number) + '/execution/node/' + str(stage_id) + '/log/'
                    }
                    job_array[job['fullname']]['stages'].append(stage_array)
                # Generate a final array of Jenkins job status
                build_description['data'].append(job_array)
        web_socket.send(json.dumps(build_description))


@sock.route("/get_jenkins_jobs")
def get_jenkins_jobs(jenkins_jobs):
    while True:
        # Connect Jenkins
        jnk = jenkins.Jenkins(jenkins_url_schema + jenkins_url, jenkins_username, jenkins_password)
        # Get all available jobs
        jobs = jnk.get_all_jobs(folder_depth=None)
        # Iterate over all found jobs to get build details and generate json array with the results
        jobs_array = {'data': []}
        for job in jobs:
            jobs_array['data'].append(job['fullname'])
        jenkins_jobs.send(json.dumps(jobs_array))

def get_jenkins_stages(jobname):
    jnk = jenkins.Jenkins(jenkins_url_schema + jenkins_url, jenkins_username, jenkins_password)
    jobinfo = jnk.get_job_info(jobname)
    stages_array = {'stage_names': []}
    if jobinfo['lastSuccessfulBuild'] is None:
        return 0
    build_number = jobinfo['lastSuccessfulBuild']['number']
    job_details = requests.request('GET',
                                   jenkins_full_url + '/job/' + jobname + '/' + str(build_number) + '/wfapi').json()
    for stage in job_details["stages"]:
        stages_array['stage_names'].append(stage['name'])
    return stages_array


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)