from package_table import PackageTable
from distance_map import DistanceMap
from datetime import datetime, timedelta, time


packages = PackageTable()
delivery_map = DistanceMap()


# Return closest package to a given address
def find_nearest(address, package_ids):
    package_addresses = dict((packages.lookup(id).address, id) for id in package_ids)
    distance, closest_address = delivery_map.closest(address, package_addresses.keys())
    return package_addresses[closest_address], distance


# Given a set of id's get the order using nearest neighbor
def get_order(package_ids, start_time=0.0):
    current_position = 'HUB'
    delivery_order = []
    ids = package_ids.copy()  # Copy since removing from this list
    priority_packages = [id for id in ids if packages.lookup(id).deadline]

    # Keep track of time to change package 9's address
    current_time = start_time

    while len(ids):
        nearest_package, nearest_distance = find_nearest(current_position, ids)
        if nearest_distance != 0 and len(priority_packages):
            nearest_package, nearest_distance = find_nearest(current_position, priority_packages)
        delivery_order.append(nearest_package)

        current_time += nearest_distance / 18 * 60 * 60
        if current_time >= 8400.0:  # seconds accrued from 8:00 until 10:20
            p = packages.lookup(9)
            p.address = '410 S State St (84111)'
            p.zipcode = '84111'
        priority_packages = [id for id in ids if packages.lookup(id).deadline and id != nearest_package]
        ids.remove(nearest_package)
        current_position = packages.lookup(nearest_package).address
    return delivery_order


def seconds_to_time(seconds, offset=0):
    as_date = datetime.combine(datetime.today(), time(8,0,0)) + timedelta(seconds=(seconds+offset))
    return as_date.time()


# Return time-based statuses for each delivery event
def deliver(package_ids, truck, start_time=0.0):
    order = get_order(package_ids, start_time)

    for package in order:
        packages.lookup(package).status = 'at hub; loaded on truck {0}'.format(truck)
    events = {0: dict((id, packages.lookup(id).status) for id in package_ids)}

    for id in package_ids:
        packages.lookup(id).status = 'en route on truck {0}'.format(truck)
    events[start_time] = dict((id, packages.lookup(id).status) for id in package_ids)

    current_position = 'HUB'
    current_time = start_time
    total_mileage = 0

    for id in order:
        distance = delivery_map.distance(current_position, packages.lookup(id).address)
        current_time += distance / 18 * 60 * 60
        packages.lookup(id).status = (f'delivered at {seconds_to_time(current_time).strftime("%H:%M")} to'
                                      f' {packages.lookup(id).address}')
        total_mileage += distance
        events[current_time] = dict((id, packages.lookup(id).status) for id in package_ids)
        current_position = packages.lookup(id).address

    total_mileage += delivery_map.distance(current_position, 'HUB')
    current_time = total_mileage / 18 * 60 * 60
    return total_mileage, current_time, events