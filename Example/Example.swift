import XCTest

final class AssertionTests: XCTestCase {
    let value: Type!
    override func setUp() {
        super.setUp()
        configureTests()
    }

    override func tearDown() {
        super.tearDown()
        cleanupTests()
    }

    func testAssertions() {
        // XCTAssert
        XCTAssert(2 + 2 == 4, "2 plus 2 should equal 4")
        XCTAssert(2 + 2 == 4)
        // XCTAssertTrue
        XCTAssertTrue(1 < 2, "1 should be less than 2")
        XCTAssertTrue(1 < 2)
        // XCTAssertFalse
        XCTAssertFalse(1 > 2, "1 should not be greater than 2")
        XCTAssertFalse(1 > 2)
        // XCTAssertEqual
        XCTAssertEqual(4, 2 + 2, "2 plus 2 should equal 4")
        XCTAssertEqual(4, 2 + 2)
        // XCTAssertNotEqual
        XCTAssertNotEqual(5, 2 + 2, "2 plus 2 should not equal 5")
        XCTAssertNotEqual(5, 2 + 2)
        // XCTAssertNil
        let optionalNil: Int? = nil
        XCTAssertNil(optionalNil, "optionalNil should be nil")
        XCTAssertNil(optionalNil)
        // XCTAssertNotNil
        let optionalNotNil: Int? = 5
        XCTAssertNotNil(optionalNotNil, "optionalNotNil should not be nil")
        XCTAssertNotNil(optionalNotNil)
        // XCTAssertIdentical
        let obj1 = NSObject()
        let obj2 = obj1
        XCTAssertIdentical(obj1, obj2, "obj1 and obj2 should reference the same object")
        XCTAssertIdentical(obj1, obj2)
        // XCTAssertNotIdentical
        let obj3 = NSObject()
        XCTAssertNotIdentical(obj1, obj3, "obj1 and obj3 should not reference the same object")
        XCTAssertNotIdentical(obj1, obj3)
        // XCTAssertGreaterThan
        XCTAssertGreaterThan(5, 3, "5 should be greater than 3")
        XCTAssertGreaterThan(5, 3)
        // XCTAssertGreaterThanOrEqual
        XCTAssertGreaterThanOrEqual(5, 5, "5 should be greater than or equal to 5")
        XCTAssertGreaterThanOrEqual(5, 5)
        // XCTAssertLessThanOrEqual
        XCTAssertLessThanOrEqual(3, 5, "3 should be less than or equal to 5")
        XCTAssertLessThanOrEqual(3, 5)
        // XCTAssertLessThan
        XCTAssertLessThan(3, 5, "3 should be less than 5")
        XCTAssertLessThan(3, 5)
        // XCTFail
        XCTFail("This test always fails")
    }

    func testThrowingTests() throws {
        // XCTUnwrap
        let unwrappedOptional: Int? = 5
        let unwrappedValue = try XCTUnwrap(unwrappedOptional, "unwrappedOptional should not be nil")
        // XCTExpectFailure
        XCTExpectFailure("This test always fails") {
            try throwingFunction()
        }
    }
}
