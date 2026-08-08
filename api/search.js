export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,POST');
  res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  const query = req.query.q || (req.body && req.body.q);

  if (!query) {
    return res.status(400).json({ ok: false, error: 'Query parameter "q" is required' });
  }

  try {
    const targetResponse = await fetch('https://paksim.xyz/psg-search.php', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://paksim.xyz/',
        'Origin': 'https://paksim.xyz'
      },
      body: `q=${encodeURIComponent(query)}`
    });

    const text = await targetResponse.text();
    
    // Check if the response is valid JSON before parsing
    try {
      const data = JSON.parse(text);
      return res.status(200).json(data);
    } catch (e) {
      // If the target site returned HTML (like a Cloudflare challenge block)
      return res.status(200).json({ ok: false, raw: text, error: 'Upstream security or cloudflare block' });
    }

  } catch (error) {
    return res.status(500).json({ ok: false, error: 'Failed to fetch upstream data' });
  }
}
