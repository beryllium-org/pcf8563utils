rename_process("bma423axis")
vr("opts", be.api.xarg())
be.api.setvar("return", "1")
if "i" in vr("opts")["o"]:
    vr("busn", 0)
    if vr("opts")["o"]["i"] is not None:
        try:
            vr("nbus", vr("opts")["o"]["i"])
            if not vr("nbus").startswith("/dev/i2c"):
                raise RuntimeError
            vr("busn", int(vr("opts")["o"]["i"][-1:]))
        except:
            term.write("Could not parse node, using default.")
    try:
        vr("i2c", be.devices["i2c"][vr("busn")])
        from bma423 import BMA423
        vr("bma", BMA423(vr("i2c")))
        be.based.run("mknod BMA423")
        vr("node", be.api.getvar("return"))
        be.api.subscript("/bin/stringproccessing/devid.py")
        vr("bma").acc_range = 3
        be.devices["BMA423"][vr("dev_id")] = vr("bma")
        del BMA423
        dmtex("Created BMA423 sensor")
        class temp:
            def __init__(self, bma):
                self._bma = bma

            @property
            def name(self) -> str:
                return "BMA423-Temp0"
            @property
            def temperature(self) -> float:
                return float(self._bma.temperature)

        be.based.run("mknod temp")
        vr("node", be.api.getvar("return"))
        be.api.subscript("/bin/stringproccessing/devid.py")
        be.devices["temp"][vr("dev_id")] = temp(vr("bma"))
        del temp
        dmtex("Temperature sensor registered at /dev/temp" + str(vr("dev_id")))
    except:
        dmtex("Failed to create BMA423 sensor!")
        try:
            del BMA423
        except NameError:
            pass
    be.api.setvar("return", "0")
elif "d" in vr("opts")["o"]:
    if vr("dev") is not None and vr("dev").startswith("/dev/BMA423_"):
        be.based.run("rmnod " + vr("dev")[5:])
        be.api.setvar("return", "0")
    else:
        term.write("Invalid device node!")
else:
    term.write("Usage:\n    axp2101pmic -i\n    axp2101pmic -d")
