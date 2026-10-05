const http = require('http');
const { createClient } = require('redis');

const PORT = 3000;
const REDIS_URL = process.env.REDIS_URL || 'redis://redis:6379';

let redisClient;

async function connectRedis() {
  redisClient = createClient({ url: REDIS_URL });
  redisClient.on('error', (err) => console.error('Redis error:', err));
  await redisClient.connect();
  console.log('Connected to Redis');

  // Seed default student data if not present
  const exists = await redisClient.exists('student:name');
  if (!exists) {
    await redisClient.hSet('student:info', {
      name: 'Alex Morgan',
      regNo: '2447101',
      programme: 'Master of Computer Applications (DevOps)',
      email: 'alex.morgan@university.edu',
      phone: '+1 (555) 019-2834',
      semester: '5th Trimester',
      section: 'MCA DevOps',
      university: 'CHRIST (Deemed-to-be University)'
    });
    console.log('Seeded default student data');
  }
}

const server = http.createServer(async (req, res) => {
  // CORS headers for frontend communication
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Content-Type', 'application/json');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  try {
    if (req.url === '/api/health') {
      const redisStatus = redisClient && redisClient.isOpen ? 'connected' : 'disconnected';
      res.writeHead(200);
      res.end(JSON.stringify({
        status: 'healthy',
        service: 'student-api',
        redis: redisStatus,
        timestamp: new Date().toISOString()
      }));
    } else if (req.url === '/api/student' && req.method === 'GET') {
      const data = await redisClient.hGetAll('student:info');
      res.writeHead(200);
      res.end(JSON.stringify({ student: data }));
    } else if (req.url === '/api/visits' && req.method === 'GET') {
      const count = await redisClient.incr('visit:count');
      res.writeHead(200);
      res.end(JSON.stringify({ visits: count }));
    } else {
      res.writeHead(404);
      res.end(JSON.stringify({ error: 'Not found' }));
    }
  } catch (err) {
    console.error('Request error:', err);
    res.writeHead(500);
    res.end(JSON.stringify({ error: 'Internal server error' }));
  }
});

connectRedis()
  .then(() => {
    server.listen(PORT, '0.0.0.0', () => {
      console.log(`Student API running on port ${PORT}`);
    });
  })
  .catch((err) => {
    console.error('Failed to start:', err);
    process.exit(1);
  });
