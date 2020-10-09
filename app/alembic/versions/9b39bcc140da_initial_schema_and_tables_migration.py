"""initial schema and tables migration

Revision ID: 9b39bcc140da
Revises: 13b346b8a803
Create Date: 2020-10-08 21:25:36.922567

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9b39bcc140da'
down_revision = '13b346b8a803'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('canonical_links',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=True),
                    sa.Column('href', sa.Text(), nullable=True),
                    sa.Column('url', sa.Text(), nullable=True),
                    sa.Column('domain', sa.Text(), nullable=True),
                    sa.Column('self_ref', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    schema='crawl'
                    )
    op.create_table('images',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=True),
                    sa.Column('src', sa.Text(), nullable=True),
                    sa.Column('alt', sa.Text(), nullable=True),
                    sa.Column('file_name', sa.Text(), nullable=True),
                    sa.Column('url', sa.Text(), nullable=True),
                    sa.Column('domain', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    schema='crawl'
                    )
    op.create_table('in_links',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=True),
                    sa.Column('url', sa.Text(), nullable=True),
                    sa.Column('in_link', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    schema='crawl'
                    )
    op.create_table('out_links',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=True),
                    sa.Column('href', sa.Text(), nullable=True),
                    sa.Column('status_code', sa.Integer(), nullable=True),
                    sa.Column('href_domain', sa.Text(), nullable=True),
                    sa.Column('url', sa.Text(), nullable=True),
                    sa.Column('domain', sa.Text(), nullable=True),
                    sa.Column('external', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    schema='crawl'
                    )
    op.create_table('page',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=True),
                    sa.Column('url', sa.Text(), nullable=True),
                    sa.Column('domain', sa.Text(), nullable=True),
                    sa.Column('valid_characters', sa.Boolean(), nullable=True),
                    sa.Column('status_code', sa.Integer(), nullable=True),
                    sa.Column('redirects', sa.ARRAY(sa.Text()), nullable=True),
                    sa.Column('title_text', sa.Text(), nullable=True),
                    sa.Column('title_text_length', sa.Integer(), nullable=True),
                    sa.Column('title_text_pixel_width', sa.Integer(), nullable=True),
                    sa.Column('description_text', sa.Text(), nullable=True),
                    sa.Column('description_text_length', sa.Integer(), nullable=True),
                    sa.Column('description_text_pixel_width', sa.Integer(), nullable=True),
                    sa.Column('h1_text', sa.ARRAY(sa.Text()), nullable=True),
                    sa.Column('h1_text_length', sa.ARRAY(sa.Integer()), nullable=True),
                    sa.Column('h2_text', sa.ARRAY(sa.Text()), nullable=True),
                    sa.Column('images', sa.ARRAY(sa.Text()), nullable=True),
                    sa.Column('out_links', sa.ARRAY(sa.Text()), nullable=True),
                    sa.Column('external_links', sa.ARRAY(sa.Text()), nullable=True),
                    sa.Column('canonical_links', sa.ARRAY(sa.Text()), nullable=True),
                    sa.Column('body_text', sa.Text(), nullable=True),
                    sa.Column('unigrams', sa.JSON(), nullable=True),
                    sa.Column('bigrams', sa.JSON(), nullable=True),
                    sa.Column('trigrams', sa.JSON(), nullable=True),
                    sa.Column('content_hash', sa.Text(), nullable=True),
                    sa.Column('content_length', sa.Integer(), nullable=True),
                    sa.Column('word_count', sa.Integer(), nullable=True),
                    sa.Column('text_ratio', sa.REAL(), nullable=True),
                    sa.Column('iframe_list', sa.ARRAY(sa.Text()), nullable=True),
                    sa.Column('object_list', sa.ARRAY(sa.Text()), nullable=True),
                    sa.Column('embed_list', sa.ARRAY(sa.Text()), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    schema='crawl'
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('page', schema='crawl')
    op.drop_table('out_links', schema='crawl')
    op.drop_table('in_links', schema='crawl')
    op.drop_table('images', schema='crawl')
    op.drop_table('canonical_links', schema='crawl')
    # ### end Alembic commands ###
