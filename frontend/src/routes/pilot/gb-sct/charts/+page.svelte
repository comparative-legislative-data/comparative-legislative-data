<script lang="ts">
  import { onMount } from 'svelte';
  import { ArrowLeft, BarChart2, Shield, Flame, Activity, Lock, HelpCircle, X, Clock, Info } from 'lucide-svelte';

  const PARTY_COLORS: Record<string, string> = {
    'Scottish National Party': '#fdf001',
    'Scottish Labour': '#e13939',
    'Scottish Labour Party': '#e13939',
    'Scottish Conservative and Unionist Party': '#0087dc',
    'Scottish Conservative Party': '#0087dc',
    'Scottish Green Party': '#00b140',
    'Scottish Liberal Democrats': '#faa61a',
    'Scottish Socialist Party': '#ff5555',
    'Independent': '#64748b',
    'No Party Affiliation': '#475569',
    'Law Officer (Non-Party)': '#94a3b8',
    'Private Promoter (Non-Party)': '#4b5563'
  };

  const PARTY_NAMES: Record<number, string> = {
    1: 'Independent',
    2: 'No Party Affiliation',
    3: 'Scottish Conservative and Unionist Party',
    4: 'Scottish Green Party',
    5: 'Scottish Labour',
    6: 'Scottish Liberal Democrats',
    7: 'Scottish National Party',
    8: 'Scottish Senior Citizens Unity Party',
    9: 'Scottish Socialist Party',
    10: 'Solidarity Group',
    14: 'Alba Party',
    98: 'Private Promoter (Non-Party)',
    99: 'Law Officer (Non-Party)'
  };

  const sessionalLineColors = ['#818cf8', '#34d399', '#f87171', '#fbbf24', '#38bdf8', '#c084fc'];

  let loading = $state(true);
  let error = $state<string | null>(null);
  let bills = $state<any[]>([]);
  let partyHistory = $state<any[]>([]);
  let sessions = $state<any[]>([]);

  // Toggle state for Bill type filter
  let activeFilter = $state('ALL'); // 'ALL', 'Government', "Member's", 'Committee', 'Private', 'Hybrid'
  let activeDashboardTab = $state<'overview' | 'workloads' | 'party'>('overview');

  // Hover state for sessional bar chart
  let hoveredSession = $state<number | null>(null);

  // Modal tooltip state
  let activeHelpKey = $state<string | null>(null);

  // Grouping function: combines Executive, Government, and Budget into 'Government'
  function getUiGroup(billType: string): string {
    if (billType === 'Executive' || billType === 'Government' || billType === 'Budget') {
      return 'Government';
    }
    return billType; // "Member's", "Committee", "Private", "Hybrid"
  }

  // Derived filtered bills list
  let filteredBills = $derived.by(() => {
    if (activeFilter === 'ALL') return bills;
    return bills.filter(b => getUiGroup(b.BillType) === activeFilter);
  });

  // Dynamic KPI calculations based on active filter
  let totalIntroduced = $derived(filteredBills.length);
  let passedBills = $derived(filteredBills.filter(b => b.PassedStage3).length);
  let successRate = $derived(totalIntroduced > 0 ? ((passedBills / totalIntroduced) * 100).toFixed(2) : '0.00');

  // Sessional stats dynamically grouped from filtered list
  interface SessionStats {
    id: number;
    introduced: number;
    passed: number;
    fallen: number;
  }
  let sessionalStats = $derived.by<SessionStats[]>(() => {
    const statsMap: Record<number, { introduced: number; passed: number }> = {
      1: { introduced: 0, passed: 0 },
      2: { introduced: 0, passed: 0 },
      3: { introduced: 0, passed: 0 },
      4: { introduced: 0, passed: 0 },
      5: { introduced: 0, passed: 0 },
      6: { introduced: 0, passed: 0 }
    };
    
    for (const bill of filteredBills) {
      const sId = bill.SessionID;
      if (sId in statsMap) {
        statsMap[sId].introduced++;
        if (bill.PassedStage3) {
          statsMap[sId].passed++;
        }
      }
    }

    return Object.entries(statsMap).map(([id, val]) => ({
      id: parseInt(id, 10),
      introduced: val.introduced,
      passed: val.passed,
      fallen: val.introduced - val.passed
    }));
  });

  // Calculate maximum introduced value for sessional bar height scaling
  let maxSessionalIntroduced = $derived.by(() => {
    const maxVal = Math.max(...sessionalStats.map(s => s.introduced));
    return maxVal > 0 ? maxVal : 1; // Prevent division by zero
  });

  // Party Success Shares dynamically compiled from filtered list
  interface PartyStats {
    name: string;
    total: number;
    passed: number;
    rate: number;
    color: string;
  }
  let partyStats = $derived.by<PartyStats[]>(() => {
    const pMap: Record<string, { total: number; passed: number }> = {};
    
    for (const bill of filteredBills) {
      const pId = bill.SponsorPartyID;
      const partyName = PARTY_NAMES[pId] || 'Independent';

      if (!pMap[partyName]) {
        pMap[partyName] = { total: 0, passed: 0 };
      }
      pMap[partyName].total++;
      if (bill.PassedStage3) {
        pMap[partyName].passed++;
      }
    }

    return Object.entries(pMap)
      .map(([name, val]) => ({
        name,
        total: val.total,
        passed: val.passed,
        rate: val.total > 0 ? (val.passed / val.total) * 100 : 0,
        color: PARTY_COLORS[name] || '#64748b'
      }))
      .sort((a, b) => b.total - a.total);
  });

  // Stage 7: Sessional Stage Durations dynamically compiled
  interface StageDurations {
    id: number;
    avgT1: number;
    avgT2: number;
    avgT3: number;
    totalAvg: number;
  }
  let stageDurationsBySession = $derived.by<StageDurations[]>(() => {
    // 1. Filter ONLY bills that have Passed Stage 3 AND valid duration data
    const validPassedBills = filteredBills.filter(b => 
      b.PassedStage3 === true && 
      b.T1DurationCalendar !== null && b.T1DurationCalendar !== undefined &&
      b.T2DurationCalendar !== null && b.T2DurationCalendar !== undefined &&
      b.T3DurationCalendar !== null && b.T3DurationCalendar !== undefined
    );
    
    const dMap: Record<number, { t1Sum: number, t2Sum: number, t3Sum: number, count: number }> = {};
    
    for (const bill of validPassedBills) {
      const sId = bill.SessionID;
      if (!dMap[sId]) dMap[sId] = { t1Sum: 0, t2Sum: 0, t3Sum: 0, count: 0 };
      dMap[sId].t1Sum += bill.T1DurationCalendar;
      dMap[sId].t2Sum += bill.T2DurationCalendar;
      dMap[sId].t3Sum += bill.T3DurationCalendar;
      dMap[sId].count++;
    }

    return Object.entries(dMap).map(([id, val]) => {
      const avgT1 = Math.round(val.t1Sum / val.count);
      const avgT2 = Math.round(val.t2Sum / val.count);
      const avgT3 = Math.round(val.t3Sum / val.count);
      return {
        id: parseInt(id, 10),
        avgT1,
        avgT2,
        avgT3,
        totalAvg: avgT1 + avgT2 + avgT3
      };
    }).sort((a, b) => a.id - b.id);
  });

  // Calculate max total duration for stacked bar scaling
  let maxTotalDuration = $derived.by(() => {
    const maxVal = Math.max(...stageDurationsBySession.map(s => s.totalAvg));
    return maxVal > 0 ? maxVal : 1;
  });

  interface SessionalAnalysis {
    id: number;
    years: string;
    totalBills: number;
    halfLife: number;
    diagnosis: string;
    gini: number;
    giniLabel: string;
    q1Pct: number;
    q2Pct: number;
    q3Pct: number;
    q4Pct: number;
    q1Count: number;
    q2Count: number;
    q3Count: number;
    q4Count: number;
    points: { x: number; y: number }[];
    linePath: string;
  }

  let sessionAnalytics = $derived.by<SessionalAnalysis[]>(() => {
    if (sessions.length === 0 || filteredBills.length === 0) return [];

    const sessionMap = new Map(sessions.map(s => [s.ID, s]));
    const results: SessionalAnalysis[] = [];

    const sessionYears: Record<number, string> = {
      1: '1999-2003',
      2: '2003-2007',
      3: '2007-2011',
      4: '2011-2016',
      5: '2016-2021',
      6: '2021-2026'
    };

    for (let sId = 1; sId <= 6; sId++) {
      const session = sessionMap.get(sId);
      if (!session || !session.StartDate) continue;

      const start = new Date(session.StartDate);
      const end = session.EndDate ? new Date(session.EndDate) : new Date('2026-03-24');
      const durationDays = (end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24);

      const sBills = filteredBills
        .filter(b => b.SessionID === sId && b.IntroductionDate)
        .map(b => ({
          ...b,
          introDate: new Date(b.IntroductionDate)
        }))
        .sort((a, b) => a.introDate.getTime() - b.introDate.getTime());

      const totalBills = sBills.length;
      if (totalBills === 0) {
        results.push({
          id: sId,
          years: sessionYears[sId] || '',
          totalBills: 0,
          halfLife: 0,
          diagnosis: 'No Data',
          gini: 0,
          giniLabel: 'No Data',
          q1Pct: 0, q2Pct: 0, q3Pct: 0, q4Pct: 0,
          q1Count: 0, q2Count: 0, q3Count: 0, q4Count: 0,
          points: [],
          linePath: ''
        });
        continue;
      }

      let q1 = 0, q2 = 0, q3 = 0, q4 = 0;
      const points = [{ x: 0, y: 0 }];

      sBills.forEach((b, index) => {
        const offsetDays = (b.introDate.getTime() - start.getTime()) / (1000 * 60 * 60 * 24);
        const x = durationDays > 0 ? Math.max(0, Math.min(1, offsetDays / durationDays)) : 0;
        const y = (index + 1) / totalBills;
        points.push({ x, y });

        if (x < 0.25) q1++;
        else if (x < 0.50) q2++;
        else if (x < 0.75) q3++;
        else q4++;
      });

      // Half-life calculation (elapsed session timeline to caucuse 50% of the sessional bill load)
      const medianIndex = Math.max(0, Math.floor(totalBills / 2) - 1);
      const medianBill = sBills[medianIndex];
      const medianOffset = (medianBill.introDate.getTime() - start.getTime()) / (1000 * 60 * 60 * 24);
      const halfLife = durationDays > 0 ? (medianOffset / durationDays) * 100 : 0;

      let diagnosis = 'Centered';
      if (halfLife < 48.0) diagnosis = 'Front-Loaded';
      else if (halfLife > 56.0) diagnosis = 'Back-Loaded';

      // Gini spacing coefficient using trapezoidal rule integration
      let area = 0;
      for (let i = 1; i < points.length; i++) {
        const dx = points[i].x - points[i-1].x;
        const sumY = points[i].y + points[i-1].y;
        area += dx * sumY;
      }
      const gini = (1 - area) * 100;
      
      let giniLabel = 'Evenly Spread';
      if (gini > 10.0) giniLabel = 'Back-Loaded';
      else if (gini < -10.0) giniLabel = 'Front-Loaded';

      // Map Gini coordinates to 320x200 SVG Viewport
      // padding: left=40, right=40, top=20, bottom=20
      const linePath = points.map((p, idx) => {
        const svgX = 40 + p.x * 240;
        const svgY = 180 - p.y * 160;
        return `${idx === 0 ? 'M' : 'L'} ${svgX.toFixed(1)} ${svgY.toFixed(1)}`;
      }).join(' ');

      results.push({
        id: sId,
        years: sessionYears[sId] || '',
        totalBills,
        halfLife,
        diagnosis,
        gini,
        giniLabel,
        q1Pct: (q1 / totalBills) * 100,
        q2Pct: (q2 / totalBills) * 100,
        q3Pct: (q3 / totalBills) * 100,
        q4Pct: (q4 / totalBills) * 100,
        q1Count: q1,
        q2Count: q2,
        q3Count: q3,
        q4Count: q4,
        points,
        linePath
      });
    }

    return results;
  });

  interface LeaderboardBill {
    bill_id: number;
    short_name: string;
    session_id: number;
    bill_type: string;
    sponsor_name: string;
    duration: number;
    introDateStr: string;
    passedDateStr: string;
  }

  let leaderboardStats = $derived.by<{ longest: LeaderboardBill[]; shortest: LeaderboardBill[] }>(() => {
    const passedList = filteredBills
      .filter(b => b.PassedStage3 && b.T1DurationCalendar !== null && b.T2DurationCalendar !== null && b.T3DurationCalendar !== null)
      .map(b => {
        const totalDuration = (b.T1DurationCalendar || 0) + (b.T2DurationCalendar || 0) + (b.T3DurationCalendar || 0);
        
        let introStr = "N/A";
        let passedStr = "N/A";
        if (b.IntroductionDate) {
          const d = new Date(b.IntroductionDate);
          introStr = d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
          
          const p = new Date(b.IntroductionDate);
          p.setDate(p.getDate() + totalDuration);
          passedStr = p.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
        }
        
        return {
          bill_id: b.BillID,
          short_name: b.ShortName,
          session_id: b.SessionID,
          bill_type: b.BillType,
          sponsor_name: b.SponsorName,
          duration: totalDuration,
          introDateStr: introStr,
          passedDateStr: passedStr
        };
      });
      
    const longest = [...passedList].sort((a, b) => b.duration - a.duration).slice(0, 10);
    const shortest = [...passedList].sort((a, b) => a.duration - b.duration).slice(0, 10);
    
    return { longest, shortest };
  });

  const INFO_REGISTRY: Record<string, { title: string; variables: { name: string; tier: string }[]; formula: string; logic: string }> = {
    introduced: {
      title: 'Introduced (All-Time) Metric',
      variables: [
        { name: 'bill_id', tier: 'Tier 1 (NATIVE_DIRECT)' },
        { name: 'bill_type', tier: 'Tier 2 (DERIVED_DETERMINISTIC)' }
      ],
      formula: 'COUNT(bill_id) GROUP BY bill_type',
      logic: 'Counts the primary bill registry IDs. Note: Raw sessional classifications (Executive, Government, Budget) are normalized at the database level into a single comparative "Government" type to account for nomenclature changes across Holyrood sessions.'
    },
    passed: {
      title: 'Passed Stage 3 Metric',
      variables: [
        { name: 'passed_stage_3', tier: 'Tier 2 (DERIVED_DETERMINISTIC)' },
        { name: 'bill_outcome', tier: 'Tier 2 (DERIVED_DETERMINISTIC)' }
      ],
      formula: "COUNT(bill_id) WHERE passed_stage_3 = TRUE",
      logic: 'Checks the Stage 3 completion date logs to verify if a bill successfully passed its final parliamentary vote.'
    },
    rate: {
      title: 'Chamber Success Rate',
      variables: [
        { name: 'passed_stage_3', tier: 'Tier 2 (DERIVED_DETERMINISTIC)' },
        { name: 'bill_id', tier: 'Tier 1 (NATIVE_DIRECT)' }
      ],
      formula: '(Passed Stage 3 / Introduced All-Time) * 100.0',
      logic: 'Percentage of all introduced bills that successfully completed Stage 3, indicating sessional passage efficiency.'
    },
    sessional: {
      title: 'Sessional Volumes Chart',
      variables: [
        { name: 'session_id', tier: 'Tier 2 (DERIVED_DETERMINISTIC)' },
        { name: 'passed_stage_3', tier: 'Tier 2 (DERIVED_DETERMINISTIC)' }
      ],
      formula: 'COUNT(bill_id) GROUP BY session_id, passed_stage_3',
      logic: 'Aggregates bill records by sessional IDs (Sessions 1-6) using introduction date intervals. Renders a stacked bar splitting Passed Stage 3 (Green) and Fallen/Withdrawn (Red/Orange) segments with a 1px transparent separation gap. Note: As of July 2026, the official upstream API does not yet expose Session 7 records, so Session 7 is excluded.'
    },
    party: {
      title: 'Party Sponsorship Share',
      variables: [
        { name: 'sponsor_party_id', tier: 'Tier 2 (DERIVED_DETERMINISTIC)' },
        { name: 'passed_stage_3', tier: 'Tier 2 (DERIVED_DETERMINISTIC)' }
      ],
      formula: 'COUNT(bill_id) GROUP BY sponsor_party_id',
      logic: 'Joins members party lists temporally on the date of introduction to resolve sponsors party alignment and success. Appointed non-elected Law Officers are resolved dynamically and assigned a synthetic party ID of 99 ("Law Officer (Non-Party)"), while external promoters of Private bills are assigned ID 98 ("Private Promoter (Non-Party)") to reflect their non-partisan statuses and differentiate them from elected Independent MSPs.'
    },
    workload: {
      title: 'Workload "Half-Life" & Sessional Heatmap',
      variables: [
        { name: 'session_id', tier: 'Tier 2 (DERIVED_DETERMINISTIC)' },
        { name: 'introduction_date', tier: 'Tier 2 (DERIVED_DETERMINISTIC)' }
      ],
      formula: 'Count(bills) caucused per quarter & 50% elapsed timeline ratio',
      logic: 'Groups bill introductions into quarters based on their relative elapsed progress through the session lifespan: progress = (intro_date - start_date) / (end_date - start_date). The workload "Half-Life" represents the exact elapsed duration percentage when 50% of caucused bills were introduced. Diagnoses map to Centered (48%-56%), Front-Loaded (<48%), and Back-Loaded (>56%).'
    },
    leaderboards: {
      title: 'Passage Speed Leaderboards',
      variables: [
        { name: 't1_duration_calendar', tier: 'Tier 2 (DERIVED_DETERMINISTIC)' },
        { name: 't2_duration_calendar', tier: 'Tier 2 (DERIVED_DETERMINISTIC)' },
        { name: 't3_duration_calendar', tier: 'Tier 2 (DERIVED_DETERMINISTIC)' }
      ],
    },
    stage_durations: {
      title: 'Sessional Stage Durations',
      variables: [
        { name: 't1_duration_calendar', tier: 'Tier 2 (DERIVED_DETERMINISTIC)' },
        { name: 't2_duration_calendar', tier: 'Tier 2 (DERIVED_DETERMINISTIC)' },
        { name: 't3_duration_calendar', tier: 'Tier 2 (DERIVED_DETERMINISTIC)' },
        { name: 'passed_stage_3', tier: 'Tier 2 (DERIVED_DETERMINISTIC)' }
      ],
      formula: 'AVG(t1), AVG(t2), AVG(t3) GROUP BY SessionID WHERE passed_stage_3 = TRUE',
      logic: 'Calculates the average number of calendar days spent in each legislative stage (Intro->S1, S1->S2, S2->S3). Crucially, the sample ONLY includes bills that successfully passed Stage 3 (passed_stage_3 = TRUE). This methodological decision prevents survivorship bias, ensuring that the averages are not artificially shortened by bills that quickly fell or were withdrawn early in the process.'
    }
  };

  onMount(async () => {
    try {
      loading = true;
      error = null;

      const resBills = await fetch('/api/v2/canonical/gb-sct/bills?$top=1000');
      if (!resBills.ok) throw new Error("Failed to load canonical bills data.");
      bills = await resBills.json();

      const resSessions = await fetch('/api/v2/canonical/gb-sct/sessions');
      if (!resSessions.ok) throw new Error("Failed to load canonical sessions data.");
      sessions = await resSessions.json();

      const resParty = await fetch('/api/v2/canonical/gb-sct/memberpartyhistory?$top=3000');
      if (!resParty.ok) throw new Error("Failed to load canonical party snapshots.");
      partyHistory = await resParty.json();

    } catch (e: any) {
      error = e.message || 'Unknown fetching error';
    } finally {
      loading = false;
    }
  });

  function toggleHelp(key: string) {
    if (activeHelpKey === key) {
      activeHelpKey = null;
    } else {
      activeHelpKey = key;
    }
  }
