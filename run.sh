python3 -m repo_generator.main

REPO=$(jq -r '.github_username' params.json)/$(jq -r '.blog_title' params.json)

gh secret set NOTION_USER_ID -b$(jq -r '.notion_user_id' params.json) --repo="$REPO"
gh secret set NOTION_TOKEN -b$(jq -r '.notion_token' params.json) --repo="$REPO"
gh secret set NOTION_ROOT_URL -b$(jq -r '.notion_root_url' params.json) --repo="$REPO"
