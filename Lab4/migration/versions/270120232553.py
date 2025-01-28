"""Adăugat noi proprietăți și model nou Address

Revision ID: 270120232553
Revises: None
Create Date: 2025-01-27 10:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '270120232553'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Modificarea tabelei 'users'
    op.add_column('users', sa.Column('phone_number', sa.String(length=20), nullable=True))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True, default=True))
    op.alter_column('users', 'created_at', type_=sa.String(length=100))  # Modificarea tipului de dată

    # Crearea tabelei 'addresses'
    op.create_table(
        'addresses',
        sa.Column('address_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('street', sa.String(length=255), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('postal_code', sa.String(length=20), nullable=False),
        sa.Column('country', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('address_id')
    )

def downgrade():
    # Îndepărtarea coloanelor adăugate în 'users'
    op.drop_column('users', 'phone_number')
    op.drop_column('users', 'is_active')
    op.alter_column('users', 'created_at', type_=sa.DateTime())  # Restaurarea tipului de dată

    # Ștergerea tabelei 'addresses'
    op.drop_table('addresses')
