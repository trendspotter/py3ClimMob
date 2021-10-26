"""climmobShare - Package - add project_id

Revision ID: 7597dde01af1
Revises: 067043357453
Create Date: 2021-08-03 13:51:39.506463

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm.session import Session
from climmob.models.climmobv4 import Package, Project

# revision identifiers, used by Alembic.
revision = "7597dde01af1"
down_revision = "067043357453"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "package", sa.Column("project_id", sa.Unicode(length=64), nullable=True)
    )

    session = Session(bind=op.get_bind())
    try:
        projects = session.execute("Select * from project")
        for project in projects:
            session.execute(
                "UPDATE package SET project_id = '"
                + project.project_id
                + "' WHERE (user_name = '"
                + project.user_name
                + "') and (project_cod = '"
                + project.project_cod
                + "');"
            )
    except Exception as e:
        print(str(e))
        exit(1)

    session.commit()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("package", "project_id")
    # ### end Alembic commands ###
