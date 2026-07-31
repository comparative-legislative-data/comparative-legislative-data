import pg from 'pg';

const { Pool } = pg;

// Singleton connection pool for isolated Database B (Canonical)
const canonicalPool = new Pool({
  host: process.env.PGHOST || '127.0.0.1',
  port: parseInt(process.env.PGPORT || '5432', 10),
  database: process.env.PGCANONICALDATABASE || 'comparative_legislative_data_canonical',
  user: process.env.PGUSER || 'postgres',
  password: process.env.PGPASSWORD || '',
  max: 10,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

export default canonicalPool;
