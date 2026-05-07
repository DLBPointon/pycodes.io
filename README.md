# PyCodes.io

Code has been expanded to optionally accept a csv file (currently containing only postcodes and a second column).
  - In this case it will scan through the postcodes and return the lat/long for each one.
  - This will then be output to a csv file as `postcode,latitude,longitude,area`

Alternatively, the original function of this script is to compare the output of Postcode API's, currently this is just:
- Postcodes.io
- Doogal


## Postcodes.io
- Dockerised
    - Running on my homelab (Chunk)
    - The docker includes their PostgreSQL data dump
- Customisable
- Open Source
- Aggregates ONS data for the data
- https://postcodes.io/about
    - Data sources are frequently updated, if not then you can.
    - All sources updated recently (earliest January 2024)

## Doogle
- Centralised
- Closed source
- https://www.doogal.co.uk/PostcodeFAQ
    - Updated every 3 months for postcode data and every 10 for census
    - last update was 2021
- "Don't use the APIs for a production website/application, pay for a service that can guarantee uptime." - on the Doogal API's page
- Doesn't return alot of data on Outcodes
