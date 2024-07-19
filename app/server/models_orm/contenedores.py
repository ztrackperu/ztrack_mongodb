from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Date,Float,TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import text
from server.database import (
    Base
)
def _get_date():
    return datetime.datetime.now()

#    Column(
#       'last_updated',
#        TIMESTAMP,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
#    )

class ModelContenedor(Base):
    __tablename__ = "contenedores_orm"
    id = Column(Integer,primary_key=True,index=True)
    nombre_contenedor = Column(String(100),default=None)
    tipo = Column(String(50),default=None )
    estado = Column(Integer, server_default=text("1"))
    descripcionC = Column(String(255),default=None)
    #created_at  = Column(Date, default=_get_date)
    #updated_at = Column(Date, default=_get_date)
    empresa_id = Column(Integer, server_default=text("1"))
    generador_id = Column(Integer, server_default=text("1"))
    telemetria_id = Column(Integer, server_default=text("1"))
    created_at  = Column(TIMESTAMP,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    #estado = Column(Integer, default=1) 
    #tipo = Column(String, default="NA")
    set_point = Column(Float,default=None)
    latitud = Column(Float,default=None)
    longitud = Column(Float,default=None)
    ultima_fecha = Column(Date,default=None)
    temp_supply_1 = Column(Float,default=None)
    temp_supply_2 = Column(Float,default=None)
    return_air = Column(Float,default=None)
    evaporation_coil = Column(Float,default=None) 
    condensation_coil = Column(Float,default=None)
    compress_coil_1 = Column(Float,default=None)
    compress_coil_2 = Column(Float,default=None)
    ambient_air = Column(Float,default=None)
    cargo_1_temp = Column(Float,default=None)
    cargo_3_temp = Column(Float,default=None)
    cargo_3_temp = Column(Float,default=None)
    cargo_4_temp = Column(Float,default=None)
    relative_humidity = Column(Float,default=None)
    avl = Column(Float,default=None)
    suction_pressure = Column(Float,default=None)
    discharge_pressure = Column(Float,default=None)
    line_voltage = Column(Float,default=None)
    line_frequency = Column(Float,default=None)
    consumption_ph_1 = Column(Float,default=None)
    consumption_ph_2 = Column(Float,default=None)
    consumption_ph_3 = Column(Float,default=None)
    co2_reading = Column(Float,default=None)
    o2_reading = Column(Float,default=None)
    condenser_speed = Column(Float,default=None)
    battery_voltage = Column(Float,default=None)
    power_kwh = Column(Float,default=None)
    power_trip_reading = Column(Float,default=None)
    power_trip_duration = Column(Float,default=None)
    suction_temp = Column(Float,default=None)
    discharge_temp = Column(Float,default=None)
    supply_air_temp = Column(Float,default=None)
    dl_battery_temp = Column(Float,default=None)
    dl_battery_charge = Column(Float,default=None)
    power_consumption = Column(Float,default=None)
    power_consumption_avg = Column(Float,default=None)
    alarm_present = Column(Float,default=None)
    capacity_load = Column(Float,default=None)
    power_state = Column(Float,default=None)
    controlling_mode = Column(String(50),default=None)
    humidity_control = Column(Float,default=None)
    humidity_set_point = Column(Float,default=None)
    fresh_air_ex_mode = Column(Float,default=None)
    fresh_air_ex_rate = Column(Float,default=None)
    fresh_air_ex_delay = Column(Float,default=None)
    set_point_o2 = Column(Float,default=None)
    set_point_co2 = Column(Float,default=None)
    defrost_term_temp = Column(Float,default=None)
    defrost_interval = Column(Float,default=None)
    water_cooled_conde = Column(Float,default=None)
    usda_trip = Column(Float,default=None)
    evaporator_exp_valve = Column(Float,default=None)
    suction_mod_valve = Column(Float,default=None)
    hot_gas_valve = Column(Float,default=None)
    economizer_valve = Column(Float,default=None)
    ethylene = Column(Float,default=None)
    stateProcess = Column(String(50),default=None)
    stateInyection = Column(String(50),default=None)
    timerOfProcess = Column(Float,default=None)
    modelo = Column(String(50),default=None)
    alarm_number = Column(Float,default=None)
    NA = Column(String(10),server_default=text("NA"))
    ripener_prueba = Column(Integer,server_default=text("1"))
    defrost_prueba = Column(Integer,server_default=text("1"))
    sp_ethyleno = Column(Float,server_default=text("1"))
    extra_1 = Column(Integer,server_default=text("0"))
    extra_2 = Column(Integer,server_default=text("0"))














