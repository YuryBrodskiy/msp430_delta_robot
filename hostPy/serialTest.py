from DeltaDriver import DeltaDriver 

def main():
    with DeltaDriver('',[0,0,0],[90,90,90],[900,900,900],[1800,1800,1800]) as delta:
        delta.calibrate([0,0,0])
        delta.setTimes([20,20,20])

if __name__ == "__main__":
    main()

