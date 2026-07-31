from .models import OccupancySnapshot

def record_occupancy_snapshot(manager):
    print("========== UTILS CALLED ==========")

    snapshot = OccupancySnapshot.objects.create(
        manager=manager,
        occupied=999,
        vacant=999,
        total_units=999,
        occupancy_rate=99.99,
    )

    print(f"Snapshot created: {snapshot.id}")