#!/usr/bin/env python3

from dataclasses import dataclass
import argparse
import os

from comby import comby_match, comby_rewrite, comby_rewrite_in_file


@dataclass
class Matcher:
    pattern: str
    replacement: str


@dataclass
class Test:
    file_path: str
    content: str


# https://swiftpackageindex.com/apple/swift-testing/main/documentation/testing/migratingfromxctest
# TODO: Review that comment and #file work the same in #expect
ASSERTION_MATCHERS = [
    Matcher(f"func test:[test_name]()", f"@Test func test:[test_name]()"),
    Matcher(":[~XCTAssertTrue|XCTAssert](:[params])", "#expect(:[params])"),
    Matcher("XCTAssertFalse(:[params])", "#expect(!:[params])"),
    Matcher("XCTAssertEqual(:[first], :[rest])", "#expect(:[first] == :[rest])"),
    Matcher("XCTAssertNotEqual(:[first], :[rest])", "#expect(:[first] != :[rest])"),
    Matcher("XCTAssertNil(:[first], :[rest])", "#expect(:[first] == nil, :[rest])"),
    Matcher("XCTAssertNil(:[single])", "#expect(:[single] == nil)"),
    Matcher("XCTAssertNotNil(:[first], :[rest])", "#expect(:[first] != nil, :[rest])"),
    Matcher("XCTAssertNotNil(:[single])", "#expect(:[single] != nil)"),
    Matcher("XCTAssertIdentical(:[first], :[rest])", "#expect(:[first] === :[rest])"),
    Matcher(
        "XCTAssertNotIdentical(:[first], :[rest])", "#expect(:[first] !== :[rest])"
    ),
    Matcher("XCTAssertGreaterThan(:[first], :[rest])", "#expect(:[first] > :[rest])"),
    Matcher(
        "XCTAssertGreaterThanOrEqual(:[first], :[rest])", "#expect(:[first] >= :[rest])"
    ),
    Matcher(
        "XCTAssertLessThanOrEqual(:[first], :[rest])", "#expect(:[first] =< :[rest])"
    ),
    Matcher("XCTAssertLessThan(:[first], :[rest])", "#expect(:[first] < :[rest])"),
    Matcher("= try XCTUnwrap(:[content])", "try #require(:[content])"),
    Matcher("XCTFail(:[content])", "Issue.record(:[content])"),
    Matcher(
        "XCTExpectFailure(:[description]) { :[content] }",
        "withKnownIssue(:[description]) { :[content] }",
    ),
]


SUITE_LEVEL_MATCHERS = [
    Matcher("class :[class_name]: XCTestCase", "struct :[class_name]"),
    Matcher("import XCTest", "import Testing"),
    Matcher("override func setUp() { :[content] }", "init() { :[content] }"),
    Matcher(
        "override func setUp() async { :[content] }", "init() async { :[content] }"
    ),
    Matcher(
        "override func setUp() throws { :[content] }", "init() throws { :[content] }"
    ),
    Matcher(
        "override func setUp() async throws { :[content] }",
        "init() async throws { :[content] }",
    ),
    Matcher("override func tearDown() { :[content] }", "deinit { :[content] }"),
    Matcher("super.setUp()", ""),
    Matcher("super.tearDown()", ""),
]

# Missing:
# XCTAssertThrowsError(try f()) #expect(throws: (any Error).self) { try f() }
# XCTAssertThrowsError(try f()) { error in … } #expect { try f() } throws: { error in return … }
# XCTAssertNoThrow(try f()) #expect(throws: Never.self) { try f() }

_UNUSPPORTED_ASSERTIONS = {
    "XCTWait",
    "XCTWaiter",
    "XCTExpectation",
    "XCTSkip",
    "XCTAssertThrowsError",
    "XCTAssertNoThrow",
}

_TESTS_DEFINITION_MATCHERS = [
    "func test:[test_suffix]() { :[content] }",
    "func test:[test_suffix]() async { :[content] }",
    "func test:[test_suffix]() throws { :[content] }",
    "func test:[test_suffix]() async throws { :[content] }",
]


def _find_tests(file_path: str) -> list[Test]:
    tests: list[Test] = []
    contents = open(file_path).read()
    if "XCTestCase" in contents:
        for matcher in _TESTS_DEFINITION_MATCHERS:
            matches = comby_match(matcher, ["-f", file_path], [])
            for match in matches:
                tests.append(Test(file_path, match["matched"]))

    return tests


def _test_has_unuspported_types(test: Test) -> bool:
    for unsupported_type in _UNUSPPORTED_ASSERTIONS:
        if unsupported_type in test.content:
            return True
    return False


def _main(args: argparse.Namespace) -> None:
    suite_path: str = args.path
    tests: list[Test] = []
    for file in os.listdir(suite_path):
        if file.endswith(".swift"):
            file_path = os.path.join(suite_path, file)
            tests = _find_tests(file_path)
            if any(_test_has_unuspported_types(test) for test in tests):
                print(f"Skipping {file} due to unsupported assertion types.")

                continue
            migrated_tests = False
            for test in tests:
                original_test_content = test.content
                updated_test_content: str = test.content
                for matcher in ASSERTION_MATCHERS:
                    rewrite_output = comby_rewrite(
                        updated_test_content, matcher.pattern, matcher.replacement, []
                    )
                    if rewrite_output:
                        updated_test_content = rewrite_output

                if updated_test_content != original_test_content:
                    with open(test.file_path, "r+") as file:
                        file_content = file.read()
                        file_content = file_content.replace(
                            original_test_content, updated_test_content
                        )
                        file.seek(0)
                        file.write(file_content)
                        file.truncate()
                        migrated_tests = True

            if migrated_tests:
                for matcher in SUITE_LEVEL_MATCHERS:
                    comby_rewrite_in_file(
                        matcher.pattern, matcher.replacement, ["-f", file_path],
                    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="Path of the suite to be rewritten.")
    return parser


if __name__ == "__main__":
    _main(_build_parser().parse_args())
