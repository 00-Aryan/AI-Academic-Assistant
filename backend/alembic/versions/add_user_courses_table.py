"""Add user_courses table for many-to-many relationship

Revision ID: add_user_courses_table
Revises: aab38a067542
Create Date: 2025-12-05 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_user_courses_table'
down_revision = 'aab38a067542'
branch_labels = None
depends_on = None


def upgrade():
    # Create user_courses table
    op.create_table(
        'user_courses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('assigned_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'course_id', name='uq_user_course'),
        sa.Index('ix_user_courses_user_id', 'user_id'),
        sa.Index('ix_user_courses_course_id', 'course_id'),
    )


def downgrade():
    # Drop user_courses table
    op.drop_table('user_courses')
