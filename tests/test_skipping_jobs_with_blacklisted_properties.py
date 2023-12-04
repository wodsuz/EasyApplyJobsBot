import unittest
from linkedin import Linkedin as JobProcessor
from models import Job


class test_skipping_jobs_with_blacklisted_properties(unittest.TestCase):
    def setUp(self):
        # Assuming JobProcessor and Job are classes in our system
        # JobProcessor processes instances of Job
        self.processor = JobProcessor()

    def test_blacklisting_jobs(self):
        # Creating a job with a blacklisted property
        blacklisted_company_job = Job(company='Crossover')
        blacklisted_title_job = Job(title='Web Developer')
        regular_job = Job(company='Google', title='Data Engineer')

        # Checking if the job is blacklisted
        isJobBlacklistedByCompany = self.processor.isJobBlacklisted(blacklisted_company_job)
        isJobBlacklistedByTitle = self.processor.isJobBlacklisted(blacklisted_title_job)
        isJobNotBlacklisted = self.processor.isJobBlacklisted(regular_job)

        # Asserting the results
        self.assertTrue(isJobBlacklistedByCompany)
        self.assertTrue(isJobBlacklistedByTitle)
        self.assertFalse(isJobNotBlacklisted)


if __name__ == '__main__':
    unittest.main()
