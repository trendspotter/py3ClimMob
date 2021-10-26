"""climmobShare - Move project_dashboard from Project to userProject

Revision ID: c65271d94458
Revises: a71f0b33ceb9
Create Date: 2021-08-11 09:52:21.746893

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "c65271d94458"
down_revision = "a71f0b33ceb9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("project", "project_dashboard")
    op.add_column(
        "user_project",
        sa.Column(
            "project_dashboard",
            sa.Integer(),
            server_default=sa.text("'1'"),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user_project", "project_dashboard")
    op.add_column(
        "project",
        sa.Column(
            "project_dashboard",
            mysql.INTEGER(),
            server_default=sa.text("'1'"),
            autoincrement=False,
            nullable=True,
        ),
    )
    # ### end Alembic commands ###
