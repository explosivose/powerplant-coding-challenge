from flask import Flask, request
from enum import Enum

WIND_PC = 'wind(%)'

class FuelPriceType(Enum):
  GAS_PRICE = 'gas(euro/MWh)'
  KEROSINE_PRICE = 'gas(euro/MWh)'
  CO2_PRICE = 'co2(euro/ton)'

class PowerPlantType(Enum):
  GAS = 'gasfired'
  JET = 'turbojet'
  WIND = 'windturbine'

class PowerPlant:
  name: str
  type: PowerPlantType
  efficiency: float
  pmin: float
  pmax: float

def create_app():
  app = Flask(__name__)

  @app.post("/productionplan")
  def production_plan_controller():
    d = request.json
    load: float = d['load']
    fuels: Fuels = d['fuels']
    plants: list[PowerPlant] = d['powerplants']
    wind_pc = fuels[WIND_PC] / 100

    merit_order = [PowerPlantType.WIND]
    if fuels[FuelPriceType.KEROSINE_PRICE.value] > fuels[FuelPriceType.GAS_PRICE.value]:
      merit_order.append(PowerPlantType.JET)
      merit_order.append(PowerPlantType.GAS)
    else:
      merit_order.append(PowerPlantType.GAS)
      merit_order.append(PowerPlantType.JET)
    
    load_remaining = load
    plants_used = []
    print(merit_order)
    for power_type in merit_order:
      plant_selection = [x for x in plants if x['type'] == power_type.value]
      for plant in plant_selection:
        plants_used.append(plant_selection)
        if (power_type == PowerPlantType.WIND.value):
          load_remaining -= plant['pmax'] * wind_pc
        else:
          load_remaining -= plant['pmax'] * plant['efficiency']
        print(load_remaining)
        if load_remaining < 0:
          break
      if load_remaining < 0:
        break


    print(plants_used, '\n')
    return plants_used

  return app