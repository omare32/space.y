# SpaceX Data Collection Summary

Generated: 2025-08-26T11:52:48

## Dataset Shape
Rows: 90, Columns: 17

## Date Range
2010-06-04 to 2020-11-05

## Head (first 5 rows)
```
 FlightNumber       Date BoosterVersion  PayloadMass Orbit   LaunchSite     Outcome  Flights  GridFins  Reused  Legs LandingPad  Block  ReusedCount Serial   Longitude  Latitude
            1 2010-06-04       Falcon 9  6123.547647   LEO CCSFS SLC 40   None None        1     False   False False       None    1.0            0  B0003  -80.577366 28.561857
            2 2012-05-22       Falcon 9   525.000000   LEO CCSFS SLC 40   None None        1     False   False False       None    1.0            0  B0005  -80.577366 28.561857
            3 2013-03-01       Falcon 9   677.000000   ISS CCSFS SLC 40   None None        1     False   False False       None    1.0            0  B0007  -80.577366 28.561857
            4 2013-09-29       Falcon 9   500.000000    PO  VAFB SLC 4E False Ocean        1     False   False False       None    1.0            0  B1003 -120.610829 34.632093
            5 2013-12-03       Falcon 9  3170.000000   GTO CCSFS SLC 40   None None        1     False   False False       None    1.0            0  B1004  -80.577366 28.561857
```

## Missing Values by Column
```
FlightNumber       0
Date               0
BoosterVersion     0
PayloadMass        0
Orbit              0
LaunchSite         0
Outcome            0
Flights            0
GridFins           0
Reused             0
Legs               0
LandingPad        26
Block              0
ReusedCount        0
Serial             0
Longitude          0
Latitude           0
```

## Numeric Columns Summary (describe)
```
       FlightNumber   PayloadMass    Flights      Block  ReusedCount   Longitude   Latitude
count     90.000000     90.000000  90.000000  90.000000    90.000000   90.000000  90.000000
mean      45.500000   6123.547647   1.788889   3.500000     3.188889  -86.366477  29.449963
std       26.124701   4732.115291   1.213172   1.595288     4.194417   14.149518   2.141306
min        1.000000    350.000000   1.000000   1.000000     0.000000 -120.610829  28.561857
25%       23.250000   2510.750000   1.000000   2.000000     0.000000  -80.603956  28.561857
50%       45.500000   4701.500000   1.000000   4.000000     1.000000  -80.577366  28.561857
75%       67.750000   8912.750000   2.000000   5.000000     4.000000  -80.577366  28.608058
max       90.000000  15600.000000   6.000000   5.000000    13.000000  -80.577366  34.632093
```

## Value Counts — Orbit
```
Orbit
GTO      27
ISS      21
VLEO     14
PO        9
LEO       7
SSO       5
MEO       3
HEO       1
ES-L1     1
SO        1
```

## Value Counts — LaunchSite
```
LaunchSite
CCSFS SLC 40    55
KSC LC 39A      22
VAFB SLC 4E     13
```

## Value Counts — Outcome
```
Outcome
True ASDS      41
None None      19
True RTLS      14
False ASDS      6
True Ocean      5
False Ocean     2
None ASDS       2
False RTLS      1
```

## Value Counts — BoosterVersion
```
BoosterVersion
Falcon 9    90
```

