"""add crypto policies

Revision ID: 7f1c2d9a4b11
Revises: ecd4a5e56027
Create Date: 2026-08-08
"""

from alembic import op
import sqlalchemy as sa


revision = "7f1c2d9a4b11"
down_revision = "ecd4a5e56027"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "crypto_policies",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            "algorithm_name",
            sa.String(length=100),
            nullable=False
        ),

        sa.Column(
            "enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        ),

        sa.Column(
            "deployment_mode",
            sa.String(length=20),
            nullable=False,
            server_default="CLASSICAL"
        ),

        sa.Column(
            "enforcement_action",
            sa.String(length=30),
            nullable=False,
            server_default="ALLOW"
        ),

        sa.Column(
            "priority",
            sa.Integer(),
            nullable=False,
            server_default="100"
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=True
        ),

        sa.UniqueConstraint(
            "algorithm_name",
            name="uq_crypto_policies_algorithm_name"
        )
    )


def downgrade():

    op.drop_table("crypto_policies")
