import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import pool from '$lib/server/db';

interface EndpointConfig {
  table: string;
  key: string;
  strategy: 'lookup' | 'yearly';
  fields: Record<string, string>; // originalCamelCase -> databaseType
}

const ENDPOINTS: Record<string, EndpointConfig> = {
  billtypes: {
    table: 'raw_gb_sct_billtypes',
    key: 'ID',
    strategy: 'lookup',
    fields: { ID: 'int', Name: 'str' }
  },
  billstagetypes: {
    table: 'raw_gb_sct_billstagetypes',
    key: 'ID',
    strategy: 'lookup',
    fields: { ID: 'int', Name: 'str', BillTypeID: 'int', Sequence: 'int' }
  },
  parties: {
    table: 'raw_gb_sct_parties',
    key: 'ID',
    strategy: 'lookup',
    fields: {
      ID: 'int', Abbreviation: 'str', ActualName: 'str',
      PreferredName: 'str', Notes: 'str', ValidFromDate: 'timestamp', ValidUntilDate: 'timestamp'
    }
  },
  committeeroles: {
    table: 'raw_gb_sct_committeeroles',
    key: 'ID',
    strategy: 'lookup',
    fields: { ID: 'int', Name: 'str', Notes: 'str' }
  },
  committeetypes: {
    table: 'raw_gb_sct_committeetypes',
    key: 'ID',
    strategy: 'lookup',
    fields: { ID: 'int', Name: 'str' }
  },
  bills: {
    table: 'raw_gb_sct_bills',
    key: 'ID',
    strategy: 'lookup',
    fields: {
      ID: 'int', Reference: 'str', ShortName: 'str',
      FullName: 'str', BillTypeID: 'int', PersonID: 'int', ThirdPartyOrganisation: 'str'
    }
  },
  billstages: {
    table: 'raw_gb_sct_billstages',
    key: 'ID',
    strategy: 'lookup',
    fields: { ID: 'int', BillID: 'int', BillStageTypeID: 'int', StageDate: 'timestamp' }
  },
  members: {
    table: 'raw_gb_sct_members',
    key: 'PersonID',
    strategy: 'lookup',
    fields: {
      PersonID: 'int', PhotoURL: 'str', Notes: 'str', BirthDate: 'timestamp',
      BirthDateIsProtected: 'bool', ParliamentaryName: 'str', PreferredName: 'str',
      GenderTypeID: 'int', IsCurrent: 'bool'
    }
  },
  memberparties: {
    table: 'raw_gb_sct_memberparties',
    key: 'ID',
    strategy: 'lookup',
    fields: { ID: 'int', PersonID: 'int', PartyID: 'int', ValidFromDate: 'timestamp', ValidUntilDate: 'timestamp' }
  },
  committees: {
    table: 'raw_gb_sct_committees',
    key: 'ID',
    strategy: 'lookup',
    fields: {
      ID: 'int', ShortName: 'str', Name: 'str', Description: 'str',
      CommitteeEmailAddress: 'str', CommitteeTelephone: 'str', ValidFromDate: 'timestamp', ValidUntilDate: 'timestamp'
    }
  },
  personcommitteeroles: {
    table: 'raw_gb_sct_personcommitteeroles',
    key: 'ID',
    strategy: 'lookup',
    fields: {
      ID: 'int', PersonID: 'int', CommitteeRoleID: 'int', CommitteeID: 'int',
      ValidFromDate: 'timestamp', ValidUntilDate: 'timestamp', Notes: 'str'
    }
  },
  motionsquestionsanswersmotions: {
    table: 'raw_gb_sct_motions',
    key: 'UniqueID',
    strategy: 'lookup',
    fields: {
      UniqueID: 'int', EventID: 'str', EventTypeID: 'int', EventSubTypeID: 'int',
      MSPID: 'int', Party: 'str', RegionID: 'int', ConstituencyID: 'int',
      ApprovedDate: 'timestamp', SubmissionDateTime: 'timestamp', Title: 'str', ItemText: 'str'
    }
  },
  motions: {
    table: 'raw_gb_sct_motions',
    key: 'UniqueID',
    strategy: 'lookup',
    fields: {
      UniqueID: 'int', EventID: 'str', EventTypeID: 'int', EventSubTypeID: 'int',
      MSPID: 'int', Party: 'str', RegionID: 'int', ConstituencyID: 'int',
      ApprovedDate: 'timestamp', SubmissionDateTime: 'timestamp', Title: 'str', ItemText: 'str'
    }
  },
  votesmotion: {
    table: 'raw_gb_sct_votes',
    key: 'ID',
    strategy: 'yearly',
    fields: {
      ID: 'str', Detail: 'jsonb', Motion: 'jsonb', Person: 'jsonb', Time: 'jsonb', UpdatedElasticDate: 'timestamp'
    }
  },
  orsplenarymeeting: {
    table: 'raw_gb_sct_plenary_reports',
    key: 'ID',
    strategy: 'yearly',
    fields: {
      ID: 'str', Meeting: 'jsonb', Committee: 'jsonb', Time: 'jsonb', ItemOfBusiness: 'jsonb', Person: 'jsonb', Detail: 'jsonb', UpdatedElasticDate: 'timestamp'
    }
  },
  orscommitteemeeting: {
    table: 'raw_gb_sct_committee_reports',
    key: 'ID',
    strategy: 'yearly',
    fields: {
      ID: 'str', RecordType: 'str', SubType: 'str', Meeting: 'jsonb', Committee: 'jsonb',
      Time: 'jsonb', ItemOfBusiness: 'jsonb', Person: 'jsonb', Detail: 'jsonb', Location: 'jsonb',
      UpdatedDate: 'timestamp', UpdatedElasticDate: 'timestamp'
    }
  }
};

