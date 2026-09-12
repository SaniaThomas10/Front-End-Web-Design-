# WWE Match Explorer

## Project Rationale

I chose the WWE match history dataset because I love watching WWE and wanted to work with a dataset that I would actually enjoy exploring. The dataset contains information about matches, including the event, date, winner, loser, and whether the match was a title match. I wanted to use the dataset to explore different wrestlers' statistics, such as their wins and losses, and see how their stats compare across different WWE events. I thought it would be interesting to see how different wrestlers perform throughout the events included in the dataset.

One limitation of the dataset is that it only covers a specific time period of WWE history. Because of this, the statistics and trends in the dataset may not represent a wrestler's entire career or WWE history overall. A wrestler could have more wins or losses outside of the time period included in the dataset.

I chose the summary metrics because they help describe the data after filters are applied. Matches Shown tells me how many matches fit the current filters, Opponents Shown shows the different wrestlers who are part of the matches being displayed, and Title Matches shows how many of the filtered matches were title matches.

For the charts, I chose a horizontal Altair bar chart because it makes it easy to compare title and non-title matches across different WWE events, compared to the vertical bar chart. I chose a Plotly pie chart for wrestler wins and losses because it gives a simple visual representation of a wrestler's match results.

## Features

- Event filtering
- Wrestler search
- Title match filtering
- Sorting
- Match statistics
- Charts

## Technologies Used

- Python
- Streamlit
- Pandas
- Altair
- Plotly

## Dataset

Kaggle WWE match history dataset containing 1,000 matches, between 12/31/2022 - 11/4/2023

