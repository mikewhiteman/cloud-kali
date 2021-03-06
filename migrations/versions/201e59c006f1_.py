"""empty message

Revision ID: 201e59c006f1
Revises: 773bdab2d6c2
Create Date: 2020-12-30 23:44:08.598166

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '201e59c006f1'
down_revision = '773bdab2d6c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('instances',
    sa.Column('ami_id', sa.String(length=60), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=512), nullable=True),
    sa.PrimaryKeyConstraint('ami_id'),
    sa.UniqueConstraint('ami_id')
    )
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_table('instances')
    # ### end Alembic commands ###
