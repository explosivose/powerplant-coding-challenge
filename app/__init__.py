from flask import Flask, request
from enum import Enum

class Fuels:
  gasPrice: float
  kerosinePrice: float
  co2Price: float
  windPc: float

class PowerPlantType(Enum):
  GAS = 'gasfired'
  JET = 'turbojet'
  WIND = 'windturbine'

class PowerPlant:
  name: str
  t: PowerPlantType
  efficiency: float
  pmin: float
  pmax: float

def create_app():
  app = Flask(__name__)

  @app.post("/productionplan")
  def production_plan_controller():
    d = request.json
    return d

  return app