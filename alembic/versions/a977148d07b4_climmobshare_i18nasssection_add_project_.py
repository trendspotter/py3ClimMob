"""climmobShare - I18nAsssection - add project_id

Revision ID: a977148d07b4
Revises: 48b5fffcfe95
Create Date: 2021-08-03 16:23:27.322406

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm.session import Session
from climmob.models.climmobv4 import I18nAsssection, Project

# revision identifiers, used by Alembic.
revision = "a977148d07b4"
down_revision = "48b5fffcfe95"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "i18n_asssection", sa.Column("project_id", sa.Unicode(length=64), nullable=True)
    )

    session = Session(bind=op.get_bind())
    try:
        projects = session.execute("Select * from project")
        for project in projects:
            session.execute(
                "UPDATE i18n_asssection SET project_id = '"
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
    op.drop_column("i18n_asssection", "project_id")
    # ### end Alembic commands ###
