// Cloudflare Worker – VLESS over WebSocket
import { connect } from 'cloudflare:sockets';

const UUID = '50414e45-4c5f-5a45-5553-a83e1adb66b6';

export default {
  async fetch(request) {
    if (request.headers.get('Upgrade') !== 'websocket') {
      return new Response('VLESS WebSocket Active', { status: 200 });
    }
    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);
    server.accept();
    handle(server);
    return new Response(null, { status: 101, webSocket: client });
  }
};

async function handle(ws) {
  let writer = null, reader = null;
  let buffer = new Uint8Array(0);
  let connected = false;

  const close = () => {
    try { ws.close(); } catch {}
    try { writer?.close(); } catch {}
  };

  ws.addEventListener('message', async (e) => {
    try {
      const chunk = new Uint8Array(e.data);
      if (!connected) {
        buffer = merge(buffer, chunk);
        const parsed = parse(buffer);
        if (!parsed) return;
        if (parsed.err) { close(); return; }
        buffer = new Uint8Array(0);

        try {
          const sock = connect({ hostname: parsed.host, port: parsed.port });
          writer = sock.writable.getWriter();
          reader = sock.readable.getReader();
        } catch { close(); return; }

        connected = true;
        ws.send(new Uint8Array([0, 0]));
        if (parsed.data.length) await writer.write(parsed.data);

        (async () => {
          try {
            while (true) {
              const { done, value } = await reader.read();
              if (done) break;
              ws.send(value);
            }
          } catch {}
          close();
        })();
      } else {
        await writer.write(chunk);
      }
    } catch { close(); }
  });

  ws.addEventListener('close', close);
  ws.addEventListener('error', close);
}

function merge(a, b) {
  const o = new Uint8Array(a.length + b.length);
  o.set(a); o.set(b, a.length);
  return o;
}

function parse(buf) {
  if (buf.length < 18) return null;
  if (buf[0] !== 0) return { err: 'version' };
  if (uuid(buf.slice(1, 17)) !== UUID) return { err: 'uuid' };

  const opt = buf[17];
  const base = 18 + opt;
  if (buf.length < base + 4) return null;

  let p = base;
  const cmd = buf[p];
  const port = (buf[p + 1] << 8) | buf[p + 2];
  const atyp = buf[p + 3];
  p += 4;

  let host;
  if (atyp === 1) {
    if (buf.length < p + 4) return null;
    host = `${buf[p]}.${buf[p+1]}.${buf[p+2]}.${buf[p+3]}`;
    p += 4;
  } else if (atyp === 2) {
    if (buf.length < p + 1) return null;
    const len = buf[p]; p += 1;
    if (buf.length < p + len) return null;
    host = new TextDecoder().decode(buf.slice(p, p + len));
    p += len;
  } else {
    return { err: 'atyp' };
  }

  if (cmd !== 1) return { err: 'cmd' };
  return { host, port, data: buf.slice(p) };
}

function uuid(b) {
  const h = Array.from(b).map(v => v.toString(16).padStart(2, '0')).join('');
  return `${h.slice(0,8)}-${h.slice(8,12)}-${h.slice(12,16)}-${h.slice(16,20)}-${h.slice(20)}`;
}
