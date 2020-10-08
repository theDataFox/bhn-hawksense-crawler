"""initial

Revision ID: ba9c222a756a
Revises: 
Create Date: 2020-10-08 11:25:48.472745

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ba9c222a756a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass

# from alembic import op
# import sqlalchemy as sa
#
#
# # revision identifiers, used by Alembic.
# revision = '6c82c972c61e'
# down_revision = '553260b3e828'
# branch_labels = None
# depends_on = None
#
#
# def upgrade():
#     op.execute("create schema foo")
#     ...
#
# def downgrade():
#     ...
#     op.execute("drop schema foo")
