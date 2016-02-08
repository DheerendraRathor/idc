
class PostStatusTypes(object):
    DRAFT = 0
    PRIVATE = 1
    PUBLISHED = 2

    @classmethod
    def dict(cls) -> dict:
        return {
            cls.DRAFT: 'Draft',
            cls.PRIVATE: 'Private',
            cls.PUBLISHED: 'Published',
        }

    @classmethod
    def choices(cls) -> [(int, str)]:
        return [(k, v) for k, v in cls.dict().items()]
