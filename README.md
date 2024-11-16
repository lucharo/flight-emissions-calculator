# ✈️ Flight Emissions Calculator

An interactive web application to calculate and visualize the carbon footprint of air travel.
Built with the [Windsurf IDE](https://codeium.com/windsurf).

## What is this?

Should we never take flights again? Some people think so and they feel guilty in the occasions they have to travel.

I once was travelling from London to Madrid and thought to calculate my emissions for it. Emission units are not intuitive to anybody (kgCO2), so I thought I wanted to compare it to emission from beef burgers or alternative transports methods. I wanted it an app that could do this repeatedly, so I built it with the help of the [Windsurf IDE](https://codeium.com/windsurf) which felt like pure magic to be honest. I'm not sure I would have ever put this project out if it wasn't for it. I started project many months prior to writing this but I left in a stale state given my lack of previous experience with web development. With Windsurf I was able to resurrect the project and bring it life in half a working day.

I think individualising the problem of climate change only takes us so far and that truly we need systemic changes if we want things to happen. Eat your veggies, travel by train if you can afford it but truly the most we can do to reduce our carbon footprint is to take on political solutions.

## Quick Start

```bash
# Install dependencies
bun install

# Start development server
bun run dev

# Build for production
bun run build
```

## Data Sources

- Airport data: OpenFlights and OurAirports
- Traffic data: [ACI World Airport Traffic Report (2021)](https://aci.aero/2022/07/25/final-data-released-top-20-busiest-airports-confirmed/)
- Emissions data: [Dolšak & Prakash, 2022](https://doi.org/10.1007/s44168-022-00001-w)

## Documentation

- [Design Overview](DESIGN.md)
- [Data Update Scripts](scripts/README.md)
