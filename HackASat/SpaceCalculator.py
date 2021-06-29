from datetime import datetime

# All units are in kilometers, seconds, or degrees unless otherwise stated.
class Orbit:
    """Default Constructor"""
    def __init__(self, semi_major_axis, eccentricity, inclination, longitude_of_ascending_node, true_anomaly, body, t=datetime()):
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.inclination = inclination
        self.longitude_of_ascending_node = longitude_of_ascending_node
        self.true_anomaly = true_anomaly
        self.body = body
        self.time = t
        self.positionVector = calcPositionVector(self)
        self.velocityVector = calcVelocityVector(self)

    @classmethod
    def fromPosAndVelVectors(cls, positionVector, velocityVector, body, t=datetime()):
        # Math to convert stuff 
        semi_major_axis = 0
        eccentricity = 0
        inclination = 0
        longitude_of_ascending_node = 0
        true_anomaly = 0
        body = 0
        time = t
        newOrbit = cls(semi_major_axis, eccentricity, inclination, longitude_of_ascending_node, true_anomaly, body, time)
        return newOrbit

    @classmethod
    def fromPosVectors(cls, positionVectorAtT1, positionVectorAtT2, body, t1=datetime(), t2=datetime()):
        # Math to convert stuff using Lambert's Equations
        semi_major_axis = 0
        eccentricity = 0
        inclination = 0
        longitude_of_ascending_node = 0
        true_anomaly = 0
        body = 0
        time = t2
        newOrbit = cls(Orbit, semi_major_axis, eccentricity, inclination, longitude_of_ascending_node, true_anomaly, body, time)
        return newOrbit

    def calcPositionVector(self):
        # Math to calculate position vector from Kepler elements
        position = [0.0, 0.0, 0.0]
        return position

    def calcVelocityVector(self):
        # Math to calculate velocity vector from Kepler elements
        velocity = [0.0, 0.0, 0.0]
        return velocity

class Attitude:
    """Default Constructor"""
    def __init__(self, quaternion=[0.0, 0.0, 0.0, 0.0]):                                                      # Default values so we can create a satellite in an orbit where we don't care about attitude
        self.quaternion = quaternion

class Propulsion:
    """Default Constructor"""                                                  
    def __init__(self, thrust=0.0, fuel=0.0, isp=0.0):                                                        # Default values so we can create a satellite in an orbit where we don't care about propulsion
        self.thrust = thrust
        self.fuel = fuel
        self.isp = isp
    
class Manuever:                                                                                               # We can maybe do without this class, but it might be useful?
    """Default Constructor"""
    def __init__(self, deltaV, burnStart=datetime(), burnEnd=datetime()):
        self.deltaV = deltaV
        self.burnStart = burnStart
        self.burnEnd = burnEnd


class Satellite:
    """Default Constructor"""
    def __init__(self, orbit, attitude=Attitude(), propulsion=Propulsion(), mass=0, gravitationalConstant=0): # Default values so we can create a satellite in an orbit where we don't care about attitude or propulsion
        self.Orbit = orbit
        self.Attitude = attitude
        self.Propulsion = propulsion
        self.mass = mass

    def calcGravitationalConstant(self, mass):
        # Math to calculate the gravitational constant for a given body
        gravitationalConstant = 0.0
        return gravitationalConstant

    def manuever(self, newOrbit):
        # Calculate deltaV, burnStart, and burnTime to reach newOrbit from current self.orbit, self.attitude, and self.propulsion
        deltaV = 0.0
        burnStart = datetime()
        burnEnd = datetime()
        man = Manuever(deltaV, burnStart, burnEnd)
        return man
