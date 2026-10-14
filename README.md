# How to Scrape Arbetsformedlingen: Sweden Job Ads from the Official JobTech API

> **Run it now, no code: [arbetsformedlingen-jobs-scraper on the Apify Store](https://apify.com/bibian/arbetsformedlingen-jobs-scraper)** &nbsp;|&nbsp; $2.00 per 1,000 job ads &nbsp;|&nbsp; no browser, no API key

Arbetsformedlingen is the Swedish Public Employment Service, publishing over 40,000 active job ads nationwide through JobTech, its own public API. This guide shows how to get the ads as clean structured data: employer, official occupation codes, location, work schedule and full description, with a free Apify Actor, from the console or from code.

Searches this page answers: arbetsformedlingen scraper, sweden jobs scraper, jobtech api, platsbanken scraper.

## What you get from the Arbetsformedlingen scraper

- Every job ad matching a keyword, newest first, with employer name, workplace and official organization number.
- Official SSYK occupation taxonomy (`occupation`, `occupationGroup`, `occupationField`), employment type and working hours type.
- Location (municipality, region, city, postcode) and a direct `applicationUrl`.
- Full plain-text description, with every named-recruiter contact block and loose phone number or e-mail removed.

Export the dataset as JSON, CSV or Excel, or read it through the Apify API. A real sample (five results, personal data removed) is in [`sample-output.json`](sample-output.json).

## Output fields

| Field | What it is |
|---|---|
| `id`, `url` | Arbetsformedlingen ad id and public link on Platsbanken |
| `title` | Job title |
| `employer.name`, `employer.workplace`, `employer.url`, `employer.organizationNumber` | Hiring employer, its public company registration number |
| `occupation`, `occupationGroup`, `occupationField` | Official SSYK occupation taxonomy labels |
| `employmentType`, `workingHoursType`, `duration` | Contract type, full/part time, duration |
| `salaryType`, `salaryDescription` | Pay type and description when disclosed, null otherwise |
| `numberOfVacancies` | How many positions the ad covers |
| `municipality`, `region`, `country`, `city`, `postcode` | Where the job is based |
| `description` | Full plain-text description, recruiter contact block removed |
| `publicationDate`, `lastApplicationDate` | Posting and deadline dates |
| `applicationUrl` | Direct link to apply |

## Use cases

- **Monitor the Swedish labour market by occupation.** Group by `occupationField`/`occupationGroup` to track demand across sectors and regions.
- **Build a daily job alert.** Schedule a run every morning with `publishedWithinDays` set to `1` and send the new ads to Slack, e-mail or a Google Sheet.
- **Find the employers hiring in a municipality.** Filter by `municipality` and list which organizations recruit there this week.
- **Feed a job board, a research dataset or a recruiting CRM.** Structured fields and a stable `id`/`url` per ad for deduplication across runs.

## Input

| Field | What it does |
|---|---|
| `keyword` | Job title, skill or employer, for example `sjukskoterska`. Empty means every ad nationwide. |
| `maxItems` | The run stops once this many ads are saved (default 50). |
| `publishedWithinDays` | Only keep ads published in the last N days. Leave empty for no date filter. |

Example input:

```json
{
  "keyword": "sjukskoterska",
  "maxItems": 50
}
```

## Three ways to use it

### 1. Apify console, no code

1. Open [the Actor page](https://apify.com/bibian/arbetsformedlingen-jobs-scraper) and click **Try for free** (a free Apify account is enough).
2. Fill in the input form (keyword, date window and the maximum number of results) and click **Start**.
3. When the run finishes, open the **Output** tab, check the table, then **Export** as CSV, Excel or JSON.
4. For a daily alert, open **Schedules**, create a daily schedule for the Actor and, optionally, add an integration that sends new results to Slack, e-mail or Google Sheets.

### 2. Apify API with JavaScript

```bash
npm install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
node examples/run.js
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('bibian/arbetsformedlingen-jobs-scraper').call({
    "keyword": "sjukskoterska",
    "maxItems": 50
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const item of items) {
    console.log(`${item.title} | ${item.employer?.name} | ${item.municipality}`);
}
```

The complete file is [`examples/run.js`](examples/run.js) (ES module, Node 18 or later).

### 3. Apify API with Python

```bash
pip install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
python examples/run.py
```

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("bibian/arbetsformedlingen-jobs-scraper").call(run_input={
    "keyword": "sjukskoterska",
    "maxItems": 50,
})

for item in client.dataset(run.default_dataset_id).iterate_items():
    employer = item.get("employer") or {}
    print(f"{item['title']} | {employer.get('name')} | {item.get('municipality')}")
```

The complete file is [`examples/run.py`](examples/run.py). Never put your token in the code: read it from the `APIFY_TOKEN` environment variable as above.

## Pricing

Pay per result: **$2.00 per 1,000 job ads** (that is $0.002 per job ad), plus a tiny start fee. You pay only for the results saved to the dataset. Apify's free plan includes monthly credits, enough to try it on a few hundred results. Prices are those shown on the [Store page](https://apify.com/bibian/arbetsformedlingen-jobs-scraper) when this guide was written; the Store page is the reference.

## Why this one

- **Official SSYK occupation codes on every ad**, useful for occupation-level analysis without an extra lookup.
- **No browser, no proxy, no API key.** JobTech's search is a plain, documented, public JSON API.
- **Date-window filtering built in**, so a daily run only brings back what is new.

## Limits and honest notes

- Most ads do not disclose a salary; `salaryDescription` is `null` when that is the case, nothing is guessed.
- Arbetsformedlingen's own `application_contacts` field (named recruiter, direct phone number) is left out entirely, and any phone number or e-mail address found loose inside `description` is stripped. The dataset carries no personal data.
- `employer.organizationNumber` is Sweden's public company registration number, not personal data.
- This is an unofficial tool, not affiliated with Arbetsformedlingen or the JobTech team. Check the API's terms and the data protection rules that apply to your use.

## FAQ

**Does it need a browser or a proxy?**  
No. The Actor reads JobTech's own public JSON API directly.

**Does it work without `keyword`?**  
Yes. Leave it empty for a productive default run across the newest ads nationwide.

**Can I get the data in Excel or Google Sheets?**  
Yes. Export the dataset as CSV, Excel or JSON from the Apify console, or connect the Apify Google Sheets integration.

## Try it

**[Open arbetsformedlingen-jobs-scraper on the Apify Store](https://apify.com/bibian/arbetsformedlingen-jobs-scraper)**

The code in `examples/` is released under the MIT license (see [LICENSE](LICENSE)). The data belongs to its original publishers.
