import sqlalchemy
from schemas.appschema import  *
setting=Settings()
metadata = sqlalchemy.MetaData()
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(50)),
    sqlalchemy.Column("role", sqlalchemy.String(50)),
    sqlalchemy.Column("email", sqlalchemy.String(50)),
    sqlalchemy.Column("password", sqlalchemy.String(550)),
)
job_detail = sqlalchemy.Table(
    "job_detail",
    metadata,
    sqlalchemy.Column("job_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "recruiter_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.user_id"),
        nullable=False,
    ),
    sqlalchemy.Column("job_title", sqlalchemy.String(500)),
    sqlalchemy.Column("job_description", sqlalchemy.String(500)),
    sqlalchemy.Column("skills", sqlalchemy.String(500)),
    sqlalchemy.Column("location", sqlalchemy.String(100)),
    sqlalchemy.Column("salary", sqlalchemy.FLOAT),
    sqlalchemy.Column("employement_type", sqlalchemy.String(100)),
    sqlalchemy.Column("experience", sqlalchemy.String(100)),
    sqlalchemy.Column("deadline", sqlalchemy.String(100)),
)
document_details = sqlalchemy.Table(
    "document_details",
    metadata,
    sqlalchemy.Column("file_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("file_name", sqlalchemy.String(500)),
    sqlalchemy.Column("file_path", sqlalchemy.String(500)),
    sqlalchemy.Column("upload_date", sqlalchemy.String(50000)),
    sqlalchemy.Column(
        "candidate_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.user_id"),
        nullable=False,
    ),
)
applications = sqlalchemy.Table(
    "applications",
    metadata,
    sqlalchemy.Column("application_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "a_user_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.user_id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "a_job_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("job_detail.job_id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column("applied_at", sqlalchemy.TIMESTAMP),
)
engine = sqlalchemy.create_engine(setting.DATABASE_URL_SYNC)
metadata.create_all(engine)
print("Tables Have Been created")
