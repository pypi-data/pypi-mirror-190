from grader.__main__ import main


def test_template():
    main(
        [
            "tests/fixtures/simpleTasks/template",
            "--tests",
            "tests/fixtures/simpleTasks/tests",
        ]
    )


def test_template_config():
    main(
        [
            "tests/fixtures/simpleTasks/template",
            "--tests",
            "tests/fixtures/simpleTasks/tests",
            "--submission",
            "submission1",
            "--config",
            "tests/fixtures/simpleTasks/tests/config.json",
        ]
    )


def test_solution():
    main(
        [
            "tests/fixtures/simpleTasks/solution",
            "--tests",
            "tests/fixtures/simpleTasks/tests",
        ]
    )


def test_solution_fallback():
    main(
        [
            "tests/fixtures/simpleTasks/solution",
            "--tests",
            "tests/fixtures/simpleTasks/tests",
            "--fallback",
            "tests/fixtures/simpleTasks/template",
        ]
    )
