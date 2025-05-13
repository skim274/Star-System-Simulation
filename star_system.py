import itertools
import math
import turtle

class SolarSystemBody(turtle.Turtle):
    """
    Base class for all stars and planets in star system
    Inherits from turtle.Turtle to utilize graphics
    """
    # Minimum display size for planets to ensure visibility
    min_display_size = 20
    # Base logarithmic scaling of body size for display
    display_log_base = 1.1
    
    def __init__(
        self,
        solar_system,
        mass,
        position=(0, 0),
        velocity=(0, 0),
    ):
        """
        Initialize star or planet
        Args:
            solar_system: SolarSystem instance this star or planet belongs to
            mass: mass of this star or planet
            position: initial (x, y) position as a tuple
            velocity: initial (vx, vy) velocity vector as a tuple 
        """
        # Initialize turtle.Turtle parent class
        super().__init__()
        # Initialize mass
        self.mass = mass
        # Set initial position
        self.setposition(position)
        self.velocity = velocity
         
        # Calculate display size using log scaling to 
        # ensure all bodies are visible while 
        # maintaining relative size differences
        self.display_size = max(
            math.log(self.mass, self.display_log_base),
            self.min_display_size,
        )
        
        # Lift pen to avoid drawing lines when moving
        self.penup()
        # Hide default turtle shape
        self.hideturtle()
        
        # Add this star or planet to this solar system
        solar_system.add_body(self)
    
    def draw(self):
        """ Clear previous drawing and draw the body as a dot """
        self.clear()
        self.dot(self.display_size)
        
    def move(self):
        """ Update this body's position position based on its current velocity """
        self.setx(self.xcor() + self.velocity[0])
        self.sety(self.ycor() + self.velocity[1])

class Sun(SolarSystemBody):
    """ Star at center of solar system """
    def __init__(
        self,
        solar_system,
        mass,
        position=(0, 0),
        velocity=(0, 0),
    ):
        """
        Initialize Sun object
        Args:
            solar_system: SolarSystem instance this star belongs to
            mass: mass of this star- typically much larger than planets
            position: initial position (usually center)
            velocity: initial velocity (usually 0)
        """
        super().__init__(solar_system, mass, position, velocity)
        # Set color of star to yellow
        self.color("yellow")
    
    
class Planet(SolarSystemBody):
    """ Represents a planet orbiting in the system """
    # Cycle through these colors for planets
    colors = itertools.cycle(["red", "green", "blue"])
    
    def __init__(
        self,
        solar_system,
        mass,
        position=(0, 0),
        velocity=(0, 0)
    ):
        """
        Initialize Planet object
        Args:
            solar_system: SolarSystem instance this planet belongs to
            mass: mass of this planet
            position: initial position (away from its star)
            velocity: initial velocity
        """
        super().__init__(solar_system, mass, position, velocity)
        
        # Assign next color in itertools cycle to this planet
        self.color(next(Planet.colors))
        
class SolarSystem:
    """
    Manages the simulation of a solar system with multiple bodies.
    Handles the screen setup, body management, and physics calculations.
    """
    def __init__(self, width, height):
        """
        Initialize the solar system simulation environment.
        Args:
            width: Width of the simulation window in pixels
            height: Height of the simulation window in pixels
        """
        # Create and configure the turtle screen
        self.solar_system = turtle.Screen()
        # Turn off animation updates for manual control
        self.solar_system.tracer(0)
        # Set the window size
        self.solar_system.setup(width, height)
        # Set black background for space
        self.solar_system.bgcolor("black")
        
        # List to keep track of all bodies in the system
        self.bodies = []
    
    def add_body(self, body):
        """
        Add a celestial body to the solar system.       
        Args:
            body: SolarSystemBody instance to add
        """
        self.bodies.append(body)
        
    def remove_body(self, body):
        """
        Remove a celestial body from the solar system.
        Used when bodies collide or need to be deleted.
        Args:
            body: A SolarSystemBody instance to remove
        """
        # Clear the body's visual representation
        body.clear()
        # Remove it from the tracked bodies list
        self.bodies.remove(body)

    def update_all(self):
        """
        Update the positions and visuals of all bodies in the system.
        Call this once per frame/iteration of the simulation.
        """
        for body in self.bodies:
            # Update position based on velocity
            body.move()
            # Redraw the body at its new position
            body.draw()
        # Update the screen with all changes at once
        self.solar_system.update()
    
    @staticmethod
    def accelerate_due_to_gravity(
        first: SolarSystemBody,
        second: SolarSystemBody, 
    ):
        """
        Calculate and apply gravitational acceleration between two bodies.
        Uses a simplified version of Newton's law of universal gravitation.
        Args:
            first: First SolarSystemBody
            second: Second SolarSystemBody
        """
        # Calculate gravitational force using F = G * m1 * m2 / r^2
        # G (gravitational constant) is assumed to be 1 for simplicity
        force = first.mass * second.mass / first.distance(second) ** 2
        # Get the angle between the two bodies
        angle = first.towards(second)
        
        # +1 for the first body (attraction toward second), -1 for the second (opposite direction)
        reverse = 1
        
        # Apply acceleration to both bodies
        for body in first, second:
            # F = ma, so a = F/m
            acceleration = force / body.mass
            
            # Split acceleration into x and y components
            acc_x = acceleration * math.cos(math.radians(angle))
            acc_y = acceleration * math.sin(math.radians(angle))
            
            # Update velocity by adding acceleration components
            body.velocity = (
                body.velocity[0] + (reverse * acc_x),
                body.velocity[1] + (reverse * acc_y),
            )
            
            # Flip the direction for the second body (equal and opposite reaction)
            reverse = -1
    
    def check_collision(self, first, second):
        """
        Check if two bodies have collided and handle the collision.
        Currently, planets are destroyed if they collide with a sun.
        Args:
            first: First SolarSystemBody
            second: Second SolarSystemBody
        """
        # Skip collision check between planets (optional behavior)
        if isinstance(first, Planet) and isinstance(second, Planet):
            return
        
        # Check if distance between bodies is less than sum of their radii
        if first.distance(second) < first.display_size/2 + second.display_size/2:
            # Process both bodies
            for body in first, second:
                # If the body is a planet, remove it (absorbed by sun or destroyed)
                if isinstance(body, Planet):
                    self.remove_body(body)
    
    def calculate_all_body_interactions(self):
        """
        Calculate all gravitational interactions and check for collisions
        between all pairs of bodies in the system.
        """
        # Create a copy to avoid issues if bodies are removed during iteration
        bodies_copy = self.bodies.copy()
        
        # Loop through all unique pairs of bodies
        for idx, first in enumerate(bodies_copy):
            for second in bodies_copy[idx + 1:]:
                # Calculate and apply gravitational forces
                self.accelerate_due_to_gravity(first, second)
                # Check and handle collisions
                self.check_collision(first, second)