# Resume Screening Angular Frontend

## Setup Instructions

1. Install Node.js and npm
2. Install Angular CLI:
   ```bash
   npm install -g @angular/cli
   ```

3. Install dependencies:
   ```bash
   npm install
   ```

4. Run development server:
   ```bash
   ng serve
   ```

5. Navigate to `http://localhost:4200/`

## Project Structure

- `src/app/components/` - UI components
- `src/app/services/` - API services
- `src/environments/` - Environment configuration

## Features

- Resume upload interface
- Real-time screening results
- Candidate management dashboard
- Analytics visualization

## API Integration

Configure backend URL in `src/environments/environment.ts`:
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000'
};
```
