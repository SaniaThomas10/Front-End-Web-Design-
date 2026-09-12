# WWE Match Explorer

## Project Rationale

I chose the WWE match history dataset because I am interested in WWE and wanted to work with a dataset that I would actually enjoy exploring. The dataset contains information about matches, including the event, date, winner, loser, and whether the match was a title match. One question I wanted to explore was whether certain WWE events have more title matches than others. I also wanted to be able to search for a wrestler and see their wins and losses.

One limitation of the dataset is that it does not include much detail about what happened during each match. For example, it does not include match length, how the match ended, or specific championship information. This means the dataset is useful for looking at basic match patterns, but it cannot explain everything about why a match had a certain result.

I chose the summary metrics because they help describe the data after filters are applied. **Matches Shown** tells me how many matches fit the current filters, **Unique Winners** shows how many different wrestlers won, and **Title Matches** shows how many filtered matches were title matches.

For the charts, I chose a **horizontal Altair bar chart** because it makes it easy to compare title and non-title matches across different WWE events. I chose a **Plotly pie chart** for wrestler wins and losses because it clearly shows the proportion of a wrestler's wins compared to their losses.

## Features

- Event filtering
- Wrestler search
- Title match filtering
- Sorting
- Match statistics
- Interactive charts

## Technologies Used

- Python
- Streamlit
- Pandas
- Altair
- Plotly

## Dataset

WWE match history dataset containing 1,000 matches.

## How to Run

```bash
streamlit run app1.py
