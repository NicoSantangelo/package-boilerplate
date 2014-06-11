try:
    from AAAPT.runner import register_tests
    register_tests({
        "command": ["{package_name}.tests.test_command"]
    })
except ImportError:
    print("Install the AAAPT Package if you want to test {PackageName}")
    