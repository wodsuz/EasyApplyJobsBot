import config
import utils

initialized = False
backend_api = None


def init():
    global initialized, backend_api
    try:
        utils.logDebugMessage("Initializing repository wrapper...")
        initialized, backend_api = import_backend_module()
    except Exception as e:
        utils.logDebugMessage(f"Error initializing repository wrapper: {e}", utils.MessageTypes.ERROR)


def import_backend_module():
    try:
        from ..frontend.utils import api as backend_api  # Change this line with your backend module
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
    

def get_answer_by_question(question):
    if initialized:
        try:
            utils.logDebugMessage(f"Getting answer for question: {question}")
            # TODO: Implement this
        except Exception as e:
            utils.logDebugMessage(f"Error getting answer for question: {e}", utils.MessageTypes.ERROR)


def post_question(question):
    if initialized:
        utils.logDebugMessage(f"Posting question: {question} with answer:")
        # TODO: Implement this