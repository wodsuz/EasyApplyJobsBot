import time

def writeResults(str):
    timeStr = time.strftime("%Y%m%d")
    fileName = "Applied Jobs DATA - " +timeStr + ".txt"
    try:
        with open("results/" +fileName) as file:
            lines = []
            for line in file:
                if "----" not in line:
                    lines.append(line)
                
        with open("results/" +fileName, 'w') as f:
            f.write("---- Applied Jobs Data ---- created at: " +timeStr+ "\n" )
            f.write("---- Job Title | Company | Location | Work Place | Posted Date | Applications | Result "   +"\n" )
            for line in lines: 
                f.write(line)
            f.write(str+ "\n")
    except:
        with open("results/" +fileName, 'w') as f:
            f.write("---- Applied Jobs Data ---- created at: " +timeStr+ "\n" )
            f.write("---- Job Title | Company | Location | Work Place | Posted Date | Applications | Result "   +"\n" )

            f.write(str+ "\n")


writeResults("debene")
writeResults("sis")