</script>

<svelte:head>
  <title>Holyrood Charts & Analytics | Scottish Parliament (GB-SCT)</title>
  <meta name="description" content="Visual trends, sessional workload concentration, and regression analytics from Database B canonical research datasets." />
</svelte:head>

<div class="analytics-container">
  <div class="container py-8">
    
    <!-- Top Back Navigation -->
    <div class="top-nav mb-6">
      <a href="/pilot/gb-sct" class="btn-back">
        <ArrowLeft size={16} /> Back to OData Registry
      </a>
    </div>

    <!-- Header Section -->
    <header class="dashboard-header mb-8 text-left">
      <div class="badge-row mb-3">
        <span class="badge badge-canonical">Analytics Staging Layer B</span>
        <span class="badge badge-vps">Live VPS Postgres Connection</span>
      </div>
      <h1 class="page-title">Holyrood Research Charts & Analytics</h1>
      <p class="page-subtitle text-slate-400 mb-4">
        Empirical evaluation of the Scottish Parliament legislative volumes, timescales, and party alignment since 1999.
      </p>
      <div class="alert-box mb-6 bg-slate-900/60 border border-slate-800 p-4 rounded text-xs text-slate-400 flex items-start gap-3">
        <span class="text-amber-500 font-semibold uppercase text-[10px] tracking-wider px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/20">Data Notice</span>
        <span><strong>API Source Lag:</strong> As of July 2026, the official Scottish Parliament OData service (<code>/sessions</code>) has not yet published the Session 7 record. In strict alignment with our academic transparency rules, we only render the native Sessions 1 to 6 returned by the API.</span>
      </div>
    </header>

    {#if loading}
      <div class="loading-state">
        <div class="spinner"></div>
        <span>Syncing and drawing vector canvases...</span>
      </div>
    {:else if error}
      <div class="error-box">
        ⚠️ Failed to query Database B: {error}
      </div>
    {:else}
      <!-- FILTER SEGMENT SELECTOR -->
      <section class="filters-row mb-8 sticky-filter">
        <span class="filter-label">Filter Dashboard by Bill Type:</span>
        <div class="filter-btn-group">
          {#each ['ALL', 'Government', "Member's", 'Committee', 'Private', 'Hybrid'] as filterOpt}
            <button 
              class="filter-btn" 
              class:active={activeFilter === filterOpt}
              onclick={() => activeFilter = filterOpt}
            >
              {filterOpt}
            </button>
          {/each}
        </div>
      </section>

      <!-- DASHBOARD NAVIGATION TABS -->
      <div class="dashboard-tabs-container mb-8">
        <div class="dashboard-tabs">
          <button class="dash-tab {activeDashboardTab === 'overview' ? 'active' : ''}" onclick={() => activeDashboardTab = 'overview'}>Overview & Volumes</button>
          <button class="dash-tab {activeDashboardTab === 'workloads' ? 'active' : ''}" onclick={() => activeDashboardTab = 'workloads'}>Workloads & Timelines</button>
          <button class="dash-tab {activeDashboardTab === 'party' ? 'active' : ''}" onclick={() => activeDashboardTab = 'party'}>Party Analysis</button>
        </div>
      </div>

      {#if activeDashboardTab === 'overview'}
      <!-- 1. KPI COUNTERS GRID -->
      <section class="kpis-grid mb-8">
        <div class="kpi-card">
          <div class="kpi-icon-row">
            <span class="kpi-label">Introduced (All-Time)</span>
            <button class="btn-info-trigger" onclick={() => toggleHelp('introduced')} aria-label="Introduced info">
              <HelpCircle size={14} />
            </button>
          </div>
          <div class="kpi-value">{totalIntroduced}</div>
          <div class="kpi-subtext">Sessional Bills caucused since 1999</div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon-row">
            <span class="kpi-label">Passed Stage 3</span>
            <button class="btn-info-trigger" onclick={() => toggleHelp('passed')} aria-label="Passed info">
              <HelpCircle size={14} />
            </button>
          </div>
          <div class="kpi-value">{passedBills}</div>
          <div class="kpi-subtext">Enacted into Public Acts</div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon-row">
            <span class="kpi-label">Chamber Success Rate</span>
            <button class="btn-info-trigger" onclick={() => toggleHelp('rate')} aria-label="Success rate info">
              <HelpCircle size={14} />
            </button>
          </div>
          <div class="kpi-value">{successRate}%</div>
          <div class="kpi-subtext">Total bills passage-to-introduction ratio</div>
        </div>
      </section>

      <!-- 2. STAGE 3 CHARTS SECTION -->
      <section class="charts-row mb-8">
        <!-- SVG Sessional Volume Chart -->
        <div class="chart-card sessional-chart-card">
          <div class="card-header-row">
            <div class="card-header">
              <h2>Sessional Introductions & Passages</h2>
              <p class="card-desc">Volume of Bills compared to successfully passed Stage 3 (Sessions 1-6)</p>
            </div>
            <button class="btn-info-trigger" onclick={() => toggleHelp('sessional')} aria-label="Sessional volume info">
              <HelpCircle size={14} />
            </button>
          </div>
          
          <!-- Hover Tooltip Overlay -->
          <div class="tooltip-container">
            {#if hoveredSession !== null}
              {@const stats = sessionalStats.find(s => s.id === hoveredSession)}
              {#if stats}
                {@const passPercent = stats.introduced > 0 ? ((stats.passed / stats.introduced) * 100).toFixed(0) : '0'}
                {@const fallenPercent = stats.introduced > 0 ? ((stats.fallen / stats.introduced) * 100).toFixed(0) : '0'}
                <div class="hover-tooltip-card">
                  <div class="tooltip-title">Session {stats.id} Details</div>
                  <div class="tooltip-row">
                    <span class="tooltip-dot introduced-dot"></span>
                    <span>Introduced:</span>
                    <strong>{stats.introduced}</strong>
                  </div>
                  <div class="tooltip-row">
                    <span class="tooltip-dot passed-dot"></span>
                    <span>Passed Stage 3:</span>
                    <strong>{stats.passed} <span class="text-emerald-400">({passPercent}%)</span></strong>
                  </div>
                  <div class="tooltip-row">
                    <span class="tooltip-dot fallen-dot"></span>
                    <span>Fallen / Withdrawn:</span>
                    <strong>{stats.fallen} <span class="text-red-400">({fallenPercent}%)</span></strong>
                  </div>
                </div>
              {/if}
            {:else}
              <div class="tooltip-placeholder">Hover over any session bar to view exact success and failure breakdowns.</div>
            {/if}
          </div>

          <div class="svg-container mt-2">
            <svg viewBox="0 0 500 240" class="bar-chart-svg">
              <!-- Grid Lines -->
              {#each [0, 25, 50, 75, 100] as gridValue}
                {@const percentHeight = maxSessionalIntroduced > 0 ? (gridValue / 100) * maxSessionalIntroduced : 0}
                {@const y = 200 - (percentHeight * (160 / maxSessionalIntroduced))}
                <line x1="40" y1={y} x2="480" y2={y} stroke="rgba(255,255,255,0.04)" stroke-dasharray="3,3" />
                <text x="35" y={y + 4} class="chart-text label-left">{percentHeight.toFixed(0)}</text>
              {/each}
              
              <!-- Session Stacked Bars -->
              {#each sessionalStats as stats, index}
                {@const x = 70 + (index * 68)}
                {@const scale = 160 / maxSessionalIntroduced}
                {@const passedHeight = stats.passed * scale}
                {@const fallenHeight = stats.fallen * scale}
                {@const totalHeight = stats.introduced * scale}
                
                <!-- Bottom Segment (Passed) -->
                {#if stats.passed > 0}
                  <rect 
                    x={x} 
                    y={200 - passedHeight} 
                    width="24" 
                    height={passedHeight} 
                    rx="3"
                    fill="rgba(16, 185, 129, 0.75)"
                    stroke="#10b981"
                    stroke-width="1"
                  />
                {/if}

                <!-- Top Segment (Fallen / Withdrawn) -->
                {#if stats.fallen > 0}
                  <!-- Apply 1px vertical gap shift if both passed and fallen exist -->
                  {@const shiftY = (stats.passed > 0) ? 1 : 0}
                  {@const adjustedFallenHeight = Math.max(0, fallenHeight - shiftY)}
                  <rect 
                    x={x} 
                    y={200 - passedHeight - adjustedFallenHeight - shiftY} 
                    width="24" 
                    height={adjustedFallenHeight} 
                    rx="3"
                    fill="rgba(239, 68, 68, 0.55)"
                    stroke="#ef4444"
                    stroke-width="1"
                  />
                {/if}

                <!-- Total Count Label above bar -->
                {#if stats.introduced > 0}
                  <text x={x + 12} y={200 - totalHeight - 6} class="chart-text count-label" text-anchor="middle">
                    {stats.introduced}
                  </text>
                {/if}

                <!-- Session Labels -->
                <text x={x + 12} y="220" class="chart-text session-label" text-anchor="middle">S{stats.id}</text>

                <!-- Invisible Hover Target Area (wider/taller for easy interaction) -->
                <rect
                  x={x - 10}
                  y="20"
                  width="44"
                  height="190"
                  fill="transparent"
                  style="cursor: pointer;"
                  onmouseenter={() => hoveredSession = stats.id}
                  onmouseleave={() => hoveredSession = null}
                />
              {/each}
              
              <line x1="40" y1="200" x2="480" y2="200" stroke="rgba(255,255,255,0.15)" stroke-width="1.5" />
            </svg>
          </div>
          <div class="legend-row">
            <div class="legend-item"><span class="legend-dot legend-passed"></span> Passed Stage 3</div>
            <div class="legend-item"><span class="legend-dot legend-fallen"></span> Fallen / Withdrawn</div>
          </div>
        </div>
      </section>

      {/if}

      {#if activeDashboardTab === 'party'}
      <section class="charts-row mb-8">
        <!-- Party Sponsorship Share List -->
        <div class="chart-card">
          <div class="card-header-row">
            <div class="card-header">
              <h2>Party Sponsorship & Success (At Intro)</h2>
              <p class="card-desc">Share of all bills sponsored by party and their historical success rates</p>
            </div>
            <button class="btn-info-trigger" onclick={() => toggleHelp('party')} aria-label="Party info">
              <HelpCircle size={14} />
            </button>
          </div>
          <div class="party-list mt-4">
            {#if partyStats.length > 0}
              {#each partyStats as p}
                <div class="party-row">
                  <div class="party-name-row">
                    <span class="party-color-indicator" style="background-color: {p.color};"></span>
                    <span class="party-title">{p.name}</span>
                    <span class="party-vals">{p.total} bills <span class="text-emerald-400">({p.rate.toFixed(0)}% success)</span></span>
                  </div>
                  <div class="progress-track">
                    <div class="progress-fill" style="width: {totalIntroduced > 0 ? (p.total / totalIntroduced) * 100 : 0}%; background-color: {p.color};"></div>
                  </div>
                </div>
              {/each}
            {:else}
              <div class="empty-state text-slate-400 py-12 text-center">No sponsorship records for this bill type.</div>
            {/if}
          </div>
        </div>
      </section>

      {/if}

      {#if activeDashboardTab === 'workloads'}
      
      <!-- STAGE 7: STAGE DURATIONS STACKED BAR CHART -->
      <section class="stage-durations-container mb-8">
        <div class="chart-card">
          <div class="card-header-row mb-4">
            <div class="card-header">
              <h2>Average Stage Durations by Session (Passed Bills Only)</h2>
              <p class="card-desc">Calendar days spent in each legislative stage</p>
            </div>
            <button class="btn-info-trigger" onclick={() => toggleHelp('stage_durations')} aria-label="Stage Durations info">
              <HelpCircle size={14} />
            </button>
          </div>

          <div class="stacked-bar-chart">
            <div class="duration-legend">
              <span class="legend-item"><span class="legend-color t1-color"></span> Intro &rarr; S1</span>
              <span class="legend-item"><span class="legend-color t2-color"></span> S1 &rarr; S2</span>
              <span class="legend-item"><span class="legend-color t3-color"></span> S2 &rarr; S3</span>
            </div>

            <div class="duration-y-axis">
              {#each stageDurationsBySession as stat}
                <div class="duration-row">
                  <div class="duration-label">Session {stat.id}</div>
                  <div class="duration-bar-container">
                    {#if stat.totalAvg > 0}
                      <!-- T1 Segment -->
                      <div class="duration-segment t1-bg" style="width: {(stat.avgT1 / maxTotalDuration) * 100}%">
                        {#if (stat.avgT1 / maxTotalDuration) > 0.08}{stat.avgT1}d{/if}
                      </div>
                      <!-- T2 Segment -->
                      <div class="duration-segment t2-bg" style="width: {(stat.avgT2 / maxTotalDuration) * 100}%">
                        {#if (stat.avgT2 / maxTotalDuration) > 0.08}{stat.avgT2}d{/if}
                      </div>
                      <!-- T3 Segment -->
                      <div class="duration-segment t3-bg" style="width: {(stat.avgT3 / maxTotalDuration) * 100}%">
                        {#if (stat.avgT3 / maxTotalDuration) > 0.08}{stat.avgT3}d{/if}
                      </div>
                    {:else}
                       <div class="duration-empty">No passed bills in filter</div>
                    {/if}
                  </div>
                  <!-- Total Average Label at the end -->
                  <div class="duration-total">
                    {stat.totalAvg > 0 ? `${stat.totalAvg}d` : '-'}
                  </div>
                </div>
              {/each}
              {#if stageDurationsBySession.length === 0}
                <div class="empty-state">No bills matching the current filter have passed Stage 3.</div>
              {/if}
            </div>
          </div>
        </div>
      </section>

      <!-- 3. STAGE 4 WORKSPACE (WORKLOAD & TIMELINE AUDIT) -->
      <section class="stage4-audit-container mb-8">
        <div class="unified-audit-card">
          
          <!-- Unified Header Panel -->
          <div class="unified-header">
            <div class="unified-title">
              <div class="title-with-icon">
                <Activity size={18} class="amber-icon" />
                <h2>Sessional Workload Spacing & "Backending" Audit</h2>
              </div>
              <p class="card-desc">Auditing whether the Scottish Government spreads the load of its bills caucused since 1999</p>
            </div>
          </div>

          <!-- Two-Column Interior Grid -->
          <div class="unified-grid">
            <!-- Left: Workload "Half-Life" Index Table -->
            <div class="unified-column">
              <div class="column-header">
                <span>Workload "Half-Life" Index <span class="sub-label">(Timeline elapsed to hit 50% bill introductions)</span></span>
                <button class="btn-info-trigger" onclick={() => toggleHelp('workload')}>
                  <HelpCircle size={16} />
                </button>
              </div>
              <div class="table-wrapper mt-0">
                <table class="half-life-table borderless">
                  <thead>
                    <tr>
                      <th class="text-left">Session</th>
                      <th class="text-center">Total Bills</th>
                      <th class="text-center">50% Mark Timeline Elapsed</th>
                      <th class="text-right">Spacing Diagnosis</th>
                    </tr>
                  </thead>
                  <tbody>
                    {#each sessionAnalytics as row}
                      <tr>
                        <td class="text-left session-label">S{row.id}</td>
                        <td class="text-center val-label">{row.totalBills}</td>
                        <td class="text-center mark-label">{row.halfLife.toFixed(1)}% <span class="elapsed-text">elapsed</span></td>
                        <td class="text-right">
                          <span class="badge {row.diagnosis === 'Centered' ? 'badge-grey' : row.diagnosis === 'Front-Loaded' ? 'badge-green' : 'badge-red'}">{row.diagnosis}</span>
                        </td>
                      </tr>
                    {/each}
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Right: Segmented horizontal progress bars -->
            <div class="unified-column">
              <div class="column-header">
                <span>Sessional Workload Concentration Heatmap <span class="sub-label">(% of sessional introductions caucused per Quarter)</span></span>
                <button class="btn-info-trigger" onclick={() => toggleHelp('workload')}>
                  <HelpCircle size={16} />
                </button>
              </div>
              
              <div class="segmented-list mt-1">
                {#each sessionAnalytics as row}
                  <div class="segmented-row">
                    <div class="heatmap-row-header">
                      <span class="session-label">S{row.id}</span>
                      <span class="count-label">{row.totalBills} caucused introductions</span>
                    </div>
                    <!-- Segmented progress bar -->
                    <div class="segmented-bar thick-bar">
                      <!-- Q1 -->
                      <div class="segment q1-color" style="width: {row.q1Pct}%;" title="Q1: {row.q1Count} bills">
                        {#if row.q1Pct > 12}<span>{row.q1Pct.toFixed(0)}%</span>{/if}
                      </div>
                      <!-- Q2 -->
                      <div class="segment q2-color" style="width: {row.q2Pct}%;" title="Q2: {row.q2Count} bills">
                        {#if row.q2Pct > 12}<span>{row.q2Pct.toFixed(0)}%</span>{/if}
                      </div>
                      <!-- Q3 -->
                      <div class="segment q3-color" style="width: {row.q3Pct}%;" title="Q3: {row.q3Count} bills">
                        {#if row.q3Pct > 12}<span>{row.q3Pct.toFixed(0)}%</span>{/if}
                      </div>
                      <!-- Q4 -->
                      <div class="segment q4-color" style="width: {row.q4Pct}%;" title="Q4: {row.q4Count} bills">
                        {#if row.q4Pct > 12}<span>{row.q4Pct.toFixed(0)}%</span>{/if}
                      </div>
                    </div>
                  </div>
                {/each}
              </div>
              
              <!-- Legend grid -->
              <div class="heatmap-legend centered mt-2">
                <div class="legend-item">
                  <span class="legend-dot q1-bg"></span>
                  <span>Sessional Q1 (0% to 25% duration)</span>
                </div>
                <div class="legend-item">
                  <span class="legend-dot q2-bg"></span>
                  <span>Sessional Q2 (25% to 50% duration)</span>
                </div>
                <div class="legend-item">
                  <span class="legend-dot q3-bg"></span>
                  <span>Sessional Q3 (50% to 75% duration)</span>
                </div>
                <div class="legend-item">
                  <span class="legend-dot q4-bg"></span>
                  <span>Sessional Q4 (75% to 100% duration)</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Timescale Leaderboards Section -->
        <div class="stage4-section mt-12 mb-8">
          <!-- Longest Duration -->
          <div class="unified-audit-card">
            <div class="card-header-row mb-4">
              <div class="title-with-icon">
                <Clock size={16} class="amber-icon" />
                <h2 class="amber-heading">The Top 10 Longest Legislative Passages</h2>
              </div>
              <button class="btn-info-trigger" onclick={() => toggleHelp('leaderboards')}>
                <HelpCircle size={16} />
              </button>
            </div>
            <div class="leaderboard-list">
              {#each leaderboardStats.longest as bill, idx}
                <div class="bill-card bill-card-amber">
                  <div class="bill-card-header">
                    <span class="bill-idx">SP BILL {bill.bill_id} • {bill.bill_type} BILL</span>
                    <span class="bill-days amber-text">{bill.duration} <span class="days-label">days</span></span>
                  </div>
                  <p class="bill-title font-expanded">{bill.short_name}</p>
                  <div class="bill-meta-row">
                    <span>Sponsor: {bill.sponsor_name} • S{bill.session_id}</span>
                    <span class="dates-meta">Intro: {bill.introDateStr} &nbsp;&nbsp;&nbsp; Passed: {bill.passedDateStr}</span>
                  </div>
                </div>
              {/each}
            </div>
          </div>

          <!-- Shortest Duration -->
          <div class="unified-audit-card">
            <div class="card-header-row mb-4">
              <div class="title-with-icon">
                <Info size={16} class="emerald-icon" />
                <h2 class="emerald-heading">The Top 10 Shortest Legislative Passages</h2>
              </div>
              <button class="btn-info-trigger" onclick={() => toggleHelp('leaderboards')}>
                <HelpCircle size={16} />
              </button>
            </div>
            <div class="leaderboard-list">
              {#each leaderboardStats.shortest as bill, idx}
                <div class="bill-card bill-card-emerald">
                  <div class="bill-card-header">
                    <span class="bill-idx">SP BILL {bill.bill_id} • {bill.bill_type} BILL</span>
                    <span class="bill-days emerald-text">{bill.duration} <span class="days-label">days</span></span>
                  </div>
                  <p class="bill-title font-expanded">{bill.short_name}</p>
                  <div class="bill-meta-row">
                    <span>Sponsor: {bill.sponsor_name} • S{bill.session_id}</span>
                    <span class="dates-meta">Intro: {bill.introDateStr} &nbsp;&nbsp;&nbsp; Passed: {bill.passedDateStr}</span>
                  </div>
                </div>
              {/each}
            </div>
          </div>
        </div>

      </section>
      {/if}


    {/if}

    <!-- POPUP INFORMATION BOX -->
    {#if activeHelpKey && INFO_REGISTRY[activeHelpKey]}
      {@const info = INFO_REGISTRY[activeHelpKey]}
      <div class="info-backdrop" onclick={() => activeHelpKey = null} role="presentation"></div>
      <div class="info-popup">
        <div class="popup-header">
          <h4>{info.title}</h4>
          <button class="btn-close-popup" onclick={() => activeHelpKey = null}>
            <X size={14} />
          </button>
        </div>
        <div class="popup-body">
          <div class="popup-section">
            <span class="popup-sec-title">Variables Involved & Provenance Tiers:</span>
            <div class="popup-vars-row">
              {#each info.variables as v}
                <div class="popup-var-badge" class:tier-1={v.tier.includes('Tier 1')} class:tier-2={v.tier.includes('Tier 2')}>
                  <span class="var-name">{v.name}</span>
                  <span class="var-tier">{v.tier}</span>
                </div>
              {/each}
            </div>
          </div>
          <div class="popup-section">
            <span class="popup-sec-title">SQL Calculation Formula:</span>
            <pre class="popup-formula"><code>{info.formula}</code></pre>
          </div>
          <div class="popup-section">
            <span class="popup-sec-title">Compilation Logic:</span>
            <p class="popup-desc">{info.logic}</p>
          </div>
        </div>
      </div>
    {/if}


  </div>
</div>

<style>
  .analytics-container {
    min-height: calc(100vh - 4.25rem);
    background: #090d16;
    color: #f8fafc;
    text-align: left;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }

  .py-8 { padding-top: 2rem; padding-bottom: 2rem; }
  .py-12 { padding-top: 3rem; padding-bottom: 3rem; }
  .mb-3 { margin-bottom: 0.75rem; }
  .mb-6 { margin-bottom: 1.5rem; }
  .mb-8 { margin-bottom: 2rem; }
  .mb-10 { margin-bottom: 2.5rem; }
  .mt-4 { margin-top: 1rem; }
  .mt-2 { margin-top: 0.5rem; }

  .btn-back {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    color: #94a3b8;
    padding: 0.45rem 1rem;
    border-radius: 0.5rem;
    font-size: 0.85rem;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.2s ease;
  }
  .btn-back:hover {
    background: rgba(255,255,255,0.08);
    color: #ffffff;
  }

  .badge-row {
    display: flex;
    gap: 0.75rem;
  }
  .badge {
    padding: 0.2rem 0.65rem;
    border-radius: 9999px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .badge-canonical {
    background: rgba(16, 185, 129, 0.12);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.25);
  }
  .badge-vps {
    background: rgba(99, 102, 241, 0.12);
    color: #818cf8;
    border: 1px solid rgba(99, 102, 241, 0.25);
  }

  .page-title {
    font-size: 2.25rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0.5rem 0 0 0;
    letter-spacing: -0.025em;
  }

  /* Filters styling */
  .filters-row {
    background: rgba(15, 23, 42, 0.3);
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 0.85rem;
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    flex-wrap: wrap;
  }
  .filter-label {
    font-size: 0.85rem;
    font-weight: 700;
    color: #94a3b8;
  }
  .filter-btn-group {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }
  .filter-btn {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    color: #94a3b8;
    padding: 0.35rem 0.85rem;
    border-radius: 0.375rem;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .filter-btn:hover {
    background: rgba(255,255,255,0.08);
    color: #ffffff;
  }
  .filter-btn.active {
    background: #10b981;
    color: #040815;
    border-color: #10b981;
    font-weight: 700;
  }

  /* KPIs counters */
  .kpis-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
  }
  @media (max-width: 768px) {
    .kpis-grid {
      grid-template-columns: 1fr;
    }
  }

  .kpi-card {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 1rem;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .kpi-icon-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
  }
  .kpi-label {
    font-size: 0.85rem;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    text-align: left;
  }
  .btn-info-trigger {
    background: transparent;
    border: none;
    color: #64748b;
    cursor: pointer;
    padding: 0;
    display: inline-flex;
    transition: color 0.2s ease;
  }
  .btn-info-trigger:hover {
    color: #38bdf8;
  }
  .kpi-value {
    font-size: 2.25rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
  }
  .kpi-subtext {
    font-size: 0.75rem;
    color: #64748b;
  }

  /* Charts Rows */
  .charts-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
  }
  @media (max-width: 1024px) {
    .charts-row {
      grid-template-columns: 1fr;
    }
  }

  .chart-card {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 1rem;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    position: relative;
  }

  .card-header-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
  }

  .card-header {
    text-align: left;
  }
  .card-header h2 {
    margin: 0;
    font-size: 1.15rem;
    font-weight: 700;
    color: #ffffff;
  }
  .card-desc {
    margin: 0.25rem 0 0 0;
    font-size: 0.8rem;
    color: #64748b;
  }

  /* Sessional Tooltip Styles */
  .tooltip-container {
    height: 38px;
    display: flex;
    align-items: center;
    margin-top: 0.75rem;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    padding-bottom: 0.75rem;
  }
  .tooltip-placeholder {
    font-size: 0.75rem;
    color: #475569;
    font-style: italic;
    text-align: left;
  }
  .hover-tooltip-card {
    display: flex;
    align-items: center;
    gap: 1.25rem;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 0.5rem;
    padding: 0.4rem 1rem;
    width: 100%;
  }
  .tooltip-title {
    font-size: 0.8rem;
    font-weight: 800;
    color: #38bdf8;
    border-right: 1px solid rgba(255,255,255,0.1);
    padding-right: 1rem;
  }
  .tooltip-row {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.75rem;
    color: #94a3b8;
  }
  .tooltip-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
  }
  .introduced-dot { background: #fbbf24; }
  .passed-dot { background: #10b981; }
  .fallen-dot { background: #ef4444; }

  /* SVG Bar chart */
  .svg-container {
    height: 240px;
    width: 100%;
  }
  .bar-chart-svg {
    width: 100%;
    height: 100%;
  }
  .chart-text {
    font-family: monospace;
    font-size: 8.5px;
    fill: #64748b;
  }
  .label-left {
    text-anchor: end;
  }
  .session-label {
    font-weight: bold;
    fill: #94a3b8;
    font-size: 10px;
  }
  .count-label {
    fill: #cbd5e1;
    font-size: 8px;
    font-weight: bold;
  }

  .legend-row {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 1rem;
  }
  .legend-item {
    font-size: 0.75rem;
    color: #94a3b8;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-weight: 600;
  }
  .legend-dot {
    width: 10px;
    height: 10px;
    border-radius: 2px;
    display: inline-block;
  }
  .legend-passed {
    background: rgba(16, 185, 129, 0.75);
    border: 1px solid #10b981;
  }
  .legend-fallen {
    background: rgba(239, 68, 68, 0.55);
    border: 1px solid #ef4444;
  }

  /* Party progress list */
  .party-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  .party-row {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }
  .party-name-row {
    display: flex;
    align-items: center;
    font-size: 0.8rem;
    gap: 0.5rem;
  }
  .party-color-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }
  .party-title {
    color: #f1f5f9;
    font-weight: 600;
    flex: 1;
    text-align: left;
  }
  .party-vals {
    color: #94a3b8;
    font-family: monospace;
    font-weight: bold;
  }
  .progress-track {
    background: rgba(255,255,255,0.03);
    border-radius: 9999px;
    height: 6px;
    width: 100%;
    overflow: hidden;
  }
  .progress-fill {
    height: 100%;
    border-radius: 9999px;
  }

  /* Locked Section Panel */
  .locked-section {
    position: relative;
    border-radius: 1rem;
    overflow: hidden;
  }
  .locked-card {
    background: rgba(15, 23, 42, 0.2);
    border: 1px dashed rgba(255, 255, 255, 0.08);
    border-radius: 1rem;
    padding: 2.5rem;
    min-height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .locked-overlay {
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 0.5rem;
  }
  .locked-overlay h3 {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
  }
  .locked-skeleton-body {
    opacity: 0.15;
    filter: blur(1.5px);
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
    margin-top: 1rem;
    pointer-events: none;
    user-select: none;
  }
  .skeleton-header {
    height: 14px;
    width: 150px;
    background: #cbd5e1;
    border-radius: 4px;
  }
  .skeleton-grid {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .skeleton-line {
    height: 8px;
    background: #64748b;
    border-radius: 2px;
    width: 100%;
  }

  /* HELP MODAL POPUP STYLES */
  .info-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(4, 6, 10, 0.5);
    backdrop-filter: blur(4px);
    z-index: 1000;
  }
  .info-popup {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #0f172a;
    border: 1px solid rgba(56, 189, 248, 0.2);
    box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5), 0 0 30px rgba(56, 189, 248, 0.1);
    border-radius: 1rem;
    width: 90%;
    max-width: 450px;
    z-index: 1001;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }
  .popup-header {
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .popup-header h4 {
    margin: 0;
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
  }
  .btn-close-popup {
    background: transparent;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 0.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
  }
  .btn-close-popup:hover {
    color: #ffffff;
    background: rgba(255,255,255,0.05);
  }
  .popup-body {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    text-align: left;
  }
  .popup-section {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }
  .popup-sec-title {
    font-size: 0.75rem;
    font-weight: bold;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .popup-vars-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }
  .popup-var-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.3rem 0.65rem;
    border-radius: 0.375rem;
    font-size: 0.75rem;
  }
  .popup-var-badge.tier-1 {
    background: rgba(56, 189, 248, 0.06);
    border: 1px solid rgba(56, 189, 248, 0.15);
    color: #38bdf8;
  }
  .popup-var-badge.tier-2 {
    background: rgba(52, 211, 153, 0.06);
    border: 1px solid rgba(52, 211, 153, 0.15);
    color: #34d399;
  }
  .var-name {
    font-family: monospace;
    font-weight: 700;
  }
  .var-tier {
    font-size: 0.65rem;
    opacity: 0.85;
    border-left: 1px solid rgba(255, 255, 255, 0.15);
    padding-left: 0.5rem;
  }
  .popup-formula {
    background: #090d16;
    border: 1px solid rgba(255,255,255,0.05);
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;
    margin: 0;
    overflow-x: auto;
  }
  .popup-formula code {
    font-family: monospace;
    color: #34d399;
    font-size: 0.8rem;
  }
  .popup-desc {
    font-size: 0.85rem;
    color: #cbd5e1;
    line-height: 1.5;
    margin: 0;
  }

  /* Common States */
  .loading-state {
    height: 350px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    color: #64748b;
    font-size: 0.95rem;
  }
  .spinner {
    width: 28px;
    height: 28px;
    border: 2px solid rgba(16, 185, 129, 0.1);
    border-top-color: #10b981;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .error-box {
    padding: 1.5rem;
    background: rgba(239, 68, 68, 0.05);
    border: 1px solid rgba(239, 68, 68, 0.15);
    color: #f87171;
    border-radius: 0.5rem;
    font-size: 0.875rem;
  }

  .text-sm { font-size: 0.875rem; }
  .max-w-md { max-w: 28rem; }
  .mx-auto { margin-left: auto; margin-right: auto; }

  /* Stage 4 custom styling */
  .stage4-audit-container {
    display: flex;
    flex-direction: column;
    width: 100%;
  }

  .tabs-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    padding-bottom: 1rem;
    margin-bottom: 1.5rem;
  }

  .tab-pills {
    display: flex;
    gap: 0.5rem;
    background: rgba(15, 23, 42, 0.4);
    padding: 0.25rem;
    border-radius: 0.5rem;
    border: 1px solid rgba(255, 255, 255, 0.05);
  }

  .tab-pill {
    background: transparent;
    border: none;
    color: #94a3b8;
    padding: 0.4rem 1rem;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 0.375rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .tab-pill:hover {
    color: #ffffff;
  }

  .tab-pill.active {
    background: rgba(255, 255, 255, 0.08);
    color: #fef08a; /* Soft golden tint matching active selection */
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.3);
  }

  .stage4-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
  }
  @media (max-width: 1024px) {
    .stage4-section {
      grid-template-columns: 1fr;
    }
  }

  .table-wrapper {
    overflow-x: auto;
    margin-top: 0.5rem;
  }

  .half-life-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.8rem;
    text-align: left;
  }

  .half-life-table th {
    font-size: 0.7rem;
    font-weight: bold;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.5rem 0.25rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }

  .half-life-table td {
    padding: 0.75rem 0.25rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.02);
    color: #cbd5e1;
    vertical-align: middle;
  }

  .half-life-table tbody tr:hover {
    background: rgba(255, 255, 255, 0.01);
  }

  /* Badge System */
  .badge {
    display: inline-flex;
    align-items: center;
    padding: 0.2rem 0.5rem;
    border-radius: 0.25rem;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.02em;
    border: 1px solid transparent;
  }

  .badge-grey {
    background: rgba(71, 85, 105, 0.15);
    border-color: rgba(71, 85, 105, 0.3);
    color: #94a3b8;
  }

  .badge-green {
    background: rgba(16, 185, 129, 0.08);
    border-color: rgba(16, 185, 129, 0.2);
    color: #34d399;
  }

  .badge-red {
    background: rgba(239, 68, 68, 0.08);
    border-color: rgba(239, 68, 68, 0.2);
    color: #f87171;
  }

  /* Segmented Heatmap styling */
  .segmented-list {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
  }

  .segmented-row {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .segmented-bar {
    display: flex;
    height: 1.75rem;
    border-radius: 0.375rem;
    overflow: hidden;
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.04);
    padding: 2px;
    gap: 1px;
    box-sizing: border-box;
  }

  .q1-segment, .q2-segment, .q3-segment, .q4-segment {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.65rem;
    font-family: monospace;
    font-weight: bold;
    border-radius: 2px;
    box-sizing: border-box;
    cursor: default;
    transition: filter 0.15s ease;
  }

  .q1-segment:hover, .q2-segment:hover, .q3-segment:hover, .q4-segment:hover {
    filter: brightness(1.1);
  }

  .heatmap-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(255, 255, 255, 0.04);
    margin-top: 1rem;
  }

  /* SVG Line Chart styling */
  .chart-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1rem;
    background: rgba(9, 13, 22, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.02);
    border-radius: 0.5rem;
  }

  .chart-legend {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.75rem;
    margin-top: 0.75rem;
  }

  /* Leaderboard Styling */
  .leaderboard-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    max-height: 400px;
    overflow-y: auto;
    padding-right: 0.25rem;
  }

  .leaderboard-list::-webkit-scrollbar {
    width: 4px;
  }
  .leaderboard-list::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.01);
  }
  .leaderboard-list::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 2px;
  }

  .bill-card {
    background: rgba(9, 13, 22, 0.6);
    border-radius: 0.5rem;
    padding: 0.75rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    transition: transform 0.2s ease, border-color 0.2s ease;
  }
  
  .bill-card:hover {
    transform: translateY(-1px);
    background: rgba(15, 23, 42, 0.8);
  }

  .bill-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
  }

  .bill-idx {
    font-family: monospace;
    font-size: 0.65rem;
    color: #475569;
    font-weight: 700;
  }

  .bill-days {
    font-family: monospace;
    font-weight: 800;
    font-size: 0.85rem;
  }

  .bill-title {
    margin: 0.25rem 0 0 0;
    font-size: 0.8rem;
    font-weight: 600;
    color: #ffffff;
    text-align: left;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .bill-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.65rem;
    color: #64748b;
    margin-top: 0.25rem;
    text-align: left;
  }
  
  .sticky-filter {
    position: sticky;
    top: 1rem;
    z-index: 40;
    background: rgba(9, 13, 22, 0.95);
    backdrop-filter: blur(8px);
    padding: 1rem;
    border-radius: 0.5rem;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
  }
  
  .dashboard-tabs-container {
    display: flex;
    justify-content: center;
    width: 100%;
  }

  .dashboard-tabs {
    display: flex;
    gap: 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0 1rem;
  }

  .dash-tab {
    background: transparent;
    border: none;
    color: #94a3b8;
    padding: 0.75rem 0.25rem;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
  }

  .dash-tab:hover {
    color: #ffffff;
    border-bottom-color: rgba(255, 255, 255, 0.3);
  }

  .dash-tab.active {
    background: transparent;
    color: #38bdf8;
    border-bottom: 2px solid #38bdf8;
    font-weight: 700;
  }

  /* Unified Audit Card Styles */
  .unified-audit-card {
    background: rgba(9, 13, 22, 0.6);
    border: 1px solid rgba(30, 41, 59, 0.8);
    border-radius: 0.75rem;
    padding: 1.5rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
  }

  .unified-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(30, 41, 59, 0.8);
    padding-bottom: 1rem;
    margin-bottom: 1.5rem;
  }

  .unified-title {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .title-with-icon {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .title-with-icon h2 {
    font-size: 1.125rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.025em;
    margin: 0;
  }

  .amber-heading { color: #f59e0b !important; }
  .emerald-heading { color: #10b981 !important; }

  :global(.amber-icon) { color: #f59e0b; }
  :global(.emerald-icon) { color: #10b981; }

  .dummy-pills {
    display: flex;
    gap: 0.5rem;
  }

  .dummy-pill {
    padding: 0.375rem 0.75rem;
    font-size: 0.625rem;
    text-transform: uppercase;
    font-weight: 700;
    border-radius: 9999px;
    background: transparent;
    color: #64748b;
    border: 1px solid rgba(51, 65, 85, 0.5);
  }

  .dummy-pill.active {
    background: rgba(245, 158, 11, 0.1);
    color: #f59e0b;
    border-color: rgba(245, 158, 11, 0.2);
  }

  .unified-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2.5rem;
  }

  @media (max-width: 1024px) {
    .unified-grid {
      grid-template-columns: 1fr;
    }
  }

  .unified-column {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .column-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .column-header span {
    font-size: 0.6875rem;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 0.025em;
    text-transform: uppercase;
  }

  .column-header .sub-label {
    color: #94a3b8;
    text-transform: none;
    font-weight: 400;
  }

  /* Table overrides */
  .half-life-table.borderless th {
    color: rgba(245, 158, 11, 0.8);
    font-size: 0.625rem;
    border-bottom: none;
    padding-bottom: 0.75rem;
  }

  .half-life-table.borderless td {
    border-bottom: none;
    border-top: 1px solid rgba(30, 41, 59, 0.5);
    padding: 0.75rem 0.25rem;
  }

  .session-label {
    font-weight: 700;
    color: #ffffff;
    font-size: 0.8125rem;
    letter-spacing: 0.025em;
  }

  .val-label {
    color: #cbd5e1;
    font-size: 0.8125rem;
  }

  .mark-label {
    color: #f59e0b;
    font-family: monospace;
    font-weight: 700;
    font-size: 0.8125rem;
  }

  .elapsed-text {
    color: #64748b;
    font-size: 0.6875rem;
    font-family: sans-serif;
    font-weight: 400;
    letter-spacing: 0.025em;
  }

  /* Heatmap */
  .heatmap-row-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 0.125rem;
  }

  .count-label {
    color: #64748b;
    font-size: 0.625rem;
    letter-spacing: 0.025em;
  }

  .thick-bar {
    height: 1.375rem !important;
    background: rgba(15, 23, 42, 0.5);
    border: none !important;
    padding: 0 !important;
  }

  .segment {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.625rem;
    font-weight: 700;
    border-right: 1px solid #0f172a;
  }

  .q1-color { background-color: #312e81; color: #a5b4fc; }
  .q2-color { background-color: #0284c7; color: #e0f2fe; }
  .q3-color { background-color: #d97706; color: #fef3c7; }
  .q4-color { background-color: #b91c1c; color: #fee2e2; border-right: none; }

  .q1-bg { background-color: #312e81; }
  .q2-bg { background-color: #0284c7; }
  .q3-bg { background-color: #d97706; }
  .q4-bg { background-color: #b91c1c; }

  .heatmap-legend.centered {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    justify-content: center;
    padding-top: 1rem;
    font-size: 0.65rem;
    color: #94a3b8;
  }
  .legend-item {
    display: flex;
    align-items: center;
    gap: 0.375rem;
  }
  .legend-dot {
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 0.125rem;
  }

  /* Leaderboards extra */
  .bill-card-amber {
    background: #0d1322;
    border: 1px solid rgba(245, 158, 11, 0.1);
    border-radius: 0.5rem;
    padding: 1rem;
    margin-bottom: 0.75rem;
    transition: all 0.2s ease;
  }
  .bill-card-amber:hover {
    border-color: rgba(245, 158, 11, 0.3);
  }

  .bill-card-emerald {
    background: #0d1322;
    border: 1px solid rgba(16, 185, 129, 0.1);
    border-radius: 0.5rem;
    padding: 1rem;
    margin-bottom: 0.75rem;
    transition: all 0.2s ease;
  }
  .bill-card-emerald:hover {
    border-color: rgba(16, 185, 129, 0.3);
  }

  .amber-text { color: #f59e0b; }
  .emerald-text { color: #34d399; }

  .days-label {
    font-size: 0.75rem;
    color: #94a3b8;
    font-family: sans-serif;
    font-weight: 400;
    letter-spacing: 0.025em;
  }

  .font-expanded {
    font-size: 0.9rem;
    line-height: 1.375;
    margin: 0.5rem 0;
  }

  .bill-meta-row {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    font-size: 0.75rem;
    color: #cbd5e1;
  }

  .dates-meta {
    font-family: monospace;
    font-size: 0.7rem;
    color: #94a3b8;
    margin-top: 0.25rem;
  }
  
  /* STAGE 7: DURATION STACKED BARS */
  .duration-legend { display: flex; gap: 1rem; margin-bottom: 1rem; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
  .duration-legend .legend-item { display: flex; align-items: center; gap: 0.35rem; }
  .duration-legend .legend-color { display: inline-block; width: 0.75rem; height: 0.75rem; border-radius: 0.2rem; }
  
  .t1-color { background-color: #6366f1; }
  .t2-color { background-color: #10b981; }
  .t3-color { background-color: #f59e0b; }
  
  .t1-bg { background-color: #6366f1; }
  .t2-bg { background-color: #10b981; border-left: 1px solid rgba(0,0,0,0.25); }
  .t3-bg { background-color: #f59e0b; border-left: 1px solid rgba(0,0,0,0.25); }

  .duration-y-axis { display: flex; flex-direction: column; gap: 0.75rem; }
  .duration-row { display: flex; align-items: center; gap: 1rem; }
  .duration-label { width: 4.5rem; text-align: right; font-size: 0.85rem; font-weight: 600; color: #cbd5e1; }
  
  .duration-bar-container { 
    flex: 1; 
    background: rgba(30, 41, 59, 0.4); 
    border-radius: 0.3rem; 
    height: 2.25rem; 
    display: flex; 
    overflow: hidden; 
    border: 1px solid rgba(51, 65, 85, 0.6); 
  }
  
  .duration-segment { 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    font-size: 0.75rem; 
    font-weight: 700; 
    color: #ffffff; 
    box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.1); 
    transition: filter 0.2s ease; 
  }
  
  .duration-segment:hover { filter: brightness(1.15); }
  .duration-empty { width: 100%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; color: #64748b; font-style: italic; }
  
  .duration-total { width: 3.5rem; text-align: left; font-size: 0.85rem; font-weight: 700; color: #38bdf8; }
</style>
