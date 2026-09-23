import inspect

from agent import tools


def test_cada_tool_tiene_contrato():
    specs = {s["name"]: s for s in tools.TOOL_SPECS}
    for name, fn in tools.TOOLS.items():
        assert name in specs, f"falta el spec de {name}"
        s = specs[name]
        assert len(s.get("description", "")) >= 15
        schema = s["input_schema"]
        assert schema["type"] == "object"
        params = set(inspect.signature(fn).parameters)
        assert set(schema["properties"]) == params, f"{name}: properties no coinciden con los parámetros"
        assert set(schema.get("required", [])) <= params
