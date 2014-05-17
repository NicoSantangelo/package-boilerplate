try:
    from AAAPT.runner import register_tests
    register_tests({
        "skeleton": ["PackageBoilerplate.tests.test_skeleton"],
        "support": ["PackageBoilerplate.tests.test_support"],
        "basepath": ["PackageBoilerplate.tests.test_basepath"]
    })
except ImportError:
    print("Install the AAAPT Package if you want to test PackageBoilerplate")
    