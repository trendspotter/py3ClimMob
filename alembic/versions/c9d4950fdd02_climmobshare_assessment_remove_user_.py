"""climmobShare - Assessment - Remove user_name and project_cod

Revision ID: c9d4950fdd02
Revises: 6203e8d86451
Create Date: 2021-08-19 14:40:48.342960

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "c9d4950fdd02"
down_revision = "6203e8d86451"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("assessment", "user_name")
    op.drop_column("assessment", "project_cod")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "assessment", sa.Column("project_cod", mysql.VARCHAR(length=80), nullable=False)
    )
    op.add_column(
        "assessment", sa.Column("user_name", mysql.VARCHAR(length=80), nullable=False)
    )
    # ### end Alembic commands ###
