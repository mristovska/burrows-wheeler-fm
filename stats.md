P1 = "ATGATG"
P2 = "CTCTCTA"
P3 = "TCACTACTCTCA"

Stats after using slow suffix array on Canis lupus familiaris genom (approx 120mil. characters)

| Cut size | Time per cut | Total time |
| ---------|--------------|------------|
| 10^2     |   ~    | ~      |
| 10^3     |   ~    | ~      | 
| 5 * 10^3 |   ~    |  ~    |
| 10^4     |   ~     |  ~     |
| 5 * 10^4 |   ~      |  ~    |
| 10^5     |   ~     |  ~    |

Stats after using fast suffix array on Canis lupus familiaris genom

| Cut size | Avg time per cut | Total time | Total matches|
| ---------|--------------|------------|-------------------|
| 10^2     |   ~    | ~      | |
| 10^3     |   ~    |  ~     | |
| 5 * 10^3 |   ~     |  ~     | |
| 10^4     |   ~0.03s    |  ~360s   | P1: 39975, P2: 11242 |
| 5 * 10^4 |   ~     |  ~     | |
| 10^5     |   ~    |  ~     | |
| 10^6     |   ~ 4.8s     |  ~615s    ||
| 10^7     |   ~       |  ~    ||
| 10^8     |   ~      |  ~     ||
