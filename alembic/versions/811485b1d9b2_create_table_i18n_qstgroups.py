"""create table i18n_qstgroups

Revision ID: 811485b1d9b2
Revises: 7ff846f965e6
Create Date: 2021-06-04 15:46:41.299070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "811485b1d9b2"
down_revision = "7ff846f965e6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "i18n_qstgroups",
        sa.Column("user_name", sa.String(length=80), nullable=False),
        sa.Column("qstgroups_id", sa.String(length=80), nullable=False),
        sa.Column("lang_code", sa.String(length=5), nullable=False),
        sa.Column("qstgroups_name", sa.String(length=120), nullable=True),
        sa.ForeignKeyConstraint(
            ["lang_code"],
            ["i18n.lang_code"],
            name=op.f("fk_i18n_qstgroups_lang_code_i18n"),
        ),
        sa.ForeignKeyConstraint(
            ["user_name", "qstgroups_id"],
            ["qstgroups.user_name", "qstgroups.qstgroups_id"],
            name=op.f("fk_i18n_qstgroups_user_name_qstgroups"),
        ),
        sa.PrimaryKeyConstraint(
            "user_name", "qstgroups_id", "lang_code", name=op.f("pk_i18n_qstgroups")
        ),
        mysql_default_charset="utf8",
        mysql_engine="InnoDB",
    )
    op.create_index(
        op.f("ix_i18n_qstgroups_lang_code"),
        "i18n_qstgroups",
        ["lang_code"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_i18n_qstgroups_lang_code"), table_name="i18n_qstgroups")
    op.drop_table("i18n_qstgroups")
    # ### end Alembic commands ###
