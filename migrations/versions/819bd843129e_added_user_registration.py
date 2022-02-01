"""added user registration

Revision ID: 819bd843129e
Revises: 1a38b97d69f4
Create Date: 2022-01-25 14:23:05.153418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '819bd843129e'
down_revision = '1a38b97d69f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_registration',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('firstname', sa.String(length=40), nullable=False),
    sa.Column('lastname', sa.String(length=40), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('updates', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_registration')
    # ### end Alembic commands ###