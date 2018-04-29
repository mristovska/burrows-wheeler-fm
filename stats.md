P1 = __ATGATG__

P2 = __CTCTCTA__

P3 = __TCACTACTCTCA__

# Canis lupus familiaris genom 1st chromosome (approx 120mil. characters)

## Slow suffix array  

| Cut size | Total memory (MB) | Total time (s) | Total matches|
| ---------|--------------|------------|--------------------|
| 10^2     |   ~284    | ~ 280    |P1: 39975, P2: 11242, P3: 7 |
| 10^3     |   ~284   | ~ 230     | P1: 39975, P2: 11242, P3: 7 |
| 10^4     |   ~284     |  ~620     |P1: 39975, P2: 11242, P3: 7 |
| 10^5     |      |  ~4270   |P1: 39975, P2: 11242, P3: 7 |
| 10^6     |      | too much   | |

## Fast suffix array 

| Cut size | Total memory (MB) | Total time (s) | Total matches|
| ---------|--------------|------------|-------------------|
| 10^2     |   ~297   | ~270       |P1: 39975, P2: 11242, P3: 7 |
| 10^3     |   ~296    |  ~220     |P1: 39975, P2: 11242, P3: 7 |
| 10^4     |   ~296     |  ~230    |P1: 39975, P2: 11242, P3: 7 |
| 10^5     |   ~298  |  ~270       | P1: 39975, P2: 11242, P3: 7 |
| 10^6     |   ~301      |  ~430   |P1: 39975, P2: 11242, P3: 7 |


# Phoenix dactylifera genome (approx 555mil. characters)

## Slow suffix array

## Fast suffix array

| Cut size | Total memory (MB) | Total time (s) | Total matches|
| ---------|--------------|------------|-------------------|
| 10^3     |   ~1800     |  ~1150   |P1: 270956, P2: 43926, P3: 44|
| 10^4     |   ~1800     |  ~1200   |P1: 270956, P2: 43926, P3: 44|
| 10^5     |   ~1800     |  ~1400   |P1: 270956, P2: 43926, P3: 44|
| 10^6     |   ~1800     |  ~2200   |P1: 270956, P2: 43926, P3: 44|
