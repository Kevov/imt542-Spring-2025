# imt542-Spring-2025 individual assignments
#### Code created with the help of ChatGPT

The code gets user information from a SteamID and the games they owned and exports them into 2 JSON files, one for player info and the other for game info. Run the Python file ```steam_user_info.py```

## I2 Challenges
Initially, the process of getting an API key from Steam requires that I give them a web domain, despite that the API key is tied to my Steam account. Thankfully it accepted a github webaap URL that I already have. So the process can be a little difficult for someone who has never touched web dev before.

## I3 Updates 
I have updated to include a visualization of playtime of the given user using a simple pie chart. Games with 0 playtime will not be included. The result is exported to ```playtime_chart.png```
Prerequisites: matplotlib.pyplot

## Example plot
![Example pie chart for playtime of a user!](/playtime_chart_example.png "Example plot")
