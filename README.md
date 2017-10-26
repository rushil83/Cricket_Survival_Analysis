# Survival Analysis In Sports

Pulled the data using `BeautifulSoup` of all cricket players, and created the model for predicting probability of career length of a given player
(i.e. player with more than 8k runs have 90% probability of 12yrs career length)

## some Application of survival analysis

There are four major applications of survival analysis into `analytics`:
- Business Planning : Profiling customers who has a higher survival rate and make strategy accordingly.
- Lifetime Value Prediction : Engage with customers according to their lifetime value
- Active customers : Predict when the customer will be active for the next time and take interventions accordingly.
- Campaign evaluation : Monitor effect of campaign on the survival rate of customers.

Following are some `industrial` specific applications of survival analysis
- Banking – customer lifetime and LTV
- Insurance – time to lapsing on policy
- Mortgages – time to mortgage redemption
- Mail Order Catalogue – time to next purchase
- Retail – time till food customer starts purchasing non-food
- Manufacturing – lifetime of a machine component
- Public Sector – time intervals to critical events


# Cricket Survival Analysis

Here we are plotting 3 graphs (https://goo.gl/photos/y8Fq4eR2VqDPiGSL7) 
First we will pulled our data and fetch them in the correct data format for modeling graphs
For this data we have created 3 graphs but similarly you can create many different statistically related graphs. 

- Country(players) vs career length = this graph tells us about what are the probability of that countrys players
to survive the specific career length
- strike rate vs career length
- runs vs career length
