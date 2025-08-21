const express = require('express');
const { exec } = require('child_process');

const app = express();

app.get('/ping', (req, res) => {
  const host = req.query.host || '127.0.0.1';
  // ❌ command injection (tainted host concatenated into shell command)
  exec('ping -c 1 ' + host, (err, stdout, stderr) => {
    if (err) return res.status(500).send(String(err));
    res.send(stdout || stderr);
  });
});

app.get('/eval', (req, res) => {
  const code = req.query.code || '1+1';
  // ❌ use of eval on untrusted input
  const out = eval(code);
  res.send(String(out));
});

app.get('/redir', (req, res) => {
  // ❌ open redirect (user-controlled URL)
  res.redirect(req.query.to || 'https://example.com');
});

app.listen(3000, () => console.log('vuln-js listening on :3000'));
