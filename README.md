<h1 align="center">S&P 500 Analysis</h1>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#reports">Reports</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#disclaimer">Disclaimer</a></li>
  </ol>
</details>

## About The Project
| Current Relational Model |
|:--:|
|![](docs/images/CurrentERD.png)|
|'Market' table references other tables via foreign keys|

## Built With
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)][python-url] <br />
[![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)][pandas-url]<br />
[![Microsoft Excel](https://img.shields.io/badge/Microsoft_Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)][excel-url]<br />
[![Power Bi](https://img.shields.io/badge/power_bi-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)][powerbi-url]

## Roadmap
- [x] Initialize DB
- [x] Update DB
- [x] Create automation script
- [ ] Generate BI reports
    - [x] FAANG + MAMAA 
        - [x] AAPL spread
        - [ ] AMZN spread
        - [ ] GOOGL spread
        - [ ] GOOG spread
        - [ ] MSFT spread
        - [ ] META spread

## Reports
| Historical Pricing Data for 2023 |
|:--:|
|![](docs/images/FAANG+MAMAAPricingData.png)|
|Displays open/close and high/low pricing data for top tech companies<br />Data can be found [HERE](Reports/FAANG+MAMAA%20Pricing%20Data.csv)|

|AAPL Pricing Spread for 2023|
|:--:|
|![](docs/images/AAPLPricingSpreadVisual.png)|
|Displays open/close and high/low pricing data for Apple Inc<br />Calculated spread can be found [HERE](Reports/AAPL%20Pricing%20Spread.csv)|

## Contact
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)][linkedin-url]<br />
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)][github-url]

## Disclaimer
Current data source limited to yfinance API. Will look to incorporate more APIs as development advances.


[python-url]: https://www.python.org/
[pandas-url]: https://pandas.pydata.org/
[excel-url]: https://www.microsoft.com/en-us/microsoft-365/excel
[powerbi-url]: https://powerbi.microsoft.com/en-us/
[linkedin-url]: https://linkedin.com/in/nicholasdagostino
[github-url]: https://github.com/nickdgas
