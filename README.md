git add .
git commit -m "feat: mern notes app"
git branch -M main
git remote add origin https://github.com/<you>/mern-notes-aws.git
# MERN Notes on AWS

React + Express notes app deployed on AWS: API on EC2, database on RDS Postgres, frontend on S3 (optionally CloudFront). Use this guide for the full step-by-step deployment guide and Free Tier notes.

Quick start
- Backend: set `DATABASE_URL` to your RDS endpoint, `DATABASE_SSL=true`, `CORS_ORIGIN` to your frontend URL; run `npm install && npm run dev` in `backend/`.
- Frontend: set `VITE_API_URL` to the API base (e.g., `https://<ec2-or-api-domain>/api`); run `npm install && npm run dev` in `frontend/`.
- Health check: `GET /api/health`.
