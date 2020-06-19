# COVID-19 Data Visualizations

## Inspiration

It's often hard to interpret numerical data, so we thought that it would be cool if we were able to help build an application for COVID-19 data visualization!

## What it does

Our application takes data from the COVID-19 data Github repository made available by John Hopkins and creates visualizations from line graphs to cloropleth maps to pie charts.

## How we built it

The application was made in the Dash API of Python. Initially, we did a lot of the data cleaning with pandas (in order to fit our specific structural needs) in order to get it in a usable form. After that, we set up the layout for a Dash app, made the necessary callbacks and functions, and figured out how to use Plotly and its graphing capabilities. Luckily, we did not have to use too much HTML since Dash handled a lot of that.

## Challenges we ran into

Initially we tried using Flask and matplotlib, but it was hard to make graphs that looked nice. After doing a lot of research and trying stuff out, we realized that the Dash API was the best solution.

## Accomplishments that we're proud of

Ultimately, this was our first experience using Dash, so we are proud of the final result that we got in terms of a relatively professional-looking website. It was nice to learn about Dash and all of its features, and we will be sure to use it for future projects!

## What's next for COVID-19 Data Dashboard

We will try to add more visualizations in order to make the dashboard even better and more complete! We might try to find data other than that from John Hopkins as well in order to expand this project.
