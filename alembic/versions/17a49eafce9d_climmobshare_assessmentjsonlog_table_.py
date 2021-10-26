"""climmobShare - AssessmentJsonLog - table relationship

Revision ID: 17a49eafce9d
Revises: c449c18b989e
Create Date: 2021-08-10 11:14:59.898437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "17a49eafce9d"
down_revision = "c449c18b989e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("PRIMARY", "assesment_jsonlog", type_="primary")
    op.create_primary_key(
        "pk_project", "assesment_jsonlog", ["project_id", "ass_cod", "log_id"]
    )

    op.create_foreign_key(
        op.f("fk_assesment_jsonlog_project_id_assessment"),
        "assesment_jsonlog",
        "assessment",
        ["project_id", "ass_cod"],
        ["project_id", "ass_cod"],
    )
    op.create_foreign_key(
        op.f("fk_assesment_jsonlog_enum_user_enumerator"),
        "assesment_jsonlog",
        "enumerator",
        ["enum_user", "enum_id"],
        ["user_name", "enum_id"],
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("PRIMARY", "assesment_jsonlog", type_="primary")
    op.create_primary_key(
        "pk_project",
        "assesment_jsonlog",
        ["user_name", "project_cod", "ass_cod", "log_id"],
    )

    op.drop_constraint(
        op.f("fk_assesment_jsonlog_enum_user_enumerator"),
        "assesment_jsonlog",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_assesment_jsonlog_project_id_assessment"),
        "assesment_jsonlog",
        type_="foreignkey",
    )
    # ### end Alembic commands ###
