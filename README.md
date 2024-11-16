# ✈️ Flight Emissions Calculator

An interactive web application to calculate and visualize the carbon footprint of air travel. Built with Svelte, TypeScript, and Leaflet.

## 🌟 Features

- 🔍 Dynamic airport search with keyboard navigation
- 🗺️ Interactive map visualization with flight paths
- 📊 Detailed emissions calculations and comparisons
- 📱 Responsive, modern UI
- 📖 Educational context about aviation's climate impact
- 📝 Flight history tracking

## 🚀 Quick Start

```bash
# Install dependencies
bun install

# Install Python dependencies for airport data updates (optional)
cd scripts
uv pip install -r requirements.txt
cd ..

# Start development server
bun run dev
```

## 🛠️ Development

### Project Structure

```
├── public/
│   └── data/
│       └── airports.json    # Airport database
├── scripts/
│   ├── update_airports.py   # Airport data updater
│   └── requirements.txt     # Python dependencies
└── src/
    ├── lib/
    │   ├── components/      # Svelte components
    │   ├── utils/          # Utility functions
    │   └── types/          # TypeScript types
    └── App.svelte          # Main application
```

### Available Scripts

```bash
# Development
bun run dev          # Start development server
bun run build        # Build for production
bun run preview      # Preview production build

# Airport Data Management
bun run update-airports         # Update airport database
bun run update-airports:dry     # Dry run
bun run update-airports:preview # Preview with more airports
bun run update-airports:verbose # Verbose output
```

### Updating Airport Data

The airport database is compiled from OpenFlights and OurAirports data. To update:

1. Run the update script:
   ```bash
   bun run update-airports
   ```
2. Check the preview first with:
   ```bash
   bun run update-airports:dry
   ```

## 🌐 Deployment

Deploy to Cloudflare Pages:

```bash
# Build the project
bun run build

# Deploy with Wrangler
bunx wrangler pages deploy dist
```

## 🧮 Emissions Calculations

The calculator provides various comparisons to help understand flight emissions:

- 🍔 Equivalent beef burgers
- 🚗 Equivalent car kilometers
- 🚂 Equivalent train kilometers
- 🏠 Days of average household emissions

Data sources:
- Aviation emissions: International Energy Agency (IEA)
- Global flight statistics: Gössling & Humpe, 2020
- Carbon budgets: Nature Climate Change, 2020

## 🗺️ Map Features

- Interactive flight path visualization
- Great circle distance calculation
- Custom markers for airports
- Automatic zoom and centering
- Location detection support

## 🛡️ Privacy

- No user data collection
- All calculations performed client-side
- No external API dependencies
- Open-source data sources

## 🔧 Technologies

- **Frontend**: Svelte, TypeScript
- **Styling**: Tailwind CSS
- **Mapping**: Leaflet
- **Build**: Vite
- **Package Manager**: Bun
- **Data Processing**: Python (uv)

## 📄 License

MIT License - feel free to use and modify!
