# Parkinson's Detection System - Frontend

## Introduction

The frontend of the Parkinson's Detection System provides an intuitive interface for users to upload and analyze medical images for Parkinson's disease detection. It supports both MRI scans and spiral drawing tests, with real-time feedback and detailed results reporting.

## Tech Stack

- **Framework**: Next.js 15.0.3 (React)
- **Styling**: Tailwind CSS
- **Maps Integration**: Azure Maps
- **State Management**: React Hooks
- **Type Safety**: TypeScript
- **Containerization**: Docker

## Folder Structure

```
|-- Dockerfile # Docker file for the frontend
|-- README.md  # Understanding the folder and setup
|-- components.json
|-- next-env.d.ts
|-- next.config.js
|-- package-lock.json
|-- package.json
|-- postcss.config.mjs
|-- public
|-- src
| |-- app
| | |-- about
| | | `-- page.tsx
|   |   |-- drawing-scan
|   |   |   `-- page.tsx
| | |-- favicon.ico
| | |-- fonts
| | | |-- GeistMonoVF.woff
| | | `-- GeistVF.woff
|   |   |-- fonts.css
|   |   |-- globals.css
|   |   |-- hospitals
|   |   |   `-- page.tsx
| | |-- layout.tsx
| | |-- mri-scan
| | | `-- page.tsx
|   |   `-- page.tsx
| |-- components
| | |-- DynamicMap.tsx
| | |-- ParkinsonMap.tsx
| | |-- footer.tsx
| | |-- header.tsx
| | `-- ui
|   |       |-- alert.tsx
|   |       |-- button.tsx
|   |       |-- card.tsx
|   |       |-- input.tsx
|   |       `-- progress.tsx
| `-- lib
|       `-- utils.ts
|-- tailwind.config.js
|-- tailwind.config.ts
|-- tsconfig.json
`-- types
    `-- azure-maps.d.ts
```

## File Descriptions

1. **Homepage (`page.tsx`)**

   - Landing page with project introduction
   - Features overview and navigation options
   - Quick access to MRI and Drawing scan features

2. **About Page (`about/page.tsx`)**

   - Project description and mission statement
   - Links to resources and getting started guide
   - Contact information and external resources

3. **Drawing Scan Page (`drawing-scan/page.tsx`)**

   - Interface for uploading spiral drawings
   - Real-time analysis of hand-drawn spirals
   - Results display with confidence scores
   - PDF report generation for positive cases

4. **MRI Scan Page (`mri-scan/page.tsx`)**

   - MRI scan upload interface
   - Brain scan analysis functionality
   - Detailed results with confidence metrics
   - Downloadable medical reports

5. **Hospitals Page (`hospitals/page.tsx`)**

   - Interactive map showing nearby hospitals
   - Current location detection
   - List of recommended Parkinson's treatment centers
   - Distance and contact information display

6. **Layout (`layout.tsx`)**

   - Root layout component
   - Consistent header and footer across pages
   - Navigation structure
   - Global styling application

7. **Style Files**
   - `globals.css`: Global styles and Tailwind utility classes
   - `fonts.css`: Custom font imports and configurations

## Setup and Installation

1. **Local Development**

   ```bash
   # Install dependencies
   npm install

   # Run development server
   npm run dev
   ```

2. **Docker Setup**
   ```bash
   docker build -t parkinsons-ui .
   docker run -p 3000:3000 parkinsons-ui
   ```

## Key Features

- **MRI Scan Analysis**: Upload and analyze MRI scans
- **Spiral Drawing Analysis**: Process spiral drawing tests
- **Hospital Locator**: Find nearby Parkinson's treatment centers
- **Responsive Design**: Mobile-first approach
- **Real-time Feedback**: Progress indicators and instant results
- **PDF Reports**: Downloadable analysis reports

## Data Flow

1. User uploads image through UI
2. Frontend preprocesses and sends to backend
3. Displays progress indicator during analysis
4. Shows results with confidence scores
5. Offers PDF report download for positive cases

## Environment Variables

NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_PRIMARY_KEY=your_azure_maps_key
NEXT_PUBLIC_SECONDARY_KEY=your_azure_maps_secondary_key

## Styling

- Tailwind CSS for utility-first styling
- Custom components using shadcn/ui
- Responsive design breakpoints
- Dark mode support
- Custom animations and transitions

## Dockerization

Multi-stage build process:

1. Builder stage: Compiles Next.js application
2. Production stage: Serves optimized build
3. Environment variable handling
4. Static file optimization

## Building

### Production Build

```bash
npm run build
npm start
```

## Future Enhancements

- [ ] Add user authentication
- [ ] Implement result history
- [ ] Enhanced visualization of analysis results
- [ ] Multiple language support
- [ ] Progressive Web App capabilities
