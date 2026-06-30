
def validate_isbn(isbn):
    """Validate ISBN-13 format."""

    if isbn is None:
        return False

    # Convert to string (handles integers from pandas)
    isbn = str(isbn).strip()

    # Remove hyphens
    isbn = isbn.replace("-", "").replace(" ", "")

    # Must be exactly 13 digits
    if len(isbn) != 13 or not isbn.isdigit():
        return False
    
    # Calculate check digit from first 12 digits
    total = 0
    for i in range(12):
        digit = int(isbn[i])
        if i % 2 == 0:
            total += digit * 1
        else:
            total += digit * 3

    check_digit = (10 - (total % 10)) % 10

    # Compare with 13th digit
    return check_digit == int(isbn[12])


def test_valid_isbn():
    result = validate_isbn('9780306406157')
    assert result == True

def test_invalid_isbn():
    result = validate_isbn('not-an-isbn')
    assert result == False

def test_wrong_length():
    result = validate_isbn('123456789')
    assert result == False

def test_invalid_check_digit():
    # valid isbn: 9780306406157
    result = validate_isbn('9780306406158')
    assert result == False