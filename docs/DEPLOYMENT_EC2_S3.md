# Deployment Documentation: AWS EC2 + S3 (FastAPI)

This guide provides a full, end-to-end deployment workflow for the FastAPI backend on AWS EC2, with ML model artifacts stored in S3 and synced during deploy. It also includes GitHub Actions CI/CD, systemd service setup, security, rollback, and troubleshooting.

## Contents
1. Architecture Overview
2. Prerequisites
3. AWS Setup
4. EC2 Instance Setup
5. Repository Setup on EC2
6. Environment Configuration
7. Systemd Service Setup
8. GitHub Actions CI/CD
9. Model Delivery via S3
10. Verification
11. Rollback
12. Monitoring and Logs
13. Security Checklist
14. Cost Notes
15. Optional: Nginx + HTTPS
16. Troubleshooting

---

## 1) Architecture Overview
- EC2 runs FastAPI via Uvicorn and systemd
- Models are stored in S3 and synced to EC2 during deploy
- GitHub Actions connects to EC2 over SSH to trigger deploy

---

## 2) Prerequisites
- AWS account with permissions for EC2, S3, IAM
- GitHub repository for this project
- A local SSH key for GitHub Actions (private key stored as a secret)
- MongoDB (local or Atlas)

---

## 3) AWS Setup
### 3.1 Create S3 bucket for models
- Example bucket: `research-models-prod`
- Upload model folder to `final_sinhala_mood_model/`
- Folder should contain model files required by `transformers` (config, tokenizer, weights)

### 3.2 Create EC2 instance
- Recommended: Ubuntu 22.04 LTS, t3.medium or larger (ML deps)
- Security Group:
  - SSH 22 from your IP or GitHub Actions IP ranges
  - App port 8000 (or 80/443 if using Nginx)

### 3.3 IAM role for EC2
Attach an IAM role to EC2 with read access to the S3 bucket.

Example policy:
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": ["arn:aws:s3:::research-models-prod"]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::research-models-prod/*"]
    }
  ]
}
```

---

## 4) EC2 Instance Setup
SSH into your instance and run:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git awscli

sudo mkdir -p /srv/research-backend
sudo chown -R ubuntu:ubuntu /srv/research-backend
```

---

## 5) Repository Setup on EC2
### Option A: Deploy key (recommended)
1. On EC2, generate a deploy key:
   ```bash
   ssh-keygen -t ed25519 -C "ec2-deploy" -f ~/.ssh/research_backend
   ```
2. Add the public key (`~/.ssh/research_backend.pub`) to GitHub as a Deploy Key with read access.
3. Add SSH config:
   ```bash
   cat >> ~/.ssh/config << 'EOF'
   Host github.com
     IdentityFile ~/.ssh/research_backend
     StrictHostKeyChecking no
   EOF
   ```
4. Clone the repo:
   ```bash
   cd /srv/research-backend
   git clone git@github.com:DhanukaNavodya/Research_Project_Backend.git .
   ```

---

## 6) Environment Configuration
Create `/srv/research-backend/.env`:

```
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=research_db
JWT_SECRET=replace-me
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
FROM_EMAIL=
FRONTEND_BASE_URL=http://localhost:3000
BACKEND_BASE_URL=http://<your-ec2-ip>:8000
BAD_MOOD_THRESHOLD=5
```

---

## 7) Systemd Service Setup
Use the template provided in the repo.

```bash
sudo cp /srv/research-backend/deploy/research-backend.service /etc/systemd/system/research-backend.service
sudo systemctl daemon-reload
sudo systemctl enable research-backend
sudo systemctl start research-backend
sudo systemctl status research-backend
```

---

## 8) GitHub Actions CI/CD
### 8.1 Workflow file
The workflow is in `.github/workflows/deploy-ec2.yml`.
It runs on every push to `main` and executes `scripts/ec2_deploy.sh` on EC2.

### 8.2 GitHub secrets
Add these in your GitHub repo settings:
- `EC2_HOST` (public IP or DNS)
- `EC2_USER` (usually `ubuntu`)
- `EC2_SSH_KEY` (private key content)
- `EC2_PORT` (optional, default 22)
- `EC2_APP_DIR` (optional, default `/srv/research-backend`)
- `S3_BUCKET` (example `research-models-prod`)
- `S3_PREFIX` (example `final_sinhala_mood_model`)
- `APP_SERVICE` (optional, default `research-backend`)

### 8.3 Ensure deploy script is executable
On EC2:
```bash
chmod +x /srv/research-backend/scripts/ec2_deploy.sh
```

---

## 9) Model Delivery via S3
Deployment script syncs the model from S3 to:

```
app/ml/model/final_sinhala_mood_model
```

This matches `app/ml/predictor.py`.

If your model path changes, update both `S3_PREFIX` and `MODEL_DIR` or `predictor.py`.

---

## 10) Verification
- API: `http://<ec2-ip>:8000`
- Docs: `http://<ec2-ip>:8000/docs`

---

## 11) Rollback
If a deploy fails or the new version is broken:
1. SSH into EC2
2. Checkout previous commit and restart:
   ```bash
   cd /srv/research-backend
   git checkout <previous-commit>
   sudo systemctl restart research-backend
   ```

---

## 12) Monitoring and Logs
- Service logs:
  ```bash
  journalctl -u research-backend -n 200 --no-pager
  ```
- Process status:
  ```bash
  systemctl status research-backend
  ```

---

## 13) Security Checklist
- Never commit `.env`
- Lock down SSH access (IP allowlist)
- Use MongoDB Atlas IP allowlist
- Use strong `JWT_SECRET`
- Prefer HTTPS via Nginx and a valid TLS certificate

---

## 14) Cost Notes
- EC2 instance cost depends on instance type
- S3 storage costs depend on model size
- Data transfer costs apply for downloads from S3 to EC2

---

## 15) Optional: Nginx + HTTPS
If you want a stable URL with HTTPS:
1. Install Nginx
2. Proxy pass to `localhost:8000`
3. Use a domain and enable TLS with certbot

---

## 16) Troubleshooting
- GitHub Actions cannot SSH:
  - Check `EC2_HOST`, `EC2_USER`, `EC2_SSH_KEY` secrets
  - Ensure SSH port open in Security Group
- Model sync errors:
  - Verify IAM role includes S3 read permissions
  - Confirm `S3_BUCKET` and `S3_PREFIX`
- App fails to start:
  - Check `journalctl` logs
  - Ensure `.env` values are correct
  - Run `uvicorn` manually for debug
