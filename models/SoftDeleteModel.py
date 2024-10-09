from sqlalchemy import Column, Boolean

class SoftDeleteModel:
    is_deleted = Column(Boolean, server_default="0")