#!/usr/bin/env python
"""Tests for `hoymiles_mqtt` package."""
import json

from hoymiles_modbus.client import MISeriesMicroinverterData, PlantData

from hoymiles_mqtt import MI_ENTITIES, PORT_ENTITIES
from hoymiles_mqtt.ha import HassMqtt

example_microinverter_data = MISeriesMicroinverterData(
    data_type=0,
    serial_number='102162804827',
    port_number=3,
    pv_voltage=1.234,
    pv_current=2.34,
    grid_voltage=22.33,
    grid_frequency=32.12,
    pv_power=40.31,
    today_production=431,
    total_production=8844,
    temperature=20.4,
    operating_status=3,
    alarm_code=0,
    alarm_count=2,
    link_status=1,
    reserved=[],
)
example_plant_data = PlantData('dtu_serial', microinverter_data=[example_microinverter_data])


def test_config_payload():
    """Test HassMqtt.config_payload."""
    ha = HassMqtt(mi_entities=['grid_voltage'], port_entities=['pv_voltage'])
    payload = list(ha.get_configs(example_plant_data))
    assert payload[0] == (
        'homeassistant/sensor/dtu_serial/DTU_pv_power/config',
        json.dumps(
            {
                'device': {
                    'name': 'DTU_dtu_serial',
                    'identifiers': ['hoymiles_mqtt_dtu_serial'],
                    'manufacturer': 'Hoymiles',
                },
                'name': 'pv_power',
                'unique_id': 'hoymiles_mqtt_DTU_dtu_serial_pv_power',
                'state_topic': 'homeassistant/hoymiles_mqtt/dtu_serial/state',
                'value_template': '{{ value_json.pv_power }}',
                'device_class': 'power',
                'unit_of_measurement': 'W',
                'state_class': 'measurement',
            }
        ),
    )
    assert payload[1] == (
        'homeassistant/sensor/dtu_serial/DTU_today_production/config',
        json.dumps(
            {
                'device': {
                    'name': 'DTU_dtu_serial',
                    'identifiers': ['hoymiles_mqtt_dtu_serial'],
                    'manufacturer': 'Hoymiles',
                },
                'name': 'today_production',
                'unique_id': 'hoymiles_mqtt_DTU_dtu_serial_today_production',
                'state_topic': 'homeassistant/hoymiles_mqtt/dtu_serial/state',
                'value_template': '{{ value_json.today_production }}',
                'device_class': 'energy',
                'unit_of_measurement': 'Wh',
                'state_class': 'total_increasing',
            }
        ),
    )
    assert payload[2] == (
        'homeassistant/sensor/dtu_serial/DTU_total_production/config',
        json.dumps(
            {
                'device': {
                    'name': 'DTU_dtu_serial',
                    'identifiers': ['hoymiles_mqtt_dtu_serial'],
                    'manufacturer': 'Hoymiles',
                },
                'name': 'total_production',
                'unique_id': 'hoymiles_mqtt_DTU_dtu_serial_total_production',
                'state_topic': 'homeassistant/hoymiles_mqtt/dtu_serial/state',
                'value_template': '{{ value_json.total_production }}',
                'device_class': 'energy',
                'unit_of_measurement': 'Wh',
                'state_class': 'total_increasing',
            }
        ),
    )
    assert payload[3] == (
        'homeassistant/binary_sensor/dtu_serial/DTU_alarm_flag/config',
        json.dumps(
            {
                'device': {
                    'name': 'DTU_dtu_serial',
                    'identifiers': ['hoymiles_mqtt_dtu_serial'],
                    'manufacturer': 'Hoymiles',
                },
                'name': 'alarm_flag',
                'unique_id': 'hoymiles_mqtt_DTU_dtu_serial_alarm_flag',
                'state_topic': 'homeassistant/hoymiles_mqtt/dtu_serial/state',
                'value_template': '{{ value_json.alarm_flag }}',
                'device_class': 'problem',
            }
        ),
    )
    assert payload[4] == (
        'homeassistant/sensor/102162804827/inv_grid_voltage/config',
        json.dumps(
            {
                'device': {
                    'name': 'inv_102162804827',
                    'identifiers': ['hoymiles_mqtt_102162804827'],
                    'manufacturer': 'Hoymiles',
                },
                'name': 'grid_voltage',
                'unique_id': 'hoymiles_mqtt_inv_102162804827_grid_voltage',
                'state_topic': 'homeassistant/hoymiles_mqtt/102162804827/state',
                'value_template': '{{ value_json.grid_voltage }}',
                'device_class': 'voltage',
                'unit_of_measurement': 'V',
                'state_class': 'measurement',
            }
        ),
    )
    assert payload[5] == (
        'homeassistant/sensor/102162804827/port_3_pv_voltage/config',
        json.dumps(
            {
                'device': {
                    'name': 'inv_102162804827',
                    'identifiers': ['hoymiles_mqtt_102162804827'],
                    'manufacturer': 'Hoymiles',
                },
                'name': 'port_3_pv_voltage',
                'unique_id': 'hoymiles_mqtt_port_3_102162804827_pv_voltage',
                'state_topic': 'homeassistant/hoymiles_mqtt/102162804827/3/state',
                'value_template': '{{ value_json.pv_voltage }}',
                'device_class': 'voltage',
                'unit_of_measurement': 'V',
                'state_class': 'measurement',
            }
        ),
    )


def test_get_states():
    """Test HassMqtt.get_states."""
    ha = HassMqtt(mi_entities=MI_ENTITIES, port_entities=PORT_ENTITIES)
    states = list(ha.get_states(example_plant_data))
    assert states[0] == (
        'homeassistant/hoymiles_mqtt/dtu_serial/state',
        '{"pv_power": 0.0, "today_production": 431, "total_production": 8844, "alarm_flag": "OFF"}',
    )
    assert states[1] == (
        'homeassistant/hoymiles_mqtt/102162804827/state',
        '{"grid_voltage": 22.33, "grid_frequency": 32.12, "temperature": 20.4, "operating_status": 3, '
        '"alarm_code": 0, "alarm_count": 2, "link_status": 1}',
    )
    assert states[2] == (
        'homeassistant/hoymiles_mqtt/102162804827/3/state',
        '{"pv_voltage": 1.234, "pv_current": 2.34, "pv_power": 40.31, "today_production": 431, '
        '"total_production": 8844}',
    )
