import subprocess
import unittest
import os
from pathlib import Path
import pytest
import json

# Set the path to the tosca file
here = os.path.dirname(os.path.abspath(__file__))
# To save re-typing the tosca file name into every test file,
# guess that the tosca file has the same root as the name of this test file
# and that the extension is .yaml
tosca_file_path = here + '/' + Path(__file__).stem.split("_test")[0] + ".yaml"
# If not the case, then uncomment the following line and give the correct name of the tosca file
# tosca_file_path = here + '/version.yaml'

# Set the path to the wrapper
wrapper_path = here + '/../../../../tools/wrappers/wrapper.py'

class TestFrameworkWithStubTool(unittest.TestCase):

    def test_valid_tosca(self):
        tosca_file_path = here + '/valid.yaml'
        command = (f'python3 {wrapper_path} {tosca_file_path}')
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        self.assertEqual(result.returncode, 0, 
                         f"Expected return code 0, but got {result.returncode} with message\n {result.stdout}")

    def test_invalid_tosca(self):
        tosca_file_path = here + '/not_valid.yaml'
        command = (f'python3 {wrapper_path} {tosca_file_path}')
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        self.assertEqual(result.returncode, 3, 
                         f"Expected return code 3, but got {result.returncode} with message\n {result.stdout}")

    def test_unreadable_file(self):
        tosca_file_path = here + '/unreadable.yaml' ## This file does not exist
        command = (f'python3 {wrapper_path} {tosca_file_path}')
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        self.assertEqual(result.returncode, 102, 
                         f"Expected return code 102, but got {result.returncode} with message\n {result.stdout}")

    def test_cant_action_tosca(self):
        tosca_file_path = here + '/cant_action.yaml'
        command = (f'python3 {wrapper_path} {tosca_file_path}')
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        self.assertEqual(result.returncode, 2, 
                         f"Expected return code 2, but got {result.returncode} with message\n {result.stdout}")

    def test_read_json(self):
        json_file_path = here + '/json_reply.json'
        with open(json_file_path, mode="r", encoding="utf-8") as read_file:
            frie_data = json.load(read_file)
        print(frie_data)
        self.assertEqual(frie_data["wrapper"]["name"], "Friedax")
        

if __name__ == '__main__':
    unittest.main()