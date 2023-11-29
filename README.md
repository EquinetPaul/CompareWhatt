# CompareWhatt
CompareWhatt is a tool written in Python for comparing electronic and household appliances. This tool is designed to perform a comparison between several products based on their purchase cost and electricity consumption cost.

To conduct this comparison, the web application allows users to fill out a form by entering the purchase price and the theoretical annual consumption of the different products. Then, this information is used to create a graph that will visualize the total cost (purchase price + consumption) of the products over time.

Additionally, certain additional parameters allow setting important factors such as the price of electricity per kWh and its theoretical annual evolution.

Information about products (purchase price and electricity consumption) can always be found on product datasheets online or in-store (in EU btw).

### Run the code
  pip install -r requirements.txt
  python app.py
  http://127.0.0.1:5000/

### Limitations

- The unit of electrical consumption used is: kWh/annum, which corresponds to the number of kWh consumed over a year for continuous use.
- Some products (like washing machines) have different units (consumption for 100 washing cycles, for example) which can make the time-based comparison inaccurate.
- For any unit other than kWh/annum (like kWh/100 cycles, for example), it is possible to enter this value but the results should be considered inaccurate in terms of the time scale.

### Study
- The Jupyter notebook study.ipynb is a study that was conducted to evaluate the theoretical annual increase in the price of electricity paid by suppliers for a subscribed power of 6kW. The resulting value from this study can be used in the advanced settings.

### To Do
- Allow the choice of the unit of electrical consumption.
- Find the point of intersection.

### Screenshots

Screenshots demonstrate the use of the tool on three household appliances:

| Name      | Purchase Price | kWh/year |
|-----------|----------------|----------|
| Product 1 | 189            | 215      |
| Product 2 | 339            | 187      |
| Product 3 | 499            | 153      |

![img1](https://github.com/EquinetPaul/CompareWhatt/blob/main/static/images/img1.PNG?raw=true)
![img2](https://github.com/EquinetPaul/CompareWhatt/blob/main/static/images/img2.PNG?raw=true)
