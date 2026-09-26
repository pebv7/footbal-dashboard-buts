# MatchFreq hosting (AWS)

Production is **Amazon S3 + CloudFront** behind **https://matchfreq.com**, deployed by GitHub Actions.

## Live URL

**https://matchfreq.com** (also `https://www.matchfreq.com`)

Distribution hostname (origin): `d25r7vf4jjcqyi.cloudfront.net`

## Stack

| Resource | Value |
|----------|--------|
| CloudFormation stack | `matchfreq-site` (eu-west-1) |
| S3 bucket | `matchfreq-site-848937835337` |
| CloudFront distribution | `E29GO3DGPWDS6K` |
| CloudFront domain | `d25r7vf4jjcqyi.cloudfront.net` |
| ACM cert (us-east-1) | `arn:aws:acm:us-east-1:848937835337:certificate/686da52d-0bde-4264-82dc-4ab168079451` |
| Route 53 zone | `Z00262423B0CK2S14NG8K` (`matchfreq.com`) |
| Deploy role (OIDC) | `arn:aws:iam::848937835337:role/matchfreq-github-deploy-848937835337` |
| CI user | `matchfreq-ci` (GitHub secrets `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`) |
| Template | [`infra/matchfreq-site.yaml`](matchfreq-site.yaml) |

## DNS

- Apex `matchfreq.com` → Route 53 **A/AAAA alias** → CloudFront (`Z2FDTNDATAQYW2` / `d25r7vf4jjcqyi.cloudfront.net`)
- `www.matchfreq.com` → **CNAME** → `d25r7vf4jjcqyi.cloudfront.net`
- CloudFront alternate names: `matchfreq.com`, `www.matchfreq.com` + ACM cert (covers both)

Registrar must use the Route 53 name servers for this hosted zone (already the case if the zone is authoritative).

## Deploy

Workflow: [`.github/workflows/deploy.yml`](../.github/workflows/deploy.yml)

- **Daily** 01:20 UTC: `fetch_espn.py` → `build.py` → commit snapshot if changed → S3 upload → CloudFront invalidation
- **Push to `main`**: rebuild + upload (skips the bot’s own data-commit push)
- **Manual**: Actions → “Update and deploy MatchFreq” → Run workflow

```bash
python3 build.py
aws s3 cp index.html s3://matchfreq-site-848937835337/index.html \
  --cache-control "public,max-age=60,must-revalidate" --content-type "text/html; charset=utf-8"
# …robots.txt, sitemap.xml, images…
aws cloudfront create-invalidation --distribution-id E29GO3DGPWDS6K --paths "/*"
```

## GitHub Pages

Disabled / not production (avoid duplicate canonicals).
