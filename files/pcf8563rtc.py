rename_process("pcf8563rtc")
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
        from adafruit_pcf8563.pcf8563 import PCF8563

        vr("rtcn", PCF8563(vr("i2c")))
        del PCF8563
        be.based.run("mknod rtc")
        vr("node", be.api.getvar("return"))
        be.api.subscript("/bin/stringproccessing/devid.py")
        be.devices["rtc"][vr("dev_id")] = vr("rtcn")
        dmtex("Created PCF8563 RTC device")
    except:
        dmtex("Failed to load PCF8563 RTC!")
        try:
            del PCF8563
        except NameError:
            pass
    be.api.setvar("return", "0")
elif "c" in vr("opts")["o"] and vr("opts")["o"]["c"] is not None:
    vr("dev", vr("opts")["o"]["c"])
    vr("dev_id", None)
    if vr("dev").startswith("/dev/rtc"):
        try:
            vr("dev_id", int(vr("dev")[-1:]))
        except:
            term.write("unidentified device node!")
    if vr("dev_id") is not None:
        vr("rtc", None)
        try:
            vr("rtc", be.devices["rtc"][vr("dev_id")])
        except:
            term.write("Could not find rtc device!")
        if vr("rtc") is not None:
            vr("td", time.time() - time.mktime(vr("rtc").datetime))
            if abs(vr("td")) > 5:
                if vr("rtc").datetime_compromised or vr("td") > 0 or (vr("td") < 0 and vr("td") > -600):
                    vr("rtc").datetime = time.localtime()
                    dmtex("Updated RTC time")
                elif vr("td") < 0:
                    import rtc

                    rtc.RTC().datetime = vr("rtc").datetime
                    del rtc
                    dmtex("Restored time from RTC")
                else:
                    dmtex("Clocks up to date.")
            else:
                dmtex("Clocks up to date.")
elif "w" in vr("opts")["o"] and vr("opts")["o"]["w"] is not None:
    vr("rtc", None)
    vr("dev", vr("opts")["o"]["w"])
    if vr("dev").startswith("/dev/rtc"):
        try:
            vr("dev_id", int(vr("dev")[-1:]))
            try:
                vr("rtc", be.devices["rtc"][vr("dev_id")])
            except:
                term.write("Could not find rtc device!")
        except:
            term.write("unidentified device node!")
    if vr("rtc") is not None:
        vr("rtc").datetime = time.localtime()
        dmtex("Updated RTC time")
elif "d" in vr("opts")["o"]:
    vr("dev", vr("opts")["o"]["d"])
    if vr("dev") is not None and vr("dev").startswith("/dev/rtc"):
        be.based.run("rmnod " + vr("dev")[5:])
        be.api.setvar("return", "0")
    else:
        term.write("Invalid device node!")
else:
    term.write("Usage:\n    pcf8563rtc -i            |  load the device, optionally providing an i2c bus.\n    pcf8563rtc -c /dev/rtcX  |  Perform an automatic clock sync.\n    pcf8563rtc -w /dev/rtcX  |  Write new time data onto the rtc device.\n    pcf8563rtc -d /dev/rtcX  |  Deinit an rtc device.")
