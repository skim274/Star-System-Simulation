import time
from star_system import SolarSystem, Sun, Planet

solar_system = SolarSystem(width=1600, height=900)
sun = Sun(solar_system, mass=10_000)
planets = (
    Planet(
        solar_system,
        mass=1,
        position=(-350, 0),
        velocity=(0, 3),
    ),
    Planet(
        solar_system,
        mass=2,
        position=(-270, 0),
        velocity=(0, 4),
    ),
    Planet(
        solar_system,
        mass=2,
        position=(-260, 0),
        velocity=(0, 5),
    ),
)

while True:
    time.sleep(0.03)
    solar_system.calculate_all_body_interactions()
    solar_system.update_all()