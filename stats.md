P1 = __ATGATG__

P2 = __CTCTCTA__

P3 = __TCACTACTCTCA__

Stats after using slow suffix array on Canis lupus familiaris genom (approx 120mil. characters)

| Cut size | Time per cut | Total time |
| ---------|--------------|------------|
| 10^2     |   ~    | ~      |
| 10^3     |   ~    | ~      | 
| 10^4     |   ~     |  ~     |
| 10^5     |   ~     |  ~    |

Stats after using fast suffix array on Canis lupus familiaris genom

| Cut size | Total memory | Total time | Total matches|
| ---------|--------------|------------|-------------------|
| 10^2     |   ~    | ~      | |
| 10^3     |   ~    |  ~     | |
| 10^4     |   ~296MB     |  ~230s   | P1: 39975, P2: 11242, P3: 7 |
| 10^5     |   ~    |  ~     | |
| 10^6     |   ~      |  ~    ||
| 10^7     |   ~       |  ~    ||
| 10^8     |   ~      |  ~     ||
