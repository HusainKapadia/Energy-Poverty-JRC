# Server-side code of Enershare
``main.py`` constains all the server-side code for the data shown on the front end application. All jupyter-notebooks are used for prototyping and testing ideas and models before deploying it on the server.

# Energy-Poverty-JRC
Requirements and datasets for Energy Poverty Challenge from Space4Good and the European Commission JRC.


## Requirements
The energy platform should meet the following requierements (from Technical Annex by JRC):
1.	Marketplace: Enable and register transfers of energy between different private producers, other community consumers and people in need (energy poverty candidates).
2.	Inventory: Up-to-date inventory of renewable energy production units (solar, wind, etc.), the quality of the power supply.
3.	Potential: Estimate the potential for renewable energy production based on satellite technologies (solar energy).
4.	Weather variations: Anticipate energy variations (surpluses, deficits) deriving from changing weather conditions affecting the renewable sources (e.g. solar photovoltaic, wind). 
5.	Demand-based Advice: Advice and/or manage the demand based on those estimations (potential and variations) for the sake of optimizing the energy supply to those in need.

**Comments:**

Regarding point 1, energy poverty candidates will register as such in the platform (check a box). For now, don’t focus on verification of who qualifies as an energy poverty canditate. 

Regarding point 2, the platform will count the # of solar panels based on the users (producers) that are registered to the platform. No pre-existing datasets of current solar panels in a city will be included to the platform. 

Regarding point 3, the theoretical solar production potential will serve as a reference point/benchmark to understand the marketplace dynamics i.e. how the market moves in terms of prices and energy security. This potential can already be provided by existing datasets (see section on PVGIS) so no calculation needed, just integration and connection with marketplace is needed.

Point 4 is the forecast of energy variations. Machine learning algorithms that detect how weather conditions affect the production and consumption of energy. The forecast of actual energy produced will then be fed to the theoretical production potential (point 3), so the algorithm learns from it.

Regarding point 5, the computer shouldn’t automatically transfer energy between prosumers. Instead, recommendations should be made to users (producers) and platform admin regarding: Who to distribute to? When can the transfer can happen (holidays, for cooking needs @6pm)? Energy poverty donations when there is energy surplus? 




### Climate/Weather data Amsterdam
Useful for point 4-*weather variations*. Climate and weather data produced by [Dutch PV Portal by TU Delft](https://www.tudelft.nl/en/eemcs/the-faculty/departments/electrical-sustainable-energy/photovoltaic-materials-and-devices/dutch-pv-portal/) based on measurements by the Koninklijk Nederlands Meteorologisch Instituut (KNMI).

**Climate Data:** Climate dataset for Amsterdam (closest KNMI station in Schiphol). A dataset of one year constructed from weather data averaged over a multitude of years (1991-2018), with a one hour time resolution. Displays the average hourly values of weather parameters: irradiation, temperature, wind, cloud, pressure, rainfall, irradiance, elevation, azimuth. The climate database is dynamically updated. Every hour, the hourly average of the real-time weather measurements is added to the climate database by making a weighted average with the climate parameter values in the historical database.

**Weather data**: the weather of today and yesterday with a 10-minute time resolution. Not provided in this repository. Head over to the [Dutch PV website](https://www.tudelft.nl/en/eemcs/the-faculty/departments/electrical-sustainable-energy/photovoltaic-materials-and-devices/dutch-pv-portal/) to download the data relevant for today.
