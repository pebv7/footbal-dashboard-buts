# MatchFreq hosting (AWS)

Production is **Amazon S3 + CloudFront**, deployed by GitHub Actions (OIDC).

## Live URL (until custom domain)

**https://d25r7vf4jjcqyi.cloudfront.net**

## Stack

| Resource | Value |
|----------|--------|
| CloudFormation stack | `matchfreq-site` (eu-west-1) |
| S3 bucket | `matchfreq-site-848937835337` |
| CloudFront distribution | `E29GO3DGPWDS6K` |
| CloudFront domain | `d25r7vf4jjcqyi.cloudfront.net` |
| Deploy role (OIDC) | `arn:aws:iam::848937835337:role/matchfreq-github-deploy-848937835337` |
| Template | [`infra/matchfreq-site.yaml`](matchfreq-site.yaml) |

## Deploy

Workflow: [`.github/workflows/deploy.yml`](../.github/workflows/deploy.yml)

- **Daily** 01:20 UTC: `fetch_espn.py` → `build.py` → commit snapshot if changed → S3 upload → CloudFront invalidation
- **Push to `main`**: rebuild + upload (skips the bot’s own data-commit push)
- **Manual**: Actions → “Update and deploy MatchFreq” → Run workflow

```bash
# Local one-shot publish (requires AWS CLI logged in)
python3 build.py
aws s3 cp index.html s3://matchfreq-site-848937835337/index.html \
  --cache-control "public,max-age=60,must-revalidate" --content-type "text/html; charset=utf-8"
# …same for robots.txt, sitemap.xml, images…
aws cloudfront create-invalidation --distribution-id E29GO3DGPWDS6K --paths "/*"
```

## GitHub Pages

GitHub Pages is **not** the production host. Prefer disabling it in repo **Settings → Pages** to avoid duplicate canonical URLs.

## Custom domain later (`matchfreq.com`)

1. Buy `matchfreq.com`.
2. Request an **ACM certificate in us-east-1** for `matchfreq.com` (+ `www` if used); validate via DNS.
3. CloudFront → Edit → Alternate domain names (CNAMEs) → add `matchfreq.com` → attach the ACM cert.
4. DNS (Route 53 or registrar): alias/ANAME apex → the CloudFront distribution; optional `www` CNAME → distribution domain.
5. Update `SITE_ORIGIN` and SEO URLs in `template.html` / `robots.txt` / `sitemap.xml` to `https://matchfreq.com`, run `build.py`, deploy, invalidate.

Re-deploy the stack after parameter changes:

```bash
aws cloudformation deploy \
  --stack-name matchfreq-site \
  --template-file infra/matchfreq-site.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --region eu-west-1
```
