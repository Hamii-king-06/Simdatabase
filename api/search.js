export default async function handler(req, res) {
  // Enable CORS for your domain
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
    // Forward the request to the upstream search source endpoint
    const targetResponse = await fetch('https://paksim.xyz/psg-search.php', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
      },
      body: `q=${encodeURIComponent(query)}`
    });

    const data = await targetResponse.json();
    return res.status(200).json(data);

  } catch (error) {
    return res.status(500).json({ ok: false, error: 'Failed to fetch upstream data' });
  }
}
