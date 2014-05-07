import unittest
import codecs
import os
import shutil


from PackageBoilerplate import package_boilerplate

def file_count(path):
    return len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])

# Remember: 
#   Install AAAPT package to run the tests
#   Save package_boilerplate to reload the tests

class Test_PackageSkeleton(unittest.TestCase):
    def setUp(self):
        self.directory_path = "tests"
        self.package_name = "SuperPackage"
        self.full_path = os.path.join(self.directory_path, self.package_name)
        self.skeleton_folder_path = os.path.join(self.directory_path, "skeleton")
        self.package_skeleton = package_boilerplate.PackageSkeleton(self.skeleton_folder_path)

    def test_creates_the_package_folder_in_the_desired_destination_with_the_files(self):
        self.assertFalse(os.path.exists(self.full_path))

        self.package_skeleton.compose(self.package_name, self.directory_path)
        
        self.assertTrue(os.path.exists(self.full_path))
        self.assertEqual(file_count(self.skeleton_folder_path), file_count(self.full_path))

    def test_replaces_the_package_name_on_each_file_name_found_on_the_skeleton_folder(self):
        self.package_skeleton.compose(self.package_name, self.directory_path)
        self.assertEqual(sorted(['super_package_command.py', 'Default (OSX).sublime-keymap', 'Default (Linux).sublime-keymap', 'SuperPackage.sublime-settings']), sorted(os.listdir(self.full_path)))

    def test_replace_content_replaces_every_appearance_of_project_name_in_the_file(self):
        result = self.package_skeleton.replace_contents("tests/fixture.txt", self.package_name)
        with codecs.open("tests/result.txt", 'r', "utf-8") as result_file:
            self.assertEqual(result_file.read(), result)

    def tearDown(self):
        if os.path.exists(self.full_path):
            shutil.rmtree(self.full_path)