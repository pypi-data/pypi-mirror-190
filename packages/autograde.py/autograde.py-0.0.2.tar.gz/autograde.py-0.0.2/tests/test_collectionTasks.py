from grader.__main__ import main


def test_template():
    main(
        [
            "tests/fixtures/collectionTasks/template",
            "--tests",
            "tests/fixtures/collectionTasks/tests/",
        ]
    )


def test_template_config():
    main(
        [
            "tests/fixtures/collectionTasks/template",
            "--tests",
            "tests/fixtures/collectionTasks/tests",
            "--submission",
            "submission1",
            "--config",
            "tests/fixtures/collectionTasks/tests/config.json",
        ]
    )


def test_solution():
    main(
        [
            "tests/fixtures/collectionTasks/solution",
            "--tests",
            "tests/fixtures/collectionTasks/tests",
        ]
    )


def test_solution_fallback():
    main(
        [
            "tests/fixtures/collectionTasks/solution",
            "--tests",
            "tests/fixtures/collectionTasks/tests",
            "--fallback",
            "tests/fixtures/collectionTasks/template",
        ]
    )
