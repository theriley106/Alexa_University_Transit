# Alexa University Transit

## API Endpoints

<a href="http://192.168.2.106:8000">
test
</a>

https://feeds.transloc.com/3/routes?agencies={agencyID}

https://feeds.transloc.com/3/vehicle_statuses?agencies={agencyID}

https://feeds.transloc.com/3/stops?agencies={agencyID}

https://feeds.transloc.com/3/announcements?agencies={agencyID}

## Transit Wrapper Functionality


```python
self.agencyNum
# This is the agency number that for the bus route
```

```python
self.agencyInfo
# This contains info on all Transloc bus routes
```

```python
self.getSpecificInfo
# This contains info relevant to the inputted agency ID
```

```python
self.longitude
# This refers to the inputted/randomly generated longitude
```

```python
self.latitude
# This refers to the inputted/randomly generated latitude
```

```python
self.busName
# This refers to the short name of the bus system.  Ie: yale, catbus, etc.
```

```python
self.busNumber
# This ALSO refers to the agencyNum...
```

```python
self.listOfStops
# This refers to the list of stops used in this route.
```

```python
self.allInfo
# This is a python dict containing all information about this bus system
```

```python
self.listOfRoutes
# This is a list of python dictionaries containing info on all routes in this bus system
```

```python
self.nearbyRoutes
# This returns all routes where self.longitude and self.latitude are within the listed bounds
```

```python
self.activeRoutes
# This returns a list of python dictionaries containing info on all bus routes that are currently in service for this agencyID
```

```python
self.activeVehicles
# This returns a list of python dictionaries containing info on all vehicles that are currently running
```

```python
self.announcements
# Returns a list of strings containing current announcements for this bus system
```

```python
self.stopDatabase
# This returns a list of python dictionaries containing info for all stops in this bus system
```

```python
self.stopName
# This returns info on either the closest stop or the default stop
```

```python
self.stopNumber
# This returns info on either the closest stop or the default stop
```

```python
self.stopNumber
# This returns the code for either the closest stop or the default stop
```

```python
self.notifcationCount
# Refers to the amount of unread notifications
```

```python
self.returnClosestStopsNames(n)
# Returns the n nearest stops to self.longitude and self.latitude
```

```python
self.generateRandomLongitude()
# This will regenerate self.longitude and self.latitude
```

```python
self.getArrivalTimes()
# This returns arrival times for the closest bus
# This will likely be removed soon, this is an additional API call
# that can be replaced by comparing values in self.allInfo
```

## Sample Utterances

"What busses are running right now?"

"Where is the nearest stop?"

"How far is the bus"

"What time will the bus be here?"

"Set a default bus"

"What time will the {busName} be here"

"How fast is the {busName} going"

"Is the bus running today?"

"When will the bus be here?"

"How far away is the bus?"

"Am I going to miss the bus?"

"Where is the bus right now?"

"Are there any announcements?"

## Supported Schools

- Adelphi University
- Alabama A&M University
- Atlantic Station Shuttles
- Auburn University
- Ball State University
- Beck Bus-Southern Illinois University, Carbondale
- Biola University
- Boston Children’s Hospital
- Boston College
- Boston University
- Bowling Green State University
- Brandeis University
- Brown University
- Bucknell University
- Burlington Transit
- Capitol Corridor Joint Powers Authority
- Cary Transit
- Central Midlands Transit-The Comet
- Cerritos on Wheels
- Chapel Hill Transit
- Chapman University
- Children’s Healthcare of Atlanta
- City of Airdrie
- City of Fayetteville (Fayetteville Area System Transit)
- City of Gainesville-Regional Transit System
- Clemson Area Transit
- Colgate University
- Columbia University
- Cornish College of the Arts
- Corpus Christi Regional Transportation Authority
- County of Maui – Transportation Department
- Duke University
- East Carolina University
- Eastern Connecticut State University
- Emory University
- Fairfield University
- Florida Agricultural and Mechanical University
- Florida International University
- Florida State University
- Fordham University
- University of Alabama at Birmingham
- University of Tennessee
- Georgetown University
- Georgia College and State University
- Georgia State University
- GoDurham
- GoRaleigh
- GoTriangle
- Greensboro Transit Authority
- Harvard University
- High Point University
- Independence Transit
- Jacksonville Transit
- Jacksonville University
- Johns Hopkins Bayview Medical Center
- Johns Hopkins Medical Institute
- Johns Hopkins University
- Johnson & Wales University
- Johnson & Wales University: North Miami Campus
- Kennesaw State University
- Lamar University
- Lawrence Technological University
- Lexington Transit Authority
- Life University
- Louisiana State University
- Mansfield University
- Martha’s Vineyard Transit Authority
- MASCO
- Memphis Area Transit Authority
- Mercer University
- Monona Express
- Montgomery County Community College
- Morgan State University
- Nantucket Regional Transit Authority
- New Jersey City University
- New Mexico DOT
- New York University
- North Carolina State University
- North Carolina State University – College of Engineering
- Northern Arizona University
- Northwestern University
- NYU Langone Medical Center
- Oakland University
- Penn State Hershey Medical Center
- Philadelphia University
- Piedmont Authority for Regional Transportation
- Playa Vista Parks & Landscape Corporation
- Princeton University
- University of New Haven
- Quinnipiac University
- Rhode Island College
- Rhode Island School of Design
- Robert Morris University
- Robert W. Woodruff Library, Atlanta University Center
- Rochester Institute of Technology
- Rock Island County Metropolitan Mass Transit District (MetroLINK)
- Rowan University
- San Jose International Airport
- Santa Clara Valley Transportation Authority
- Savannah College of Art & Design
- Savannah College of Art & Design – Atlanta
- Southern Illinois University, Carbondale
- StarMetro
- Stevens Institute of Technology
- Swarthmore College
- Texas Christian University
- The M Transit System
- The Pennsylvania State University-Main Campus
- The University of Alabama, Tuscaloosa
- The University of Alabama at Birmingham
- The University of Arizona
- The University of Chicago
- The University of Maryland, Baltimore County
- The University of Texas at Arlington
- The University of Toledo
- The University of Vermont
- Troy University
- Tuscaloosa Transit Authority (TTA)
- UF Health Shands Hospital – UFL
- United States Military Academy
- University of Iowa
- University of Kentucky
- University of Maryland-College Park
- University of Massachusetts Boston
- University of Memphis
- University of New Haven
- University of North Alabama
- University of North Carolina at Chapel Hill
- University of North Florida
- University of Rochester
- University of South Carolina-Columbia
- University of Tennessee
- University of Virginia
- University of Western Sydney
- University of West Florida Main Campus
- University of Wyoming
- Virginia Commonwealth University
- Wake Forest University
- Widener University
- Yale University
