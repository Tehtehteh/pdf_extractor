import sqlalchemy as sa

from .engine import metadata


pdfs = sa.Table(
    "pdf_files",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("uri", sa.String)
)

pdf_extracted_dates = sa.Table(
    "pdf_extracted_dates",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("pdf_id", sa.Integer, sa.ForeignKey("pdf_files.id"), nullable=False),
    sa.Column("extracted_date", sa.Date, nullable=False),
    sa.Column("extracted_context", sa.String)
)
