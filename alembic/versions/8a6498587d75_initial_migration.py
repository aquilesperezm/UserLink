"""Initial migration

Revision ID: 8a6498587d75
Revises: 
Create Date: 2024-10-07 11:50:48.120881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8a6498587d75'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userlink_rel_tags_by_post')
    op.drop_table('userlink_comment')
    op.drop_table('userlink_post')
    op.drop_table('userlink_tag')
    op.drop_table('userlink_user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userlink_user',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('userlink_user_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('fullname', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('lastname', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='userlink_user_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('userlink_tag',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('userlink_tag_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('slug', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('color', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='userlink_tag_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('userlink_post',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('userlink_post_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('author', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['userlink_user.id'], name='userlink_post_user_id_fkey', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='userlink_post_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('userlink_comment',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('author', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('likes', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('status', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['userlink_post.id'], name='userlink_comment_post_id_fkey', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='userlink_comment_pkey')
    )
    op.create_table('userlink_rel_tags_by_post',
    sa.Column('idpost', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('idtag', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['idpost'], ['userlink_post.id'], name='userlink_rel_tags_by_post_idpost_fkey', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['idtag'], ['userlink_tag.id'], name='userlink_rel_tags_by_post_idtag_fkey', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('idpost', 'idtag', name='userlink_rel_tags_by_post_pkey')
    )
    # ### end Alembic commands ###
