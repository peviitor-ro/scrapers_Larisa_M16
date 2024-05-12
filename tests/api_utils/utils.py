from unidecode import unidecode
import re

class TestUtils:

    # Check if a string has special characters
    def check_special_characters(self, string):
        # Regular expression to match any special characters
        regex = re.compile(r'[@_!$%^&*<>?|}{~:]')

        # Search for special characters in the string
        if regex.search(string) is not None:
            return string
        else:
            return False

    # return the non special characters for a job title
    def return_without_special_characters(self, string):
        # Regular expression to match any non-letter, non-digit, non-exception characters
        regex = re.compile(r'[^a-zA-Z0-9\s#/\\(),.]')

        # Replace special characters with an empty string
        result = re.sub(regex, '', string)

        return result
    
    # Remove diacritics from input recursive
    def remove_diacritics(self, item):
        
        # If instance of list remove diacritics recursive
        if isinstance(item, list):
            return [self.remove_diacritics(subitem) for subitem in item]
        else:
            # Remove diacritics from string
            return unidecode(item)
    
    # Utility function for checking missing items
    def get_missing_items(self, expected_list, actual_list):
        return [item for item in expected_list if item not in actual_list][:20]
    
    # Utility function for checking cities/country
    def get_different_items(self, expected_list, actual_list, job_titles):
        # Check if actual list is empty
        if not actual_list:
            return expected_list, job_titles
        
        dummy_actual_list = actual_list[:]

        for expected_index, expected_item in enumerate(expected_list):

            # Check if actual list is empty otherwise pop
            if not dummy_actual_list:
                return expected_list[expected_index:], job_titles[expected_index:]
            
            dummy_actual_list.pop(0)
        
        return [], []