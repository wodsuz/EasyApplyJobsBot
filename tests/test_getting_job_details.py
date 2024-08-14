import unittest

from linkedin import Linkedin as JobProcessor
from models import Job, JobForVerification


class test_getting_job_details_from_linkedin_job_post(unittest.TestCase):

    jobs_from_search_page = []
    
    @classmethod
    def setUpClass(cls):
        # This will be executed once for the test class
        cls.processor = JobProcessor()

        # Get the jobs from the search page
        cls.jobs_from_search_page = cls.find_jobs_from_search_page()

    
    @classmethod
    def find_jobs_from_search_page(cls) -> list[JobForVerification]:
        # Open the Linkedin general job search page
        cls.processor.goToJobsSearchPage()

        # Get the jobs from the search page
        jobs = cls.processor.getJobsFromSearchPage()
        return jobs


    def setUp(self):
        # This will be executed before each test method
        pass


    def find_job_with_title(self) -> JobForVerification:    
        # Find the first job that contains non-empty job title
        job_with_title = next(job for job in self.jobs_from_search_page if job.title)
        return job_with_title
    

    def test_getting_job_title_from_search_page(self):
        # Find the first job that contains non-empty job title
        job_details_from_search_page = self.find_job_with_title()
        job_title_from_search_page = job_details_from_search_page.title

        # Asserting the results
        self.assertTrue(job_title_from_search_page)


    def test_getting_job_title_from_job_post_page(self):
        # Find the first job that contains non-empty job title
        job_details_from_search_page = self.find_job_with_title()
        job_title_from_search_page = job_details_from_search_page.title

        # Open page with a job with a title property
        self.processor.goToJobPage(job_details_from_search_page.linkedinJobId)
        job_details_from_job_page = self.processor.getJobProperties(job_details_from_search_page.linkedinJobId)

        # Getting the job title
        job_title_from_job_page = job_details_from_job_page.title

        # Asserting the results
        self.assertEqual(job_title_from_search_page, job_title_from_job_page)


    def find_job_with_company(self) -> JobForVerification:
        # Find the first job that contains non-empty company name
        job_with_company = next(job for job in self.jobs_from_search_page if job.company)
        return job_with_company


    def test_getting_job_company_from_search_page(self):
        job_details_from_search_page = self.find_job_with_company()
        job_company_from_search_page = job_details_from_search_page.company

        # Asserting the results
        self.assertTrue(job_company_from_search_page)


    def test_getting_job_company_from_job_post_page(self):
        job_details_from_search_page = self.find_job_with_company()
        job_company_from_search_page = job_details_from_search_page.company

        # Open page with a job with a company property
        self.processor.goToJobPage(job_details_from_search_page.linkedinJobId)
        job_details_from_job_page = self.processor.getJobProperties(job_details_from_search_page.linkedinJobId)

        # Getting the job company
        job_company_from_job_page = job_details_from_job_page.company

        # Asserting the results
        self.assertEqual(job_company_from_search_page, job_company_from_job_page)