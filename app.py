from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from flask import Flask, render_template, request

app = Flask(__name__)


@dataclass(frozen=True)
class ConverterConfig:
    title: str
    units: Tuple[str, ...]


LENGTH_UNITS: Dict[str, float] = {
    "millimeter": 0.001,
    "centimeter": 0.01,
    "meter": 1.0,
    "kilometer": 1000.0,
    "inch": 0.0254,
    "foot": 0.3048,
    "yard": 0.9144,
    "mile": 1609.344,
}

WEIGHT_UNITS: Dict[str, float] = {
    "milligram": 0.000001,
    "gram": 0.001,
    "kilogram": 1.0,
    "ounce": 0.028349523125,
    "pound": 0.45359237,
}

TEMPERATURE_UNITS: Tuple[str, ...] = ("Celsius", "Fahrenheit", "Kelvin")


CONFIGS = {
    "length": ConverterConfig("Length Converter", tuple(LENGTH_UNITS.keys())),
    "weight": ConverterConfig("Weight Converter", tuple(WEIGHT_UNITS.keys())),
    "temperature": ConverterConfig("Temperature Converter", TEMPERATURE_UNITS),
}


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    meters = value * LENGTH_UNITS[from_unit]
    return meters / LENGTH_UNITS[to_unit]


def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    kilograms = value * WEIGHT_UNITS[from_unit]
    return kilograms / WEIGHT_UNITS[to_unit]


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit == to_unit:
        return value

    if from_unit == "Celsius":
        celsius = value
    elif from_unit == "Fahrenheit":
        celsius = (value - 32) * 5 / 9
    else:
        celsius = value - 273.15

    if to_unit == "Celsius":
        return celsius
    if to_unit == "Fahrenheit":
        return (celsius * 9 / 5) + 32
    return celsius + 273.15


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/length", methods=["GET", "POST"])
def length() -> str:
    result = None
    selected = {}
    if request.method == "POST":
        value = float(request.form["value"])
        from_unit = request.form["from_unit"]
        to_unit = request.form["to_unit"]
        result = convert_length(value, from_unit, to_unit)
        selected = {
            "value": value,
            "from_unit": from_unit,
            "to_unit": to_unit,
        }
    return render_template(
        "converter.html",
        config=CONFIGS["length"],
        result=result,
        selected=selected,
        unit_label="Length",
    )


@app.route("/weight", methods=["GET", "POST"])
def weight() -> str:
    result = None
    selected = {}
    if request.method == "POST":
        value = float(request.form["value"])
        from_unit = request.form["from_unit"]
        to_unit = request.form["to_unit"]
        result = convert_weight(value, from_unit, to_unit)
        selected = {
            "value": value,
            "from_unit": from_unit,
            "to_unit": to_unit,
        }
    return render_template(
        "converter.html",
        config=CONFIGS["weight"],
        result=result,
        selected=selected,
        unit_label="Weight",
    )


@app.route("/temperature", methods=["GET", "POST"])
def temperature() -> str:
    result = None
    selected = {}
    if request.method == "POST":
        value = float(request.form["value"])
        from_unit = request.form["from_unit"]
        to_unit = request.form["to_unit"]
        result = convert_temperature(value, from_unit, to_unit)
        selected = {
            "value": value,
            "from_unit": from_unit,
            "to_unit": to_unit,
        }
    return render_template(
        "converter.html",
        config=CONFIGS["temperature"],
        result=result,
        selected=selected,
        unit_label="Temperature",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
