"""add enumeratos to tables _jsonlog

Revision ID: 5dade0633cee
Revises: 8f782ab34aea
Create Date: 2020-02-25 11:36:10.712488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5dade0633cee"
down_revision = "8f782ab34aea"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "assesment_jsonlog", sa.Column("enum_id", sa.String(length=80), nullable=False)
    )
    op.add_column(
        "assesment_jsonlog",
        sa.Column("enum_user", sa.String(length=80), nullable=False),
    )
    op.create_foreign_key(
        op.f("fk_assesment_jsonlog_enum_user_enumerator"),
        "assesment_jsonlog",
        "enumerator",
        ["enum_user", "enum_id"],
        ["user_name", "enum_id"],
        ondelete="CASCADE",
    )
    op.add_column(
        "registry_jsonlog", sa.Column("enum_id", sa.String(length=80), nullable=False)
    )
    op.add_column(
        "registry_jsonlog", sa.Column("enum_user", sa.String(length=80), nullable=False)
    )
    op.create_foreign_key(
        op.f("fk_registry_jsonlog_enum_user_enumerator"),
        "registry_jsonlog",
        "enumerator",
        ["enum_user", "enum_id"],
        ["user_name", "enum_id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("fk_registry_jsonlog_enum_user_enumerator"),
        "registry_jsonlog",
        type_="foreignkey",
    )
    op.drop_column("registry_jsonlog", "enum_user")
    op.drop_column("registry_jsonlog", "enum_id")
    op.drop_constraint(
        op.f("fk_assesment_jsonlog_enum_user_enumerator"),
        "assesment_jsonlog",
        type_="foreignkey",
    )
    op.drop_column("assesment_jsonlog", "enum_user")
    op.drop_column("assesment_jsonlog", "enum_id")
    # ### end Alembic commands ###
