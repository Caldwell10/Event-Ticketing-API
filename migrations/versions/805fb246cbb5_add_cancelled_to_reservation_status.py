# revision identifiers, used by Alembic.
revision = "805fb246cbb5"
down_revision = "e72eaec77123"

from alembic import op

def upgrade():
    # Postgres: replace the check constraint to add CANCELLED
    op.drop_constraint(
        "reservation_status_check", "reservations", type_="check"
    )
    op.create_check_constraint(
        "reservation_status_check",
        "reservations",
        "status IN ('HELD','CONFIRMED','EXPIRED','CANCELLED')",
    )

def downgrade():
    # revert to the 3-state constraint
    op.drop_constraint(
        "reservation_status_check", "reservations", type_="check"
    )
    op.create_check_constraint(
        "reservation_status_check",
        "reservations",
        "status IN ('HELD','CONFIRMED','EXPIRED')",
    )
