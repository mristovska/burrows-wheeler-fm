P1 = __ATGATG__

P2 = __CTCTCTA__

P3 = __TCACTACTCTCA__

Stats after using slow suffix array on Canis lupus familiaris genom (approx 120mil. characters)

| Cut size | Total memory (MB) | Total time (s) | Total matches|
| ---------|--------------|------------|--------------------|
| 10^2     |   ~    | ~      |
| 10^3     |   ~    | ~      | 
| 10^4     |   ~284     |  ~620     |P1: 39975, P2: 11242, P3: 7 |
| 10^5     |   ~     |  ~    |

Stats after using fast suffix array on Canis lupus familiaris genom

| Cut size | Total memory (MB) | Total time (s) | Total matches|
| ---------|--------------|------------|-------------------|
| 10^2     |   ~297   | ~270       |P1: 39975, P2: 11242, P3: 7 |
| 10^3     |   ~296    |  ~220     |P1: 39975, P2: 11242, P3: 7 |
| 10^4     |   ~296     |  ~230    |P1: 39975, P2: 11242, P3: 7 |
| 10^5     |   ~298  |  ~270       | P1: 39975, P2: 11242, P3: 7 |
| 10^6     |   ~301      |  ~430   |P1: 39975, P2: 11242, P3: 7 |

