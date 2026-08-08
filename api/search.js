export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const query = req.query.q;
  if (!query) {
    return res.status(400).json({ ok: false, error: 'Query is missing' });
  }

  try {
    const response = await fetch('https://paksim.xyz/psg-search.php', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://paksim.xyz/'
      },
      body: `q=${encodeURIComponent(query)}`
    });

    const text = await response.text();
    try {
      const json = JSON.parse(text);
      return res.status(200).json(json);
    } catch (e) {
      return res.status(200).json({ ok: false, error: 'Target site blocked automated request' });
    }
  } catch (error) {
    return res.status(500).json({ ok: false, error: 'Server error' });
  }
}
