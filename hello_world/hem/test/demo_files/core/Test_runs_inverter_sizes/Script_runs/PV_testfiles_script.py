import json
import copy

# Base JSON data
base_data = {
    "SimulationTime": {
        "start": 5088,
        "end": 5112,
        "step": 1
    },
    "ExternalConditions": {
        "air_temperatures": [19.0] * 24,
        "wind_speeds": [3.9, 3.8, 3.9, 4.1, 3.8, 4.2, 4.3, 4.1] * 3,
        "ground_temperatures": [8.0, 8.7, 9.4, 10.1, 10.8, 10.5, 11.0, 12.7] * 3,
        "diffuse_horizontal_radiation": [0, 0, 0, 0, 35, 73, 139, 244, 320, 361, 369, 348, 318, 249, 225, 198, 121, 68, 19, 0, 0, 0, 0, 0],
        "direct_beam_radiation": [0, 0, 0, 0, 0, 0, 7, 53, 63, 164, 339, 242, 315, 577, 385, 285, 332, 126, 7, 0, 0, 0, 0, 0],
        "solar_reflectivity_of_ground": [0.2] * 24,
        "latitude": 51.383,
        "longitude": -0.783,
        "timezone": 0,
        "start_day": 212,
        "end_day": 212,
        "time_series_step": 1,
        "january_first": 1,
        "daylight_savings": "not applicable",
        "leap_day_included": False,
        "direct_beam_conversion_needed": False,
        "shading_segments": [
            {"number": 1, "start360": 0, "end360": 45},
            {"number": 2, "start360": 45, "end360": 90},
            {"number": 3, "start360": 90, "end360": 135},
            {"number": 4, "start360": 135, "end360": 180, 
             "shading": [
                 {"type": "obstacle", "height": 10.5, "distance": 12}
             ]
            },
            {"number": 5, "start360": 180, "end360": 225},
            {"number": 6, "start360": 225, "end360": 270},
            {"number": 7, "start360": 270, "end360": 315},
            {"number": 8, "start360": 315, "end360": 360}
        ]
    },
    "InternalGains": {
        "metabolic gains":{
            "start_day": 212,
            "time_series_step": 1,
            "schedule": {
                "main": [256, 368, 584, 416, 712, 448, 816, 648] * 3
            }
        },
        "other": {
            "start_day": 212,
            "time_series_step": 1,
            "schedule": {
                "main": [88, 200, 184, 376, 576, 544, 728, 608] * 3
            }
        }
    },
    "ApplianceGains": {
        "lighting": {
            "start_day": 212,
            "time_series_step": 1,
            "gains_fraction": 0.5,
            "EnergySupply": "mains elec",
            "schedule": {
                "8hrs": [32.0, 46.0, 33.0, 21.0, 12.0, 17.0, 25.0, 46.0],
                "main": [{"value": "8hrs", "repeat": 3}]
            }
        },
        "cooking": {
            "start_day": 212,
            "time_series_step": 1,
            "gains_fraction": 1,
            "EnergySupply": "mains elec",
            "schedule": {
                "8hrs": [300.0, 120.0, 220.0, 750.0, 890.0, 150.0, 550.0, 280.0],
                "main": [{"value": "8hrs", "repeat": 3}]
            }
        }
    },
    "ColdWaterSource": {
        "mains water": {
            "start_day": 212,
            "temperatures": [17.0, 17.1, 17.2, 17.3, 17.4, 17.5, 17.6, 17.7] * 3,
            "time_series_step": 1
        }
    },
    "EnergySupply": {
        "mains elec": {
            "fuel": "electricity",
            "ElectricBattery": {
                "capacity": 2,
                "charge_discharge_efficiency": 0.8
            },
            "is_export_capable": True
        }
    },
    "Control": {
        "hw timer": {
            "type": "OnOffTimeControl",
            "start_day": 212,
            "time_series_step": 1,
            "schedule": {
                "main": [{"value": True, "repeat": 24}]
            }
        },
        "main__hw timer__converted_from_OnOffTimeControl": {
            "type": "SetpointTimeControl",
            "start_day": 212,
            "time_series_step": 1,
            "schedule": {
                "main": [{"value": 21.0, "repeat": 24}]
            }
        },
        "cooling system 1__hw timer__converted_from_OnOffTimeControl": {
            "type": "SetpointTimeControl",
            "start_day": 212,
            "time_series_step": 1,
            "schedule": {
                "main": [{"value": 25.0, "repeat": 24}]
            }
        }
    },
    "HotWaterSource": {
        "hw cylinder": {
            "type": "StorageTank",
            "volume": 80.0,
            "daily_losses": 1.68,
            "min_temp": 52.0,
            "setpoint_temp": 55.0,
            "ColdWaterSource": "mains water",
            "HeatSource": {
                "immersion": {
                    "type": "ImmersionHeater",
                    "power": 3.0,
                    "EnergySupply": "mains elec",
                    "Control": "hw timer",
                    "heater_position": 0.1,
                    "thermostat_position": 0.33
                }
            }
        }
    },
    "HotWaterDemand": {
        "Shower": {
            "mixer": {
                "type": "MixerShower",
                "flowrate": 8.0,
                "ColdWaterSource": "mains water"
            },
            "IES": {
                "type": "InstantElecShower",
                "rated_power": 9.0,
                "ColdWaterSource": "mains water",
                "EnergySupply": "mains elec"
            }
        },
        "Bath": {
            "medium": {
                "size": 100,
                "ColdWaterSource": "mains water",
                "flowrate": 8.0
            }
        },
        "Other": {
            "other": {
                "flowrate": 8.0,
                "ColdWaterSource": "mains water"
            }
        },
        "Distribution": [
            {
                "location": "internal",
                "internal_diameter_mm": 25,
                "length": 8.0
            },
            {
                "location": "internal",
                "internal_diameter_mm": 25,
                "length": 8.0
            },
            {
                "location": "external",
                "internal_diameter_mm": 25,
                "length": 8.0
            },
            {
                "location": "external",
                "internal_diameter_mm": 25,
                "length": 8.0
            }
        ]
    },
    "Events": {
        "Shower": {
            "IES": [
                {"start": 4.1, "duration": 6, "temperature": 41.0},
                {"start": 4.5, "duration": 6, "temperature": 41.0},
                {"start": 6, "duration": 6, "temperature": 41.0}
            ],
            "mixer": [
                {"start": 7, "duration": 6, "temperature": 41.0}
            ]
        },
        "Bath":{
            "medium": [
                {"start": 6, "temperature": 41.0}
            ]
        },
        "Other": {
            "other": [
                {"start": 5, "duration": 6, "temperature": 41.0}
            ]
        }
    },
    "InverterSystem": {
        "Type": "string inverter",
        "strings": 1,
        "string_size": 20,
        "inverter_efficiency": 0.96,
        "inverter_losses": {
            "static": 0.02,
            "dynamic": 0.02
        },
        "inverter_power_limitations": {
            "nominal": 5.0,
            "overload": 6.0
        },
        "inverter_voltage_limits": {
            "min": 250.0,
            "max": 600.0
        },
        "inverter_peak_power_dc": 2,
        "inverter_peak_power_ac": 0.1,
    }
}

# Increments
increment_dc = 0
increment_ac = 0.1

# Create x new JSON files with incremented values
x = 20
for i in range (x):
    new_data = copy.deepcopy(base_data)
    new_data["InverterSystem"]["inverter_peak_power_dc"] += increment_dc * i
    new_data["InverterSystem"]["inverter_peak_power_ac"] += increment_ac * i

    # Write to new JSON file
    filename = f"PV_testfile_script_{i+1}.json"
    with open(filename, 'w') as outfile:
        json.dump(new_data, outfile, indent=4)
    print(f"Created {filename} with inverter_peak_power_dc = {new_data['InverterSystem']['inverter_peak_power_dc']} and inverter_peak_power_ac = {new_data['InverterSystem']['inverter_peak_power_ac']}")
    i += 1
