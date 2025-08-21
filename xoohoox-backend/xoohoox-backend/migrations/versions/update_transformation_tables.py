"""Update transformation tables to match new model structure

Revision ID: update_transformation_tables
Revises: 4d7ab37d55a5
Create Date: 2024-04-12 12:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'update_transformation_tables'
down_revision: Union[str, None] = '4d7ab37d55a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create transformation_stages table
    op.create_table(
        'transformation_stages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.String(), nullable=True),
        sa.Column('stage_number', sa.Integer(), nullable=True),
        sa.Column('stage_name', sa.String(), nullable=True),
        sa.Column('start_date', sa.DateTime(), nullable=True),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transformation_stages_batch_id'), 'transformation_stages', ['batch_id'], unique=False)
    
    # Create juicing_results table
    op.create_table(
        'juicing_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('stage_id', sa.Integer(), nullable=True),
        sa.Column('juice_volume', sa.Float(), nullable=True),
        sa.Column('juice_yield', sa.Float(), nullable=True),
        sa.Column('brix', sa.Float(), nullable=True),
        sa.Column('ph', sa.Float(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['stage_id'], ['transformation_stages.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create fermentation_results table
    op.create_table(
        'fermentation_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('stage_id', sa.Integer(), nullable=True),
        sa.Column('initial_gravity', sa.Float(), nullable=True),
        sa.Column('final_gravity', sa.Float(), nullable=True),
        sa.Column('abv', sa.Float(), nullable=True),
        sa.Column('temperature', sa.Float(), nullable=True),
        sa.Column('ph', sa.Float(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['stage_id'], ['transformation_stages.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('fermentation_results')
    op.drop_table('juicing_results')
    op.drop_index(op.f('ix_transformation_stages_batch_id'), table_name='transformation_stages')
    op.drop_table('transformation_stages') 