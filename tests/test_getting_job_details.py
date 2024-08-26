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
    

    def find_job_with_workplace_type(self) -> JobForVerification:
        # Find the first job that contains non-empty workplace type
        job_with_workplace_type = next((job for job in self.jobs_from_search_page if job.workplaceType), None)
        return job_with_workplace_type
    

    def test_getting_job_title_from_search_page(self):
        # Find the first job that contains non-empty job title
        job_details_from_search_page = self.find_job_with_title()
        job_title_from_search_page = job_details_from_search_page.title

        # Asserting the results
        self.assertTrue(job_title_from_search_page, "The job title should not be empty.")


    def test_getting_job_title_from_job_post_page(self):
        # Find the first job that contains non-empty job title
        job_details_from_search_page = self.find_job_with_title()
        job_title_from_search_page = job_details_from_search_page.title

        # Open page with a job with a title property
        self.processor.goToJobPage(job_details_from_search_page.linkedinJobId)
        job_details_from_job_page = self.processor.getJobPropertiesFromJobPage(job_details_from_search_page.linkedinJobId)

        # Getting the job title
        job_title_from_job_page = job_details_from_job_page.title

        # Asserting the results
        self.assertEqual(
            job_title_from_search_page, 
            job_title_from_job_page, 
            f"The job title should be the same on job search page and job post page."
            f"Got {job_title_from_search_page} from search page and {job_title_from_job_page} from job post page."
        )


    def find_job_with_company(self) -> JobForVerification:
        # Find the first job that contains non-empty company name
        job_with_company = next(job for job in self.jobs_from_search_page if job.company)
        return job_with_company


    def test_getting_job_company_from_search_page(self):
        job_details_from_search_page = self.find_job_with_company()
        job_company_from_search_page = job_details_from_search_page.company

        # Asserting the results
        self.assertTrue(job_company_from_search_page, "The company name should not be empty.")


    def test_getting_job_company_from_job_post_page(self):
        job_details_from_search_page = self.find_job_with_company()
        job_company_from_search_page = job_details_from_search_page.company

        # Open page with a job with a company property
        self.processor.goToJobPage(job_details_from_search_page.linkedinJobId)
        job_details_from_job_page = self.processor.getJobPropertiesFromJobPage(job_details_from_search_page.linkedinJobId)

        # Getting the job company
        job_company_from_job_page = job_details_from_job_page.company

        # Asserting the results
        self.assertEqual(
            job_company_from_search_page, 
            job_company_from_job_page, 
            f"The company name should be the same on job search page and job post page." 
            f"Got {job_company_from_search_page} from search page and {job_company_from_job_page} from job post page."
        )

    
    def test_getting_job_location_from_job_post_page(self):
        # Find the first job that contains non-empty title
        job_details_from_search_page = self.find_job_with_title()

        # Open page with a job with a title property
        self.processor.goToJobPage(job_details_from_search_page.linkedinJobId)
        job_details_from_job_page = self.processor.getJobPropertiesFromJobPage(job_details_from_search_page.linkedinJobId)

        # Getting the job location
        job_location_from_job_page = job_details_from_job_page.location

        # Asserting the results
        self.assertTrue(job_location_from_job_page, "The job location should not be empty.")


    def test_getting_job_posted_date_from_job_post_page(self):
        # Find the first job that contains non-empty title
        job_details_from_search_page = self.find_job_with_title()

        # Open page with a job with a title property
        self.processor.goToJobPage(job_details_from_search_page.linkedinJobId)
        job_details_from_job_page = self.processor.getJobPropertiesFromJobPage(job_details_from_search_page.linkedinJobId)

        # Getting the job posted date
        job_posted_date_from_job_page = job_details_from_job_page.posted_date

        # Asserting that the date is not empty
        self.assertTrue(job_posted_date_from_job_page, "The posted date should not be empty.")

        # Assert that the string contains a number
        self.assertTrue(
            any(char.isdigit() for char in job_posted_date_from_job_page), 
            f"The posted date string should contain a digit."
            f"Got: {job_posted_date_from_job_page}"
        )

        # Assert that the string contains 'ago'
        self.assertTrue(
            "ago" in job_posted_date_from_job_page.lower(), 
            f"The posted date string should contain 'ago'."
            f"Got: {job_posted_date_from_job_page}"
        )


    def test_getting_number_of_applicants_from_job_post_page(self):
        # Find the first job that contains non-empty title
        job_details_from_search_page = self.find_job_with_title()

        # Open page with a job with a title property
        self.processor.goToJobPage(job_details_from_search_page.linkedinJobId)
        job_details_from_job_page = self.processor.getJobPropertiesFromJobPage(job_details_from_search_page.linkedinJobId)

        # Getting the job number of applicants
        number_of_applicants_from_job_page = job_details_from_job_page.applicants_at_time_of_applying

        # Assert that there is some value
        self.assertTrue(number_of_applicants_from_job_page, "The number of applicants should not be empty.")

        # Assert that the string contains a number
        self.assertTrue(
            any(char.isdigit() for char in number_of_applicants_from_job_page), 
            f"The number of applicants string should contain a digit."
            f"Got: {number_of_applicants_from_job_page}"
        )

        # Assert that the string contains 'applicant' or 'people'
        self.assertTrue(
            "applicant" in number_of_applicants_from_job_page.lower() or "people" in number_of_applicants_from_job_page.lower(), 
            f"The number of applicants string should contain 'applicant' or 'people'."
            f"Got: {number_of_applicants_from_job_page}"
        )


    def test_getting_number_of_applicants_from_job_post_page_when_workplace_type_is_empty(self):
        # TODO: Implement this test
        pass
    

    def test_getting_job_workplace_type_from_search_page(self):
        # Find the first job that contains non-empty workplace type
        job_details_from_search_page = self.find_job_with_workplace_type()

        # Assert that the job details are not empty
        self.assertTrue(job_details_from_search_page, "The job details should not be empty, there should be at least one job with workplace type.")

        # Getting the job workplace type
        job_workplace_type_from_search_page = job_details_from_search_page.workplaceType

        # Assert that the string is not empty
        self.assertTrue(job_workplace_type_from_search_page, "The workplace type should not be empty.")

        # Assert that the string contains a word 'remote', 'on-site' or 'hybrid' 
        self.assertTrue(
            job_workplace_type_from_search_page.lower() in ["remote", "on-site", "hybrid"], 
            f"The workplace type should be 'remote', 'on-site' or 'hybrid'."
            f"Got: {job_workplace_type_from_search_page}"
        )


    def test_getting_empty_job_workplace_type_from_search_page(self):
        # TODO: Implement this test
        pass


    def test_getting_job_workplace_type_from_job_post_page(self):
        # Find the first job that contains non-empty title
        job_details_from_search_page = self.find_job_with_workplace_type()
        job_workplace_type_from_search_page = job_details_from_search_page.workplaceType

        # Open page with a job with a title property
        self.processor.goToJobPage(job_details_from_search_page.linkedinJobId)
        job_details_from_job_page = self.processor.getJobPropertiesFromJobPage(job_details_from_search_page.linkedinJobId)

        # Getting the job workplace type
        job_workplace_type_from_job_page = job_details_from_job_page.workplace_type

        # Assert that the string is not empty
        self.assertTrue(job_workplace_type_from_job_page, "The workplace type should not be empty.")

        # Assert that the string contains a word 'remote', 'on-site' or 'hybrid' 
        self.assertTrue(
            job_workplace_type_from_job_page.lower() in ["remote", "on-site", "hybrid"], 
            f"The workplace type should be 'remote', 'on-site' or 'hybrid'."
            f"Got: {job_workplace_type_from_job_page}"
        )

        # Assert that the workplace type is the same on job search page and job post page
        self.assertEqual(
            job_workplace_type_from_search_page, 
            job_workplace_type_from_job_page, 
            f"The workplace type should be the same on job search page and job post page."
            f"Got {job_workplace_type_from_search_page} from search page and {job_workplace_type_from_job_page} from job post page."
        )


    def test_getting_empty_job_workplace_type_from_job_post_page(self):
        # TODO: Implement this test
        pass

    
    def test_getting_job_description_from_job_post_page(self):
        # TODO: Implement this test
        pass
