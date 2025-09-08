# Frontend (AetherNotes)

This is the React + TypeScript frontend built with Vite.

## Setup

```bash
cd frontend
npm install
npm run dev

## Authentication Flow

- **Email OTP Login**
  - `/auth/otp/request` → Request OTP via email
  - `/auth/otp/verify` → Verify OTP, receive JWT

- **Google OAuth Login**
  - `/auth/google/login` → Redirects to Google for sign-in
  - `/auth/google/callback` → Handles Google callback and returns JWT

### Usage
1. Run the backend (`http://localhost:8000`).
2. Run the frontend (`npm run dev`).
3. Go to `/login` to test OTP or Google login.