"""empty message

Revision ID: 7576403cdd0e
Revises: f07ece1b2464
Create Date: 2022-08-18 14:04:47.182944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7576403cdd0e'
down_revision = 'f07ece1b2464'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people_user',
    sa.Column('people_id', sa.Integer(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('people_id', 'users_id')
    )
    op.create_table('planets_user',
    sa.Column('planets_id', sa.Integer(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['planets_id'], ['planets.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('planets_id', 'users_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('planets_user')
    op.drop_table('people_user')
    # ### end Alembic commands ###