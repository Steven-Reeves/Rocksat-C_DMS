/Temperature/ {print $1","$3 >> "temp.txt"}
/Pressure/ {print $1","$3 >> "pressure.txt"} 
/altitude/ {print "Altitude,"$4 >> "altitude.txt"}
