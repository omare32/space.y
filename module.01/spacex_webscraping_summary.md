# SpaceX Web Scraping Summary

Generated: 2025-08-26T12:04:31

## Dataset Shape
Rows: 121, Columns: 12

## Head (first 5 rows)
```
 Flight No. Launch site                                Payload Payload mass Orbit      Customer Launch outcome  Version Booster Booster landing       Date  Time  Payload mass (kg)
          1       CCAFS   Dragon Spacecraft Qualification Unit            0   LEO        SpaceX        Success F9 v1.07B0003.18         Failure 2010-06-04 18:45                NaN
          2       CCAFS      Dragondemo flight C1(Dragon C101)            0   LEO NASA(COTS)NRO        Success F9 v1.07B0004.18         Failure 2010-12-08 15:43                NaN
          3       CCAFS Dragondemo flight C2+[18](Dragon C102)       525 kg   LEO    NASA(COTS)        Success F9 v1.07B0005.18      No attempt 2012-05-22 07:44              525.0
          4       CCAFS          SpaceX CRS-1[22](Dragon C103)     4,700 kg   LEO     NASA(CRS)        Success F9 v1.07B0006.18      No attempt 2012-10-08 00:35             4700.0
          5       CCAFS          SpaceX CRS-2[22](Dragon C104)     4,877 kg   LEO     NASA(CRS)        Success F9 v1.07B0007.18      No attempt 2013-03-01 15:10             4877.0
```

## Missing Values by Column
```
Flight No.           0
Launch site          0
Payload              0
Payload mass         0
Orbit                0
Customer             0
Launch outcome       0
Version Booster      0
Booster landing      0
Date                 0
Time                 0
Payload mass (kg)    5
```

## Numeric Columns Summary (describe)
```
       Flight No.  Payload mass (kg)
count  121.000000         116.000000
mean    61.000000        7401.681034
std     35.073732        5342.154139
min      1.000000         362.000000
25%     31.000000        3122.500000
50%     61.000000        5235.500000
75%     91.000000       13155.000000
max    121.000000       15600.000000
```

## Value Counts — Orbit
```
Orbit
LEO            67
GTO            33
SSO             7
Polar           7
MEO             3
HEO             2
Polar orbit     1
Sub-orbital     1
```

## Value Counts — Launch site
```
Launch site
CCAFS             40
KSC               33
Cape Canaveral    20
VAFB              16
CCSFS             12
```

## Value Counts — Launch outcome
```
Launch outcome
Success    120
Failure      1
```

## Value Counts — Version Booster
```
Version Booster
F9 B5               19
F9 FT[              17
F9 v1.1[             9
F9 B5[               7
F9 B4[               7
F9 v1.1              5
F9 B5 ♺[             5
F9 B5 ♺              5
F9 v1.07B0007.18     1
F9 v1.07B0006.18     1
```

