import XCTest

final class UnsupportedAssertions: XCTestCase {
    func testUnsupportedTypes() {
        // XCTAssertThrowsError
        XCTAssertThrowsError(try throwingFunction()) { error in
            XCTAssertEqual(error as? MyError, MyError.someError, "The error should be MyError.someError")
        }
        // XCTAssertNoThrow
        XCTAssertNoThrow(try nonThrowingFunction(), "This function should not throw an error")
    }
    
    // Helper functions and enum for error throwing tests
    enum MyError: Error {
        case someError
    }
    
    func throwingFunction() throws {
        throw MyError.someError
    }
    
    func nonThrowingFunction() throws {
        // This function doesn't throw
    }
}