"""Initial migration

Revision ID: ed430d1a1fc3
Revises: 
Create Date: 2022-11-30 13:37:32.893857

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ed430d1a1fc3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    role = op.create_table('role',
                           sa.Column('id', sa.Integer(), nullable=False),
                           sa.Column('name', sa.String(length=50), nullable=False),
                           sa.PrimaryKeyConstraint('id')
                           )
    op.bulk_insert(role, [{'id': 1, 'name': 'user'}, {'id': 2, 'name': 'admin'}])
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(length=255), nullable=False),
                    sa.Column('first_name', sa.String(length=255), nullable=False),
                    sa.Column('last_name', sa.String(length=255), nullable=False),
                    sa.Column('email', sa.String(length=255), nullable=False),
                    sa.Column('password', sa.String(length=255), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('username')
                    )
    op.create_table('account',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('balance', sa.Numeric(precision=15, scale=2), nullable=False),
                    sa.Column('userId', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['userId'], ['user.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('users_roles',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('role_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_roles')
    op.drop_table('account')
    op.drop_table('user')
    op.drop_table('role')
    # ### end Alembic commands ###
