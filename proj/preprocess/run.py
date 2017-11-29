# line
from . import bus_line
from . import subway_line
# node
from . import bicycle_node
from . import car_node
from . import subway_gate
from . import subway_station
from . import bus_node
# link
from . import bicycle_link
from . import subway_link
from . import walk_link
from . import bus_link
from . import subway_gate_link


def update_line():
    subway_line.run()
    bus_line.run()


def update_node():
    bicycle_node.run()
    car_node.run()
    subway_gate.run()
    subway_station.run()
    bus_node.run()


def update_link():
    bicycle_link.run()
    bus_link.run()
    subway_link.run()
    subway_gate_link.run()
    walk_link.run()


def run():
    update_line()
    update_node()
    update_link()
