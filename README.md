# Consulting Analytics Lab

I started this project to practise using numbers to answer business questions. I am combining consulting-style cases with analysis of public datasets in one repository, instead of making a separate project for each one.

I am still building it. At the moment, the first calculation helpers and their tests are in place. The case files are examples of how I want to organise the work; they are not all connected to a full analysis runner yet.

## What I want to work on

- Profitability: revenue, costs, contribution margin and break-even.
- Market entry: make assumptions visible and compare a few possible outcomes.
- Operational efficiency: measure a simple problem before suggesting a change.
- Public-data analysis: choose a real dataset, record where it came from and explain what it can and cannot tell us.
- Later, I want to add a pharma operations case for inventory, expiry risk, supplier performance and working capital. That will be an extension of this project, not a separate analytics engine.

## Current folder layout

~~~text
src/analytics_lab/       Small calculation helpers
tests/                   Unit tests for the calculations
cases/                   Case questions and assumptions
docs/                    Notes about sources and calculations
.github/workflows/       Automated test run
~~~

## Run the tests

The current calculation helpers use the Python standard library, so no extra packages are needed for this first part.

~~~bash
python -m unittest discover -s tests -v
~~~

## How I plan to use data

I will start with small examples that I can check by hand. For the public-data part, I will record the original source, download date, units, missing values and any changes I make to the data. I do not want to present made-up data as real findings.

Any example numbers in the case files are fictional and are only there to test the calculations. A scenario result is not a promise of what a real company would achieve.

## What this project is not

This is a student learning project, not a consulting firm's toolkit. It will not automatically find a perfect answer or replace checking the assumptions. I want each result to be simple enough that I can explain how it was calculated and why I used it.

I am keeping the first version small so I can understand the calculations and improve them as I go.
