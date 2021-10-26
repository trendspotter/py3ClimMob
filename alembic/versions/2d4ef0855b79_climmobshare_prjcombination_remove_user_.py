"""climmobShare - Prjcombination - Remove user_name and project_cod

Revision ID: 2d4ef0855b79
Revises: c9d4950fdd02
Create Date: 2021-08-26 11:15:07.824770

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "2d4ef0855b79"
down_revision = "c9d4950fdd02"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("prjcombination", "project_cod")
    op.drop_column("prjcombination", "user_name")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "prjcombination",
        sa.Column("user_name", mysql.VARCHAR(length=80), nullable=False),
    )
    op.add_column(
        "prjcombination",
        sa.Column("project_cod", mysql.VARCHAR(length=80), nullable=False),
    )
    # ### end Alembic commands ###