export const GET: RequestHandler = async ({ params, url }) => {
  const { endpoint } = params;

  if (!endpoint) {
    return json({ error: 'Endpoint parameter is required' }, { status: 400 });
  }

  // Case-insensitive lookup of config
  const matchingKey = Object.keys(ENDPOINTS).find(k => k.toLowerCase() === endpoint.toLowerCase());
  
  if (!matchingKey) {
    return json({ error: `OData resource endpoint '${endpoint}' not found` }, { status: 404 });
  }

  const ep = ENDPOINTS[matchingKey];
  const table = ep.table;
  const fields = ep.fields;
  const strategy = ep.strategy;
  
  try {
    const sqlParams: any[] = [];
    const filterClauses: string[] = [];
    let pCounter = 1;

    // 1. Parse OData $filter
    const filterParam = url.searchParams.get('$filter');
    if (filterParam) {
      // Basic OData filter parsing: e.g. "UniqueID eq 255683" or "ID eq 'M123'"
      // Regex captures: [col] [op] [val]
      const filterRegex = /^\s*([a-zA-Z0-9_]+)\s+(eq|gt|lt|ge|le)\s+(.+)\s*$/i;
      const match = filterParam.match(filterRegex);
      if (match) {
        const colName = match[1];
        const op = match[2].toLowerCase();
        let val = match[3].trim();

        // Validate column is allowed
        const matchingField = Object.keys(fields).find(f => f.toLowerCase() === colName.toLowerCase());
        if (matchingField) {
          // Strip quotes if string
          if ((val.startsWith("'") && val.endsWith("'")) || (val.startsWith('"') && val.endsWith('"'))) {
            val = val.substring(1, val.length - 1);
          }

          let sqlOp = '=';
          if (op === 'gt') sqlOp = '>';
          if (op === 'lt') sqlOp = '<';
          if (op === 'ge') sqlOp = '>=';
          if (op === 'le') sqlOp = '<=';

          filterClauses.push(`${colName.toLowerCase()} ${sqlOp} $${pCounter++}`);
          sqlParams.push(val);
        }
      }
    }

    // 2. Parse Year slice parameters (mandatory helper for year-sliced endpoints if no direct filter)
    const yearParam = url.searchParams.get('year');
    if (yearParam && strategy === 'yearly') {
      const year = parseInt(yearParam, 10);
      if (!isNaN(year)) {
        // Query database via JSONB time range filter on the 'time' column start date
        filterClauses.push(`(time->>'Start')::timestamp >= $${pCounter++}`);
        sqlParams.push(`${year}-01-01T00:00:00`);

        filterClauses.push(`(time->>'Start')::timestamp < $${pCounter++}`);
        sqlParams.push(`${year + 1}-01-01T00:00:00`);
      }
    }

    // 3. Select projection ($select)
    let selectClause = '*';
    const selectParam = url.searchParams.get('$select');
    if (selectParam) {
      const parts = selectParam.split(',').map(p => p.trim());
      const validCols: string[] = [];
      for (const part of parts) {
        const match = Object.keys(fields).find(f => f.toLowerCase() === part.toLowerCase());
        if (match) {
          validCols.push(part.toLowerCase());
        }
      }
      if (validCols.length > 0) {
        selectClause = validCols.join(', ');
      }
    }

    // 4. Order by ($orderby)
    let orderClause = '';
    const orderParam = url.searchParams.get('$orderby');
    if (orderParam) {
      const match = orderParam.match(/^\s*([a-zA-Z0-9_]+)(?:\s+(asc|desc))?\s*$/i);
      if (match) {
        const colName = match[1];
        const dir = (match[2] || 'asc').toUpperCase();
        const validField = Object.keys(fields).find(f => f.toLowerCase() === colName.toLowerCase());
        if (validField) {
          orderClause = `ORDER BY ${colName.toLowerCase()} ${dir}`;
        }
      }
    }

    // 5. Limit and Offset ($top and $skip)
    let limitClause = 'LIMIT 100'; // Default safety limit
    const topParam = url.searchParams.get('$top');
    if (topParam) {
      const topVal = parseInt(topParam, 10);
      if (!isNaN(topVal) && topVal >= 0) {
        limitClause = `LIMIT ${Math.min(topVal, 1000)}`; // Max 1000 records
      }
    }

    let offsetClause = '';
    const skipParam = url.searchParams.get('$skip');
    if (skipParam) {
      const skipVal = parseInt(skipParam, 10);
      if (!isNaN(skipVal) && skipVal >= 0) {
        offsetClause = `OFFSET ${skipVal}`;
      }
    }

    // 6. Build SQL
    const whereClause = filterClauses.length > 0 ? `WHERE ${filterClauses.join(' AND ')}` : '';
    const sql = `SELECT ${selectClause} FROM ${table} ${whereClause} ${orderClause} ${limitClause} ${offsetClause};`;

    // 7. Query database
    const dbRes = await pool.query(sql, sqlParams);
    
    // 8. Remap columns to original OData CamelCase keys
    const mappedRows = dbRes.rows.map(row => {
      const mapped: Record<string, any> = {};
      for (const [camelKey, type] of Object.entries(fields)) {
        const lowKey = camelKey.toLowerCase();
        if (lowKey in row) {
          let val = row[lowKey];
          if (val === null) {
            mapped[camelKey] = null;
          } else if (type === 'timestamp' && val instanceof Date) {
            // Standardize format as YYYY-MM-DDTHH:mm:ss
            mapped[camelKey] = val.toISOString().split('.')[0];
          } else {
            mapped[camelKey] = val;
          }
        }
      }
      return mapped;
    });

    return json(mappedRows, {
      headers: {
        'Cache-Control': 'public, max-age=60',
        'Access-Control-Allow-Origin': '*'
      }
    });

  } catch (error: any) {
    console.error(`Mirror API Query Failure on endpoint '${endpoint}':`, error);
    return json({ error: 'Database execution failed', details: error.message }, { status: 500 });
  }
};
