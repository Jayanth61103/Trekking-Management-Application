import uuid

def generate_uuid(prefix):
    """
    Generates IDs like:

    STF-34AB8D21
    TRK-28D9C4AA
    TREK-19AB7732
    BOOK-83FF0021
    """

    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"