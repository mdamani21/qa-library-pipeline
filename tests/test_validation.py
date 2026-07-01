from data_processing.validation import validate_isbn

def test_valid_isbn():
    result = validate_isbn('9780306406157')
    # TODO: assert result is True

def test_invalid_isbn():
    result = validate_isbn('not-an-isbn')
    # TODO: assert result is False

def test_wrong_length():
    result = validate_isbn('123456789')
    # TODO: assert result is False