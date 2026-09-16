(() => {
  const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
  }[char]));

  const style = document.createElement('style');
  style.textContent = `
    .crm-form { display:grid; grid-template-columns:1.4fr 1fr 1.2fr auto; gap:10px; padding:18px; }
    .crm-form input,.crm-form select { min-width:0; padding:11px 12px; border:1px solid var(--line); border-radius:9px; color:var(--ink); background:var(--surface); outline:0; font-size:12px; }
    .crm-form input:focus,.crm-form select:focus { border-color:#8eb879; box-shadow:0 0 0 3px rgba(142,184,121,.18); }
    .crm-table { overflow:auto; }
    .crm-row { display:grid; grid-template-columns:1.5fr .8fr 1fr 1fr 1fr; min-width:680px; gap:14px; align-items:center; padding:14px 18px; border-bottom:1px solid var(--line); }
    .crm-row:last-child { border-bottom:0; }
    .crm-row.header { color:var(--muted); font:500 10px DM Mono,monospace; text-transform:uppercase; }
    .crm-company { font-size:12px; font-weight:800; }
    @media (max-width:760px) { .crm-form { grid-template-columns:1fr; } }
  `;
  document.head.appendChild(style);

  const nav = document.querySelector('.nav[aria-label="Primary navigation"]');
  const content = document.querySelector('main.content');
  if (!nav || !content || document.querySelector('[data-view="crm"]')) return;

  const navButton = document.createElement('button');
  navButton.type = 'button';
  navButton.dataset.view = 'crm';
  navButton.innerHTML = '<span class="nav-icon">◈</span>CRM';
  nav.appendChild(navButton);

  const view = document.createElement('section');
  view.className = 'view';
  view.id = 'view-crm';
  view.innerHTML = `
    <div class="hero"><div><div class="eyebrow">Customer relationships</div><h1>CRM</h1><p>Manage real companies, prospects, and leads connected to your workforce.</p></div></div>
    <form class="panel crm-form" id="crm-form">
      <input name="company" placeholder="Company name" required>
      <select name="record_type" aria-label="Record type"><option value="company">Company</option><option value="prospect">Prospect</option><option value="lead">Lead</option><option value="client">Client</option></select>
      <input name="industry" placeholder="Industry (optional)">
      <button class="primary" type="submit">Add record</button>
    </form>
    <div class="section-head"><h2>Records</h2><span class="date" id="crm-count"></span></div>
    <div class="panel crm-table" id="crm-records"><div class="empty">Loading CRM records...</div></div>
  `;
  content.appendChild(view);

  const recordsNode = view.querySelector('#crm-records');
  const countNode = view.querySelector('#crm-count');
  const render = (records) => {
    countNode.textContent = `${records.length} record${records.length === 1 ? '' : 's'}`;
    if (!records.length) {
      recordsNode.innerHTML = '<div class="empty">No CRM records yet. Add a company, prospect, lead, or client above.</div>';
      return;
    }
    recordsNode.innerHTML = `
      <div class="crm-row header"><span>Company</span><span>Type</span><span>Industry</span><span>Stage</span><span>Created</span></div>
      ${records.map((record) => `<div class="crm-row"><span class="crm-company">${escapeHtml(record.company)}</span><span>${escapeHtml(record.record_type)}</span><span>${escapeHtml(record.industry || '—')}</span><span>${escapeHtml(record.sales_stage)}</span><span class="task-meta">${escapeHtml(record.created_at)}</span></div>`).join('')}
    `;
  };

  const load = async () => {
    recordsNode.innerHTML = '<div class="empty">Loading CRM records...</div>';
    const response = await fetch('/api/crm', { cache: 'no-store' });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || 'CRM API failed to load.');
    render(payload.records || []);
  };

  view.querySelector('#crm-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const button = form.querySelector('button');
    button.disabled = true;
    try {
      const response = await fetch('/api/crm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(Object.fromEntries(new FormData(form)))
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || 'CRM record could not be saved.');
      form.reset();
      await load();
    } catch (error) {
      recordsNode.innerHTML = `<div class="empty">${escapeHtml(error.message)}</div>`;
    } finally {
      button.disabled = false;
    }
  });

  load().catch((error) => {
    recordsNode.innerHTML = `<div class="empty">${escapeHtml(error.message)}</div>`;
  });
})();
