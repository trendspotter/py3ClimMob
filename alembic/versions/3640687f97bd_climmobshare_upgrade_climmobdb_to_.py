"""climmobShare - Upgrade ClimMobDB to utf8mb4_unicode_ci

Revision ID: 3640687f97bd
Revises: c6682ac905bc
Create Date: 2021-10-22 10:53:04.087781

"""
from alembic import op
import sqlalchemy as sa
from alembic import context

# revision identifiers, used by Alembic.
revision = "3640687f97bd"
down_revision = "c6682ac905bc"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    config_uri = context.config.get_main_option("sqlalchemy.url", None)
    schema = config_uri.split("/")[3].split("?")[0]

    conn = op.get_bind()
    sql = (
        "ALTER DATABASE "
        + schema
        + " CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci"
    )
    conn.execute(sql)
    sql = (
        "SELECT table_name FROM INFORMATION_SCHEMA.TABLES "
        "WHERE TABLE_TYPE = 'BASE TABLE' and TABLE_SCHEMA = '" + schema + "'"
    )
    res = conn.execute(sql)
    conn.execute("SET foreign_key_checks = 0")
    for a_record in res:
        sql = (
            "ALTER TABLE " + schema + ".{} CONVERT TO CHARACTER "
            "SET utf8mb4 COLLATE utf8mb4_unicode_ci".format(a_record[0])
        )
        conn.execute(sql)
    conn.execute("SET foreign_key_checks = 1")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
