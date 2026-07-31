import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import canonicalPool from '$lib/server/canonicalDb';

interface EndpointField {
  dbColumn: string;
  type: 'int' | 'str' | 'bool' | 'date';
}

interface EndpointConfig {
  table: string;
  key: string;
  fields: Record<string, EndpointField>; // originalCamelCase -> field info
}

const ENDPOINTS: Record<string, EndpointConfig> = {
  bills: {
    table: 'canonical_gb_sct_bills',
    key: 'BillID',
    fields: {
      BillID: { dbColumn: 'bill_id', type: 'int' },
      ShortName: { dbColumn: 'short_name', type: 'str' },
      SessionID: { dbColumn: 'session_id', type: 'int' },
      BillType: { dbColumn: 'bill_type', type: 'str' },
      SponsorType: { dbColumn: 'sponsor_type', type: 'str' },
      SponsorName: { dbColumn: 'sponsor_name', type: 'str' },
      SponsorPartyID: { dbColumn: 'sponsor_party_id', type: 'int' },
      SponsorGenderID: { dbColumn: 'sponsor_gender_id', type: 'int' },
      SponsorIsFirstTime: { dbColumn: 'sponsor_is_first_time', type: 'bool' },
      SessionalBillLoad: { dbColumn: 'sessional_bill_load', type: 'int' },
      PassedStage3: { dbColumn: 'passed_stage_3', type: 'bool' },
      WentToReconsideration: { dbColumn: 'went_to_reconsideration', type: 'bool' },
      BillOutcome: { dbColumn: 'bill_outcome', type: 'str' },
      IntroductionDate: { dbColumn: 'introduction_date', type: 'date' },
      T1DurationCalendar: { dbColumn: 't1_duration_calendar', type: 'int' },
      T2DurationCalendar: { dbColumn: 't2_duration_calendar', type: 'int' },
      T3DurationCalendar: { dbColumn: 't3_duration_calendar', type: 'int' },
      ViscosityOutlier: { dbColumn: 'viscosity_outlier', type: 'bool' }
    }
  },
  memberpartyhistory: {
    table: 'canonical_gb_sct_member_party_history',
    key: 'SnapshotDate',
    fields: {
      SnapshotDate: { dbColumn: 'snapshot_date', type: 'date' },
      PartyID: { dbColumn: 'party_id', type: 'int' },
      PartyName: { dbColumn: 'party_name', type: 'str' },
      MemberCount: { dbColumn: 'member_count', type: 'int' }
    }
  },
  sessions: {
    table: 'raw_mirror.raw_gb_sct_sessions',
    key: 'ID',
    fields: {
      ID: { dbColumn: 'id', type: 'int' },
      ShortName: { dbColumn: 'shortname', type: 'str' },
      Name: { dbColumn: 'name', type: 'str' },
      StartDate: { dbColumn: 'startdate', type: 'date' },
      EndDate: { dbColumn: 'enddate', type: 'date' }
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
    return json({ error: `Canonical resource endpoint '${endpoint}' not found` }, { status: 404 });
  }

  const ep = ENDPOINTS[matchingKey];
  const table = ep.table;
  const fields = ep.fields;
  
  try {
    const sqlParams: any[] = [];
    const filterClauses: string[] = [];
    let pCounter = 1;

    // 1. Parse OData $filter
    const filterParam = url.searchParams.get('$filter');
    if (filterParam) {
      // Basic OData filter parsing: e.g. "BillID eq 124" or "BillOutcome eq 'PASSED'"
      const filterRegex = /^\s*([a-zA-Z0-9_]+)\s+(eq|gt|lt|ge|le)\s+(.+)\s*$/i;
      const match = filterParam.match(filterRegex);
      if (match) {
        const odataKey = match[1];
        const op = match[2].toLowerCase();
        let val = match[3].trim();

        // Validate column is allowed
        const matchingField = Object.entries(fields).find(([k]) => k.toLowerCase() === odataKey.toLowerCase());
        if (matchingField) {
          const [camelKey, fieldInfo] = matchingField;
          // Strip quotes if string
          if ((val.startsWith("'") && val.endsWith("'")) || (val.startsWith('"') && val.endsWith('"'))) {
            val = val.substring(1, val.length - 1);
          }

          let sqlOp = '=';
          if (op === 'gt') sqlOp = '>';
          if (op === 'lt') sqlOp = '<';
          if (op === 'ge') sqlOp = '>=';
          if (op === 'le') sqlOp = '<=';

          filterClauses.push(`${fieldInfo.dbColumn} ${sqlOp} $${pCounter++}`);
          sqlParams.push(val);
        }
      }
    }

    // 2. Select projection ($select)
    let selectClause = '*';
    const selectParam = url.searchParams.get('$select');
    if (selectParam) {
      const parts = selectParam.split(',').map(p => p.trim());
      const validCols: string[] = [];
      for (const part of parts) {
        const matchingField = Object.entries(fields).find(([k]) => k.toLowerCase() === part.toLowerCase());
        if (matchingField) {
          validCols.push(`${matchingField[1].dbColumn} AS ${matchingField[0].toLowerCase()}`);
        }
      }
      if (validCols.length > 0) {
        selectClause = validCols.join(', ');
      }
    } else {
      // Build projection to map db snake_case to lowercase camel key matching row map expectation
      const selectParts = Object.entries(fields).map(([camelKey, fieldInfo]) => {
        return `${fieldInfo.dbColumn} AS ${camelKey.toLowerCase()}`;
      });
      selectClause = selectParts.join(', ');
    }

    // 3. Order by ($orderby)
    let orderClause = '';
    const orderParam = url.searchParams.get('$orderby');
    if (orderParam) {
      const match = orderParam.match(/^\s*([a-zA-Z0-9_]+)(?:\s+(asc|desc))?\s*$/i);
      if (match) {
        const odataKey = match[1];
        const dir = (match[2] || 'asc').toUpperCase();
        const matchingField = Object.entries(fields).find(([k]) => k.toLowerCase() === odataKey.toLowerCase());
        if (matchingField) {
          orderClause = `ORDER BY ${matchingField[1].dbColumn} ${dir}`;
        }
      }
    }

    // 4. Limit and Offset ($top and $skip)
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

    // 5. Build SQL
    const whereClause = filterClauses.length > 0 ? `WHERE ${filterClauses.join(' AND ')}` : '';
    const sql = `SELECT ${selectClause} FROM ${table} ${whereClause} ${orderClause} ${limitClause} ${offsetClause};`;

    // 6. Query Database B (Canonical)
    const dbRes = await canonicalPool.query(sql, sqlParams);
    
    // 7. Remap database columns back to OData CamelCase keys
    const mappedRows = dbRes.rows.map(row => {
      const mapped: Record<string, any> = {};
      for (const [camelKey, fieldInfo] of Object.entries(fields)) {
        const lowKey = camelKey.toLowerCase();
        if (lowKey in row) {
          let val = row[lowKey];
          if (val === null) {
            mapped[camelKey] = null;
          } else if (fieldInfo.type === 'date' && val instanceof Date) {
            mapped[camelKey] = val.toISOString().split('T')[0];
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
    console.error(`Canonical API Query Failure on endpoint '${endpoint}':`, error);
    return json({ error: 'Database execution failed', details: error.message }, { status: 500 });
  }
};
