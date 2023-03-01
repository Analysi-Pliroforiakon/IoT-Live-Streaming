import random

# This function returns the energy factor of the air conditioner
# obiosly, it is higher whem temperature is not in the range of 16-25
# since the air conditioner is working harder to cool or heat the room
def air_conditioner_energyFactor(temperature):
  if temperature > 35 or temperature < 12: 
    return 3
  elif temperature > 25 or temperature < 16 :
    return 2
  else :
    return 1
# This function returns the energy consumption of the air conditioner
# it is calculated based on the energy factor and the temperature
def calculate_energyConsumption(temperature, type , randomEnergy, skew):
    if(randomEnergy):
        return random.uniform(0, 100 * type)
    wattsPerHour = air_conditioner_energyFactor(temperature) * type * abs(temperature - 20) * 2 + random.uniform(-0.5+skew, 0.5+skew)
    if(wattsPerHour > 100 * type):
        return 100 * type
    elif(wattsPerHour < 0):
        return 0
    elif(abs(temperature - 20) < 3):
        # return wattsPerHour or 0 with equal probability
        return random.choice([wattsPerHour, 0, 0])
    else:
        return wattsPerHour
# This function returns the energy consumption of some appliances
# If type is 2, it is a kitchen tool that is using more energy at mid day
# it is calculated based on time of the day, mid day which is 13:00 to 15:00 
# the microwave is using more energy -> someone is cooking.
# if type is not 2 then it is a light bulb that is using more energy at night
def calculate_energy_base_on_hours(curr_datetime, type , randomEnergy, skew):
    if(randomEnergy):
        return random.uniform(0, 100 * type)
    if(type == 2):
        # this is a kitchen tool that is using 200Wh 
        # if curr_datetime.hour >= 13 and curr_datetime.hour <= 15 else np.random.uniform(0, 100 * type)
        if curr_datetime.hour >= 13 and curr_datetime.hour <= 15:
            return 100 * type 
        else:
            return random.uniform(0, 100 * type)
    else:
        # it is a light bulb that is using 100Wh only at night
        if curr_datetime.hour >= 19 and curr_datetime.hour <= 23:
            return 100 * type
        else:
            return random.uniform(0, 100 * type)
    
def calculate_total_energyConsumption(curr_datetime, prev, self):
    if(curr_datetime.hour == 0 and curr_datetime.minute == 0):

        w =  2600 * 24 + prev + random.uniform(-1000, 1000)
        self.prevEtot = w
        return w

    else:
        return prev
# Class to handle energy consumption
# of all the appliances in the house
class EnergyConsumption():
    def __init__(self, degresOutside, curr_datetime, skew=0, random=False):
        self.degreesOutside = degresOutside
        self.curr_datetime = curr_datetime
        self.skew = skew
        self.random = random
        self.HVAC1 = calculate_energyConsumption(self.degreesOutside, 1 , self.random, self.skew)
        self.HVAC2 = calculate_energyConsumption(self.degreesOutside, 2 , self.random, self.skew)
        self.MiAC1 = calculate_energy_base_on_hours(self.curr_datetime, 1.5 , self.random, self.skew)
        self.MiAC2 = calculate_energy_base_on_hours(self.curr_datetime, 2 , self.random, self.skew)
        self.prevEtot = 0
        self.Etot = calculate_total_energyConsumption(self.curr_datetime, self.prevEtot, self)
    def getConsumption(self, degresOutside, curr_datetime):
        self.degreesOutside = degresOutside
        self.curr_datetime = curr_datetime
        self.HVAC1 = calculate_energyConsumption(self.degreesOutside, 1 , self.random, self.skew)
        self.HVAC2 = calculate_energyConsumption(self.degreesOutside, 2 , self.random, self.skew)
        self.MiAC1 = calculate_energy_base_on_hours(self.curr_datetime, 1.5 , self.random, self.skew)
        self.MiAC2 = calculate_energy_base_on_hours(self.curr_datetime, 2 , self.random, self.skew)
        self.Etot = calculate_total_energyConsumption(self.curr_datetime, self.prevEtot, self)