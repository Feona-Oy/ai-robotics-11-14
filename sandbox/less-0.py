from rover_sim import Rover
 
 
def mission(drift):
    """ run to the red marker and take if the sample """
    r = Rover(x=4, y=2, heading=0, drift=drift)     # x,y: coordinates, heading: degrees, drift: degrees per step
 
    try:
        for _ in range(10):      # 10 small steps forward
            r.forward(1)
        r.turn_right(90)
        r.forward(1)
        r.collect_sample()
    except RuntimeError:
        pass                     # rover lost, mission lost
 
    r.show()
 
    if not r.alive:
        status = "ROVER LOST"
    elif r.samples:
        status = "Sample collected"
    else:
        status = "Lost sample"
    print(f"Drift {drift}   ->   {status}")
 
 
# ↓↓↓ Change just this number ↓↓↓
mission(drift=10)
