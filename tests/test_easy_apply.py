from base_test_class import BaseTestCase

from linkedin import Linkedin as JobProcessor
from models import JobForVerification, JobCounter
from typing import List


class test_getting_job_details_from_linkedin_job_post(BaseTestCase):

    easy_apply_jobs_from_search_page: List[JobForVerification] = []

    @classmethod
    def setUpClass(cls):
        # This will be executed once for the test class
        cls.processor = JobProcessor()

        # Get the jobs from the search page
        cls.easy_apply_jobs_from_search_page = cls.find_easy_apply_jobs_from_search_page()


    @classmethod
    def find_easy_apply_jobs_from_search_page(cls) -> list[JobForVerification]:
        # Open the Linkedin general job search page
        cls.processor.goToEasyApplyJobsSearchPage()

        # Get the jobs from the search page
        jobs = cls.processor.getJobsFromSearchPage()
        return jobs


    def setUp(self):
        super().setUp()


    def tearDown(self):
        super().tearDown(self.processor.driver)
    

    def test_clicking_easy_apply_button(self):
        # Go to the first job
        easy_apply_job = self.easy_apply_jobs_from_search_page[0]
        self.processor.goToJobPage(easy_apply_job.linkedinJobId)

        # Verify that Easy Apply button is displayed
        is_easy_apply_button_displayed = self.processor.isEasyApplyButtonDisplayed()
        self.assertTrue(is_easy_apply_button_displayed, "Easy Apply button is not displayed")

        # Click the Easy Apply button
        self.processor.clickEasyApplyButton()

        # Check if the application popup is displayed
        is_application_popup_displayed = self.processor.isApplicationPopupDisplayed()
        self.assertTrue(is_application_popup_displayed, "Application popup is not displayed")


    def test_reaching_final_step_of_application(self):
        # Go to the first job
        easy_apply_job = self.easy_apply_jobs_from_search_page[1]
        self.processor.goToJobPage(easy_apply_job.linkedinJobId)

        # Click the Easy Apply button
        self.processor.clickEasyApplyButton()

        # Check if the application popup is displayed
        is_application_popup_displayed = self.processor.isApplicationPopupDisplayed()
        self.assertTrue(is_application_popup_displayed, "Application popup is not displayed")

        # Click through the application process
        while self.processor.isApplicationStepDisplayed():
            self.processor.clickNextButton()

        # Check if Review button is displayed
        is_last_application_step_displayed = self.processor.isLastApplicationStepDisplayed()
        self.assertTrue(is_last_application_step_displayed, "Last application step is not displayed")

        # Click the Review button
        self.processor.clickReviewApplicationButton()

        # Check if the Submit button is displayed
        is_review_application_step_displayed = self.processor.isReviewApplicationStepDisplayed()
        self.assertTrue(is_review_application_step_displayed, "Review application step is not displayed")

        # Click the Submit button
        self.processor.clickSubmitApplicationButton()

        # Check if the application was submitted
        is_application_submitted_dialog_displayed = self.processor.isApplicationSubmittedDialogDisplayed()
        self.assertTrue(is_application_submitted_dialog_displayed, "Application submitted dialog is not displayed")


    def test_process_job_reaching_final_step_of_application(self):
        # Go to the first job
        easy_apply_job = self.easy_apply_jobs_from_search_page[2]

        # Process the job
        jobCounter = self.processor.processJob(easy_apply_job.linkedinJobId, JobCounter())

        # Check if the application was submitted
        is_application_submitted_dialog_displayed = self.processor.isApplicationSubmittedDialogDisplayed()
        self.assertTrue(is_application_submitted_dialog_displayed, "Application submitted dialog is not displayed")

        # Check if the counter was updated
        self.assertEqual(jobCounter.applied, 1, "Job counter was not updated")

