# BizBuildersAI Social Automation Starter Kit

This kit sets up:
- Notion = content hub
- Activepieces = automation engine
- Postiz = social publisher

## Setup Steps

1. Copy `.env.template` to `.env` and add your keys (Notion, Postiz, AI).

2. Run:
   docker-compose --env-file .env up -d

   - Activepieces → http://YOUR_SERVER:8080
   - Postiz → http://YOUR_SERVER:5000

3. Create Notion DB using `notion_create_database.json` (replace page_id).
   Add sample posts with `notion_sample_pages.json`.

4. Import Activepieces workflows:
   - AI → Notion Drafts
   - Notion Approved → Postiz Publish

   Replace placeholders with real keys.

5. In Postiz, connect your social accounts, generate API key, update `.env`.

6. Daily ops:
   - Draft and approve posts in Notion.
   - Approved posts auto-publish via Postiz.
   - Notion updates to Published with Live URL.

---
