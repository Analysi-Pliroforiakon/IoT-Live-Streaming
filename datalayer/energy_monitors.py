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
    elif(abs(temperature - 20) < 3):
        # return wattsPerHour or 0 with equal probability
        # print('random choice for wattsPerHour: ', wattsPerHour, ' type: ', type)
        return random.choice([wattsPerHour, 0, 0])
    else:
        return wattsPerHour
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
    #print('hour: ', curr_datetime.hour, ' minute: ', curr_datetime.minute)
    if(curr_datetime.hour == 0 and curr_datetime.minute == 0):

        w =  2600 * 24 + prev + random.uniform(-1000, 1000)
        self.prevEtot = w
        #print('returned w: ', w)
        return w

    else:
        #print('returned prev: ', prev)
        return prev

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