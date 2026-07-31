from .models import Unit, OccupancySnapshot


def record_occupancy_snapshot(manager):
    """
    Record a snapshot only if occupancy has changed.
    """

    total_units = Unit.objects.filter(
        property__manager=manager
    ).count()

    occupied_units = Unit.objects.filter(
        property__manager=manager,
        status="OCCUPIED"
    ).count()

    vacant_units = Unit.objects.filter(
        property__manager=manager,
        status="VACANT"
    ).count()

    occupancy_rate = 0

    if total_units > 0:
        occupancy_rate = round(
            (occupied_units / total_units) * 100,
            2
        )

    latest = (
        OccupancySnapshot.objects
        .filter(manager=manager)
        .order_by("-recorded_at")
        .first()
    )

    if latest:

        if (
            latest.occupied == occupied_units
            and latest.vacant == vacant_units
            and latest.total_units == total_units
        ):
            return

    OccupancySnapshot.objects.create(
        manager=manager,
        occupied=occupied_units,
        vacant=vacant_units,
        total_units=total_units,
        occupancy_rate=occupancy_rate
    )