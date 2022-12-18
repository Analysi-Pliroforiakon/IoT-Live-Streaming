import random

def air_conditioner_energyFactor(temperature):
  if temperature > 35 or temperature < 12: 
    return 3
  elif temperature > 25 or temperature < 16 :
    return 2
  else :
    return 1

def calculate_energyConsumption(temperature, type , randomEnergy, skew):
    if(randomEnergy):
        return random.uniform(0, 100 * type)
    wattsPerHour = air_conditioner_energyFactor(temperature) * type * abs(temperature - 20) * 2 + random.uniform(-0.5+skew, 0.5+skew)
    if(wattsPerHour > 100 * type):
        return 100 * type
    elif(wattsPerHour < 0):
        return 0
    else:
        return wattsPerHour

class AirConditionEnergyConsomption():
    def __init__(self, degresOutside, skew=0, random=False):
        self.degreesOutside = degresOutside
        self.skew = skew
        self.random = random
        self.HVAC1 = calculate_energyConsumption(self.degreesOutside, 1 , self.random, self.skew)
        self.HVAC2 = calculate_energyConsumption(self.degreesOutside, 2 , self.random, self.skew)
    def getConsumption(self, degresOutside):
        self.degreesOutside = degresOutside
        self.HVAC1 = calculate_energyConsumption(self.degreesOutside, 1 , self.random, self.skew)
        self.HVAC2 = calculate_energyConsumption(self.degreesOutside, 2 , self.random, self.skew)