"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2025-01-24 10:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create license status enum
    op.execute("CREATE TYPE licensestatus AS ENUM ('active', 'inactive', 'suspended', 'expired')")
    
    # Create license type enum
    op.execute("CREATE TYPE licensetype AS ENUM ('business', 'professional', 'trade', 'food_service', 'retail')")
    
    # Create business_licenses table
    op.create_table('business_licenses',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('license_number', sa.String(length=50), nullable=False),
        sa.Column('business_name', sa.String(length=255), nullable=False),
        sa.Column('business_type', sa.Enum('business', 'professional', 'trade', 'food_service', 'retail', name='licensetype'), nullable=False),
        sa.Column('status', sa.Enum('active', 'inactive', 'suspended', 'expired', name='licensestatus'), nullable=False),
        sa.Column('issued_date', sa.DateTime(), nullable=False),
        sa.Column('expiration_date', sa.DateTime(), nullable=False),
        sa.Column('issuing_authority', sa.String(length=255), nullable=False),
        sa.Column('street_address', sa.String(length=255), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('state', sa.String(length=50), nullable=False),
        sa.Column('zip_code', sa.String(length=20), nullable=False),
        sa.Column('contact_person', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('conditions', sa.Text(), nullable=True),
        sa.Column('is_renewable', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_business_licenses_license_number'), 'business_licenses', ['license_number'], unique=True)
    op.create_index(op.f('ix_business_licenses_business_name'), 'business_licenses', ['business_name'], unique=False)
    op.create_index(op.f('ix_business_licenses_city'), 'business_licenses', ['city'], unique=False)
    op.create_index(op.f('ix_business_licenses_state'), 'business_licenses', ['state'], unique=False)
    op.create_index(op.f('ix_business_licenses_zip_code'), 'business_licenses', ['zip_code'], unique=False)
    op.create_index(op.f('ix_business_licenses_expiration_date'), 'business_licenses', ['expiration_date'], unique=False)

def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_business_licenses_expiration_date'), table_name='business_licenses')
    op.drop_index(op.f('ix_business_licenses_zip_code'), table_name='business_licenses')
    op.drop_index(op.f('ix_business_licenses_state'), table_name='business_licenses')
    op.drop_index(op.f('ix_business_licenses_city'), table_name='business_licenses')
    op.drop_index(op.f('ix_business_licenses_business_name'), table_name='business_licenses')
    op.drop_index(op.f('ix_business_licenses_license_number'), table_name='business_licenses')
    
    # Drop table
    op.drop_table('business_licenses')
    
    # Drop enums
    op.execute("DROP TYPE licensetype")
    op.execute("DROP TYPE licensestatus")