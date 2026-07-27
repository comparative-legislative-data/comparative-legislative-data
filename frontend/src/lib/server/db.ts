import pg from 'pg';

const { Pool } = pg;

// Singleton PostgreSQL connection pool to prevent connection exhaustion under web traffic
const pool = new Pool({
  host: process.env.PGHOST || '127.0.0.1',
  port: parseInt(process.env.PGPORT || '5432', 10),
  database: process.env.PGDATABASE || 'comparative_legislative_data',
  user: process.env.PGUSER || 'postgres',
  password: process.env.PGPASSWORD || '',
  max: 20, // Max 20 connections in pool
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

export default pool;
