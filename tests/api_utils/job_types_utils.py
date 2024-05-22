import allure


class TypeTestUtils:
    
    def check_job_format_types(self, job_types_scraper):
        msg = "An unknown error occured"
        expected_job_type_formats = ["hybrid", "remote", "on-site"]
        
        for job_type in job_types_scraper:
            if job_type not in expected_job_type_formats:
                msg = f"One of the job format types is not within the expected job type formats"
                raise AssertionError(msg)
        
        assert job_types_scraper, msg