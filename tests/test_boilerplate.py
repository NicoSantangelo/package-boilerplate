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

    def test_compose_creates_the_package_folder_in_the_desired_destination_with_the_files(self):
        self.assertFalse(os.path.exists(self.full_path))

        self.package_skeleton.compose(self.package_name, self.directory_path)
        
        self.assertTrue(os.path.exists(self.full_path))
        self.assertEqual(file_count(self.skeleton_folder_path), file_count(self.full_path))

    def test_compose_replaces_the_package_name_on_each_file_name_found_on_the_skeleton_folder(self):
        self.package_skeleton.compose(self.package_name, self.directory_path)
        self.assertEqual(sorted(['super_package_command.py', 'Default (OSX).sublime-keymap', 'Default (Linux).sublime-keymap', 'SuperPackage.sublime-settings']), sorted(os.listdir(self.full_path)))

    def test_compose_skips_the_files_passed_on_the_constructor_using_file_pattern_matching(self):
        package_skeleton = package_boilerplate.PackageSkeleton(self.skeleton_folder_path, skip = ['*.sublime-keymap', 'SuperPackage.sublime-settings'])
        package_skeleton.compose(self.package_name, self.directory_path)
        self.assertEqual(sorted(['super_package_command.py']), sorted(os.listdir(self.full_path)))

    def test_compose_replaces_every_appearance_of_project_name_in_the_file(self):
        self.package_skeleton.compose(self.package_name, self.directory_path)
        with codecs.open(os.path.join(self.directory_path, "result.py"), 'r', "utf-8") as expected_file:
            expected_result = expected_file.read()

        with codecs.open(os.path.join(self.full_path, "super_package_command.py"), 'r', "utf-8") as result_file:
            self.assertEqual(expected_result, result_file.read())

    def tearDown(self):
        if os.path.exists(self.full_path):
            shutil.rmtree(self.full_path)