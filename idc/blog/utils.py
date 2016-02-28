
class PostStatusTypes(object):
    DRAFT = 0
    PRIVATE = 1
    REQUESTED = 2
    PUBLISHED = 3


    @classmethod
    def dict(cls) -> dict:
        return {
            cls.DRAFT: 'Save As Draft',
            cls.PRIVATE: 'Publish within IIT',
            cls.REQUESTED: 'Request Pending',
            cls.PUBLISHED: 'Publish to Public',
        }

    @classmethod
    def user_options(cls) -> dict:
        return {
            cls.DRAFT: 'Save As Draft',
            cls.PRIVATE: 'Publish within IIT',
            cls.PUBLISHED: 'Publish to Public',
        }

    @classmethod
    def choices(cls) -> [(int, str)]:
        return [(k, v) for k, v in cls.dict().items()]
