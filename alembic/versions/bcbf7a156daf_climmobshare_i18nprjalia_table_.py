"""climmobShare - I18nPrjalia - table relationship

Revision ID: bcbf7a156daf
Revises: 8f39e41f9fed
Create Date: 2021-08-10 14:35:16.074531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bcbf7a156daf"
down_revision = "8f39e41f9fed"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("PRIMARY", "i18n_prjalias", type_="primary")
    op.create_primary_key(
        "pk_i18n_prjalias",
        "i18n_prjalias",
        ["project_id", "tech_id", "alias_id", "lang_code"],
    )

    op.create_foreign_key(
        op.f("fk_i18n_prjalias_project_id_prjalias"),
        "i18n_prjalias",
        "prjalias",
        ["project_id", "tech_id", "alias_id"],
        ["project_id", "tech_id", "alias_id"],
    )
    op.create_foreign_key(
        op.f("fk_i18n_prjalias_lang_code_i18n"),
        "i18n_prjalias",
        "i18n",
        ["lang_code"],
        ["lang_code"],
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("PRIMARY", "i18n_prjalias", type_="primary")
    op.create_primary_key(
        "pk_i18n_prjalias",
        "i18n_prjalias",
        ["user_name", "project_cod", "tech_id", "alias_id", "lang_code"],
    )

    op.drop_constraint(
        op.f("fk_i18n_prjalias_lang_code_i18n"), "i18n_prjalias", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_i18n_prjalias_project_id_prjalias"),
        "i18n_prjalias",
        type_="foreignkey",
    )
    # ### end Alembic commands ###
