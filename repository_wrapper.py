import utils
from dotenv import load_dotenv

initialized = False
backend_api = None


def init():
    global initialized, backend_api
    utils.logDebugMessage("Initializing repository wrapper...")
    initialized, backend_api = import_backend_module()


def import_backend_module():
    try:
        print(load_dotenv(".env"))
        
        from frontend.utils import (
            api as backend_api,  # Change this line with your backend module
        )
        utils.logDebugMessage(f"Successfully imported backend module", utils.MessageTypes.SUCCESS)

        return True, backend_api
    
    except ImportError as e:
        utils.logDebugMessage(f"Could not import backend module: {e}", utils.MessageTypes.WARNING)
        return False, None
    

def verify_jobs(jobs):
    if initialized:
        try:
            utils.logDebugMessage(f"Verifying jobs: {jobs}")
            jobs = backend_api.verify_jobs(jobs)
        except Exception as e:
            utils.logDebugMessage(f"Error verifying jobs: {e}", utils.MessageTypes.ERROR)

    return jobs
    

def update_job(job):
    if initialized:
        try:
            utils.logDebugMessage(f"Updating job: {job}")
            job = backend_api.update_job_with_job_properties(job)
        except Exception as e:
            utils.logDebugMessage(f"Error updating job: {e}", utils.MessageTypes.ERROR)

    return job

def get_answer_by_question(question):
    if initialized:
        try:
            utils.logDebugMessage(f"Getting answer for question: {question}")
            # TODO: Implement this
        except Exception as e:
            utils.logDebugMessage(f"Error getting answer for question: {e}", utils.MessageTypes.ERROR)


def post_question(question):
    if initialized:
        try:
            utils.logDebugMessage(f"Posting question: {question} with answer:")
            # TODO: Implement this
        except Exception as e:
            utils.logDebugMessage(f"Error posting question: {e}", utils.MessageTypes.ERROR)


def applied_to_job(job):
    if initialized:
        try:
            utils.logDebugMessage(f"Marking job as applied: {job}")
            backend_api.applied_to_job(job)
        except Exception as e:
            utils.logDebugMessage(f"Error marking job as applied: {e}", utils.MessageTypes.ERROR)
