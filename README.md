
# MERN Notes on AWS

React + Express notes app deployed on AWS: API on EC2, database on RDS Postgres, frontend on S3 (optionally CloudFront). Use this guide for the full step-by-step deployment guide and Free Tier notes.
For more Info: 
https://app.notion.com/p/Deploying-a-Full-Stack-Notes-App-to-AWS-DevOps-Lab-3860f6c540d28150b5bfeea3713d9f90?pvs=12

Quick start
- Backend: set `DATABASE_URL` to your RDS endpoint, `DATABASE_SSL=true`, `CORS_ORIGIN` to your frontend URL; run `npm install && npm run dev` in `backend/`.
- Frontend: set `VITE_API_URL` to the API base (e.g., `https://<ec2-or-api-domain>/api`); run `npm install && npm run dev` in `frontend/`.
- Health check: `GET /api/health`.
