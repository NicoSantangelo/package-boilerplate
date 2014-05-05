try:
    from AAAPT.runner import register_tests
    register_tests({
        "boilerplate": ["PackageBoilerplate.tests.test_boilerplate"]
    })
except ImportError:
    print("Install the AAAPT Package if you want to test PackageBoilerplate")
    