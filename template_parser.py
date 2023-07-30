import yaml
import re

class TemplateParser:
    def __init__(self, template_file_path):
        self.template_file_path = template_file_path
        self.id = None
        self.data = None
        self.matcher_regex = None
        self.extractor_regex = None
        self.match = None

        # Load the yaml data to the parser initially.
        self.load_data()


    def validate_template(self):
        """Validate the template.yaml"""
        pass

    def load_data(self):
        """Loads the yaml data to parser object."""
        try:
            with open(self.template_file_path, 'r', encoding='utf-8') as file:
                self.data = yaml.safe_load(file)
                self.id = self.data.get('id')
                self.matcher_regex = self.data.get('parser', {})["matcher"][0]["regex"][0]
                self.extractor_regex = self.data.get('parser', {})["extractor"][0]["regex"][0]
    
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
        except yaml.YAMLError as e:
            print(f"Error: Failed to parse YAML file '{self.file_path}': {e}")

    
    def matcher(self, regex, content):
        """Return true if the given regex matches with the content."""

        match = re.search(regex, content)
        if match:
            self.match = match.group()  # Store the matched text
            return True
        else:
            self.match = None  # Reset the match variable if no match is found
            return False

    def extractor(self, regex, content):
        """Extracts data according to the regex in the target text"""
        extracted_data = []

        matches = re.findall(regex, content)
        if matches:
            extracted_data = [match[0] for match in matches]

        return extracted_data