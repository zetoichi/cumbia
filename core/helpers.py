import shortuuid

def generate_uuid(length: int=22) -> str:
    """Generate a UUID"""
    return shortuuid.ShortUUID().random(length=length)