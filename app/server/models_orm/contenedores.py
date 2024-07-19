from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Date,Float
from sqlalchemy.orm import relationship
from datetime import datetime
from server.database import Base

def _get_date():
    return datetime.datetime.now()

class ModelContenedor(Base):
    __tablename__ = "contenedores_orm"
    id = Column(Integer,primary_key=True,index=True)
    nombre_contenedor = Column(String(100),default=None)
    tipo = Column(String(50),default=None )
    estado = Column(Integer, default=1)
    descripcionC = Column(String(255),default=None)
    created_at  = Column(Date, default=_get_date)
    updated_at = Column(Date, default=_get_date)
    empresa_id = Column(Integer, default=1)
    generador_id = Column(Integer, default=1)
    telemetria_id = Column(Integer, default=1)
    set_point = Column(Float(precision=10, scale=2),default=None)
    latitud = Column(Float(precision=10, scale=2),default=None)
    longitud = Column(Float(precision=10, scale=2),default=None)
    ultima_fecha = Column(Date,default=None)
    temp_supply_1 = Column(Float(precision=10, scale=2),default=None)
    temp_supply_2 = Column(Float(precision=10, scale=2),default=None)
    return_air = Column(Float(precision=10, scale=2),default=None)
    evaporation_coil = Column(Float(precision=10, scale=2),default=None) 
    condensation_coil = Column(Float(precision=10, scale=2),default=None)
    compress_coil_1 = Column(Float(precision=10, scale=2),default=None)
    compress_coil_2 = Column(Float(precision=10, scale=2),default=None)
    ambient_air = Column(Float(precision=10, scale=2),default=None)
    cargo_1_temp = Column(Float(precision=10, scale=2),default=None)
    cargo_3_temp = Column(Float(precision=10, scale=2),default=None)
    cargo_3_temp = Column(Float(precision=10, scale=2),default=None)
    cargo_4_temp = Column(Float(precision=10, scale=2),default=None)
    relative_humidity = Column(Float(precision=10, scale=2),default=None)
    avl = Column(Float(precision=10, scale=2),default=None)
    suction_pressure = Column(Float(precision=10, scale=2),default=None)
    discharge_pressure = Column(Float(precision=10, scale=2),default=None)
    line_voltage = Column(Float(precision=10, scale=2),default=None)
    line_frequency = Column(Float(precision=10, scale=2),default=None)
    consumption_ph_1 = Column(Float(precision=10, scale=2),default=None)
    consumption_ph_2 = Column(Float(precision=10, scale=2),default=None)
    consumption_ph_3 = Column(Float(precision=10, scale=2),default=None)
    co2_reading = Column(Float(precision=10, scale=2),default=None)
    o2_reading = Column(Float(precision=10, scale=2),default=None)
    condenser_speed = Column(Float(precision=10, scale=2),default=None)
    battery_voltage = Column(Float(precision=10, scale=2),default=None)
    power_kwh = Column(Float(precision=10, scale=2),default=None)
    power_trip_reading = Column(Float(precision=10, scale=2),default=None)
    power_trip_duration = Column(Float(precision=10, scale=2),default=None)
    suction_temp = Column(Float(precision=10, scale=2),default=None)
    discharge_temp = Column(Float(precision=10, scale=2),default=None)
    supply_air_temp = Column(Float(precision=10, scale=2),default=None)
    dl_battery_temp = Column(Float(precision=10, scale=2),default=None)
    dl_battery_charge = Column(Float(precision=10, scale=2),default=None)
    power_consumption = Column(Float(precision=10, scale=2),default=None)
    power_consumption_avg = Column(Float(precision=10, scale=2),default=None)
    alarm_present = Column(Float(precision=10, scale=2),default=None)
    capacity_load = Column(Float(precision=10, scale=2),default=None)
    power_state = Column(Float(precision=10, scale=2),default=None)
    controlling_mode = Column(String(50),default=None)
    humidity_control = Column(Float(precision=10, scale=2),default=None)
    humidity_set_point = Column(Float(precision=10, scale=2),default=None)
    fresh_air_ex_mode = Column(Float(precision=10, scale=2),default=None)
    fresh_air_ex_rate = Column(Float(precision=10, scale=2),default=None)
    fresh_air_ex_delay = Column(Float(precision=10, scale=2),default=None)
    set_point_o2 = Column(Float(precision=10, scale=2),default=None)
    set_point_co2 = Column(Float(precision=10, scale=2),default=None)
    defrost_term_temp = Column(Float(precision=10, scale=2),default=None)
    defrost_interval = Column(Float(precision=10, scale=2),default=None)
    water_cooled_conde = Column(Float(precision=10, scale=2),default=None)
    usda_trip = Column(Float(precision=10, scale=2),default=None)
    evaporator_exp_valve = Column(Float(precision=10, scale=2),default=None)
    suction_mod_valve = Column(Float(precision=10, scale=2),default=None)
    hot_gas_valve = Column(Float(precision=10, scale=2),default=None)
    economizer_valve = Column(Float(precision=10, scale=2),default=None)
    ethylene = Column(Float(precision=10, scale=2),default=None)
    stateProcess = Column(String(50),default=None)
    stateInyection = Column(String(50),default=None)
    timerOfProcess = Column(Float(precision=10, scale=2),default=None)
    modelo = Column(String(50),default=None)
    alarm_number = Column(Float(precision=10, scale=2),default=None)
    NA = Column(String(10),default=None)
    ripener_prueba = Column(Integer,default=None)
    defrost_prueba = Column(Integer,default=None)
    sp_ethyleno = Column(Float(precision=10, scale=2),default=None)
    extra_1 = Column(Integer,default=None)
    extra_2 = Column(Integer,default=None)














